#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

# -----------------------------------------------------------------------------
# Fast device discovery helpers (Windows focused)
# - Auto-detect local subnets via `ipconfig`
# - ARP priming without ICMP dependency
# - Parse ARP table -> alive candidates
# - Multi-threaded SSH port scan (22, 2222, 2200)
# - Mark NVIDIA OUIs (Jetson candidates)
# - Reverse DNS names (private IP only, async with timeout)
# - Return a list[dict] for downstream usage
# - VERBOSE DEBUG LOGS at each stage (before/after parsing)
# -----------------------------------------------------------------------------

# =========================
# 공통 상수 & 디버그 유틸
# =========================

NVIDIA_OUIS = {"00:04:4b", "48:b0:2d", "b8:59:9f"}

def _dbg_head(label: str):
    import logging
    logging.debug("=" * 12 + f" {label} " + "=" * 12)

def _dbg_list(label: str, items, max_show: int = 10):
    import logging
    n = len(items) if hasattr(items, "__len__") else None
    if n is not None:
        logging.debug(f"{label} (count={n})")
    else:
        logging.debug(f"{label}")
    c = 0
    for x in items:
        if c >= max_show:
            logging.debug(f"... (showing first {max_show})")
            break
        logging.debug(f"{x}")
        c += 1

def _dbg_text(label: str, text: str, max_lines: int = 20):
    import logging
    lines = (text or "").splitlines()
    logging.debug(f"{label} (lines={len(lines)})")
    for i, line in enumerate(lines[:max_lines]):
        logging.debug(f"{i+1:02d}: {line}")
    if len(lines) > max_lines:
        logging.debug(f"... (showing first {max_lines} lines)")

# =========================
# 자동 감지 (ipconfig) 버전
# =========================
@ensure_seconds_measured
def ensure_device_ssh_available_ips_found_auto_via_ipconfig():
    """
    Auto-detect local IPv4 subnets from `ipconfig` (Windows), then for each:
      (1) ARP priming (no ICMP dependency)
      (2) Parse ARP table for alive candidates in that CIDR
      (3) Multi-threaded SSH port scan (22, 2222, 2200)
      (4) Flag NVIDIA OUIs and attach reverse DNS name (private IP only)
    Debug: prints BEFORE/AFTER parsing snapshots at each stage
    Returns: List[Dict[str, Any]]
    """
    # Lazy imports
    import logging
    import ipaddress
    import socket
    import subprocess
    import re
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from typing import List, Dict, Any, Tuple

    # ----------------------------
    # Tunables
    # ----------------------------
    WORKERS = 256
    TIMEOUT_CONNECT = 0.25  # seconds, for TCP connect attempts
    PRIMING_PORTS = (22, 80, 443, 1)  # short TCP pokes to populate ARP
    SSH_PORT_CANDIDATES = (22, 2222, 2200)  # scan these as SSH candidates
    REVERSE_DNS_TIMEOUT = 0.1  # seconds

    # ----------------------------
    # Utilities
    # ----------------------------
    def _run_cmd(cmd: List[str], timeout: float = 3.0) -> str:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=timeout)
            return (r.stdout or "") + (r.stderr or "")
        except Exception as e:
            logging.debug(f"_run_cmd error for {cmd}: {e}")
            return ""

    def _mask_to_prefix(mask: str) -> int:
        """Convert dotted mask to prefix (e.g. 255.255.255.0 -> 24).
        If invalid/ non-contiguous, fall back to /24 for safety."""
        try:
            parts = [int(x) for x in mask.split(".")]
            if len(parts) != 4 or any(p < 0 or p > 255 for p in parts):
                return 24
            bits = "".join(f"{p:08b}" for p in parts)
            if "01" in bits:  # non-contiguous
                return 24
            return bits.count("1")
        except Exception:
            return 24

    def _ip_to_network_cidr(ip: str, prefix: int) -> str:
        """Normalize to a network CIDR string.
        If too broad (< /24), clamp to /24 to avoid huge scans."""
        try:
            if prefix < 24:
                prefix = 24
            net = ipaddress.ip_network(f"{ip}/{prefix}", strict=False)
            return str(net)
        except Exception:
            base = ".".join(ip.split(".")[:3]) + ".0/24"
            return str(ipaddress.ip_network(base, strict=False))

    def _is_private_cidr(cidr: str) -> bool:
        try:
            return ipaddress.ip_network(cidr, strict=False).is_private
        except Exception:
            return False

    def _is_private_ip(ip: str) -> bool:
        try:
            return ipaddress.ip_address(ip).is_private
        except Exception:
            return False

    def _parse_ipconfig_pairs() -> List[Tuple[str, int]]:
        """
        Parse `ipconfig` output (Korean/English) to get (IPv4, prefix) pairs.
        - Korean: "IPv4 주소", "서브넷 마스크"
        - English: "IPv4 Address", "Subnet Mask"
        Exclude 127.x and 169.254.x link-local.
        """
        _dbg_head("RUN ipconfig")
        out = _run_cmd(["ipconfig"])
        _dbg_text("ipconfig RAW OUTPUT", out, max_lines=30)
        if not out:
            return []

        ipv4_re = re.compile(r"(ipv4\s*주소|ipv4\s*address)\s*.*?:\s*([\d\.]+)", re.IGNORECASE)
        mask_re = re.compile(r"(서브넷\s*마스크|subnet\s*mask)\s*.*?:\s*([\d\.]+)", re.IGNORECASE)

        pairs: List[Tuple[str, int]] = []
        pending_ip = None

        for raw in out.splitlines():
            line = raw.strip()
            m_ip = ipv4_re.search(line)
            if m_ip:
                ip_val = m_ip.group(2).strip()
                if ip_val.startswith("169.254.") or ip_val.startswith("127."):
                    pending_ip = None
                else:
                    pending_ip = ip_val
                continue
            m_mask = mask_re.search(line)
            if m_mask and pending_ip:
                mask = m_mask.group(2).strip()
                pref = _mask_to_prefix(mask)
                pairs.append((pending_ip, pref))
                pending_ip = None

        if pending_ip:
            pairs.append((pending_ip, 24))

        _dbg_list("PARSED (IPv4, prefix) pairs", [f"{ip}/{pref}" for ip, pref in pairs], max_show=20)
        return pairs

    def _unique_cidrs_from_pairs(pairs: List[Tuple[str, int]]) -> List[str]:
        cidrs, seen = [], set()
        for ip, pref in pairs:
            cidr = _ip_to_network_cidr(ip, pref)
            if cidr not in seen:
                seen.add(cidr)
                cidrs.append(cidr)
        _dbg_list("CIDRs constructed from pairs", cidrs, max_show=20)
        return cidrs

    def hosts_from_cidr(cidr: str):
        net = ipaddress.ip_network(cidr, strict=False)
        for ip in net.hosts():
            yield str(ip)

    def _try_connect(ip: str, port: int, timeout: float) -> bool:
        try:
            with socket.create_connection((ip, port), timeout=timeout):
                return True
        except Exception:
            return False

    def _arp_prime_ip(ip: str) -> None:
        # 짧은 TCP connect 시도 → L2 ARP 요청 유도
        for p in PRIMING_PORTS:
            _try_connect(ip, p, TIMEOUT_CONNECT)

    def _get_arp_table() -> Dict[str, str]:
        """Return {ip: mac_lower}. Try `ip neigh show` then `arp -a`."""
        mapping: Dict[str, str] = {}

        _dbg_head("RUN ip neigh show")
        neigh = _run_cmd(["ip", "neigh", "show"]).lower()
        _dbg_text("ip neigh RAW", neigh, max_lines=20)
        if neigh:
            for line in neigh.splitlines():
                s = line.strip().lower()
                parts = [p for p in s.split() if p]
                if len(parts) >= 5 and parts[0].count(".") == 3:
                    ip = parts[0]
                    mac = ""
                    if "lladdr" in parts:
                        try:
                            mac = parts[parts.index("lladdr") + 1]
                        except Exception:
                            mac = ""
                    if ip and mac:
                        mapping[ip] = mac.replace("-", ":").lower()

        _dbg_head("RUN arp -a")
        arp = _run_cmd(["arp", "-a"]).lower()
        _dbg_text("arp -a RAW", arp, max_lines=20)
        if arp:
            for line in arp.splitlines():
                line = line.strip()
                if not line:
                    continue
                ip = None
                mac = None
                if "(" in line and ")" in line and " at " in line:
                    # Linux-like: "? (IP) at MAC [ether] on eth0"
                    try:
                        ip = line.split("(")[1].split(")")[0].strip()
                        mac = line.split(" at ")[1].split(" ")[0].strip()
                    except Exception:
                        pass
                else:
                    # Windows-like: "IP MAC dynamic"
                    parts = [tok for tok in line.replace("\t", " ").split(" ") if tok]
                    if len(parts) >= 2:
                        for idx, tok in enumerate(parts):
                            if tok.count(".") == 3:
                                ip = tok
                                for j in range(idx + 1, min(idx + 4, len(parts))):
                                    c = parts[j]
                                    if any(sep in c for sep in [":", "-"]) and len(c) >= 11:
                                        mac = c
                                        break
                                break
                if ip and mac:
                    mapping[ip] = mac.replace("-", ":").lower()

        _dbg_list("ARP table parsed entries (ip -> mac)", [f"{k} {v}" for k, v in mapping.items()], max_show=20)
        return mapping

    def _is_unicast_host_in(cidr: str, ip: str) -> bool:
        net = ipaddress.ip_network(cidr, strict=False)
        addr = ipaddress.ip_address(ip)
        return (addr in net) and (addr != net.network_address) and (addr != net.broadcast_address)

    def _is_nvidia(mac: str) -> bool:
        if not mac or ":" not in mac:
            return False
        return ":".join(mac.split(":")[0:3]) in NVIDIA_OUIS

    # 퍼블릭 IP에서는 역방향 조회를 하지 않아 지연 방지
    def _rev_name(ip: str) -> str:
        if not _is_private_ip(ip):
            return ""
        try:
            return socket.gethostbyaddr(ip)[0]
        except Exception:
            return ""

    # ----------------------------
    # Execute
    # ----------------------------
    pairs = _parse_ipconfig_pairs()
    if not pairs:
        logging.debug("[PkTexts.NET] ipconfig parse failed (need PowerShell/cmd, locale?).")
        return []

    cidrs_all = _unique_cidrs_from_pairs(pairs)
    # 기본: 프라이빗만 스캔
    cidrs = [c for c in cidrs_all if _is_private_cidr(c)]
    if not cidrs:
        logging.debug("[PkTexts.NET] No private CIDR found from ipconfig. "
                      "If your Jetson is on a private LAN, run from that LAN or enable a private NIC.")
        # 필요시 퍼블릭까지 스캔하려면 아래 줄 주석 해제:
        # cidrs = cidrs_all

    # 프라이빗 우선 정렬
    cidrs = sorted(cidrs, key=lambda c: (not _is_private_cidr(c), c))
    _dbg_list("CIDRs selected for scan (private first)", cidrs, max_show=20)

    if not cidrs:
        return []

    all_results: List[Dict[str, Any]] = []

    for cidr in cidrs:
        _dbg_head(f"SCAN START for {cidr}")
        logging.debug(f"[PkTexts.SCAN] [CIDR] {cidr}")

        targets = list(hosts_from_cidr(cidr))
        _dbg_list("Targets (first few)", targets, max_show=15)

        # (1) ARP priming
        logging.debug(f"[PkTexts.SCAN] (1/4) ARP priming {cidr} with {WORKERS} threads...")
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            list(as_completed(ex.submit(_arp_prime_ip, ip) for ip in targets))

        # (2) ARP table -> alive (filter inside this CIDR, exclude network/broadcast)
        logging.debug(f"[PkTexts.SCAN] (2/4) Reading ARP table...")
        arp_map = _get_arp_table()

        alive_ips = sorted(
            [ip for ip in arp_map.keys() if _is_unicast_host_in(cidr, ip)],
            key=lambda s: tuple(int(x) for x in s.split("."))
        )
        _dbg_list("ALIVE via ARP (filtered)", alive_ips, max_show=30)

        if not alive_ips:
            logging.debug(f"[PkTexts.SCAN] [CIDR {cidr}] No ARP-alive hosts.")
            _dbg_head(f"SCAN END for {cidr}")
            continue

        # (3) Multi-port SSH check
        logging.debug(f"[PkTexts.SCAN] (3/4) SSH check on {len(alive_ips)} hosts (ports={SSH_PORT_CANDIDATES})")
        open_map: Dict[str, List[int]] = {ip: [] for ip in alive_ips}
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            fut_map = {}
            for ip in alive_ips:
                for p in SSH_PORT_CANDIDATES:
                    fut_map[ex.submit(_try_connect, ip, p, TIMEOUT_CONNECT)] = (ip, p)
            for fut in as_completed(fut_map):
                ip, p = fut_map[fut]
                ok = False
                try:
                    ok = fut.result()
                except Exception:
                    ok = False
                if ok:
                    open_map[ip].append(p)
                    logging.debug(f"[PkTexts.SCAN] [SSH OPEN] {ip}:{p}")

        # SSH open summary
        ssh_open_count = sum(1 for v in open_map.values() if v)
        logging.debug(f"[PkTexts.SCAN] SSH open hosts count = {ssh_open_count}")
        if ssh_open_count:
            examples = [f"{ip}:{','.join(map(str, ports))}" for ip, ports in open_map.items() if ports][:10]
            _dbg_list("SSH OPEN examples", examples, max_show=10)

        # (4) Summary & results (이름 조회는 비동기 + 타임아웃)
        from concurrent.futures import ThreadPoolExecutor as TPE
        name_pool = TPE(max_workers=32)
        f_name = {ip: name_pool.submit(_rev_name, ip) for ip in alive_ips}

        logging.debug(f"[PkTexts.SCAN] (4/4) Summary for {cidr}")
        for ip in alive_ips:
            mac = arp_map.get(ip, "")
            try:
                name = f_name[ip].result(timeout=REVERSE_DNS_TIMEOUT)
            except Exception:
                name = ""
            ports = sorted(open_map.get(ip, []))
            r = {
                "cidr": cidr,
                "ip": ip,
                "name": name,
                "alive": True,
                "ssh_open_any": bool(ports),
                "ssh_open_ports": ports,
                "mac": mac,
                "is_nvidia": _is_nvidia(mac),
            }
            tag = []
            if r["ssh_open_any"]:
                tag.append(f"SSH:{','.join(str(x) for x in ports)}")
            if r["is_nvidia"]:
                tag.append("NVIDIA?")
            tag_s = f" [{' '.join(tag)}]" if tag else ""
            mac_s = f"  MAC={mac}" if mac else ""
            name_s = f"  NAME={name}" if name else ""
            logging.debug(f"{ip}{mac_s}{name_s}{tag_s}")
            all_results.append(r)

        name_pool.shutdown(wait=False)
        _dbg_head(f"SCAN END for {cidr}")

    if not all_results:
        logging.debug("[PkTexts.NET] No hosts found across all local subnets. Check VLAN/static IP/APIPA/DHCP/switch port/cable.")
    else:
        logging.debug(f"[PkTexts.NET] TOTAL RESULTS: {len(all_results)}")
    return all_results


# =========================
# 고정 CIDR 버전
# =========================
@ensure_seconds_measured
def ensure_device_ssh_available_ips_found_fixed():
    """
    Fixed-CIDR variant for quick checks.
    Edit CIDR below as needed.
    """
    import logging
    import ipaddress
    import socket
    import subprocess
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from typing import List, Dict, Any

    CIDR = "172.21.239.0/24"  # <--- 필요 시 수정
    WORKERS = 256
    TIMEOUT_CONNECT = 0.25
    PRIMING_PORTS = (22, 80, 443, 1)
    SSH_PORT_CANDIDATES = (22, 2222, 2200)
    REVERSE_DNS_TIMEOUT = 0.1

    def _run_cmd(cmd: List[str], timeout: float = 3.0) -> str:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=timeout)
            return (r.stdout or "") + (r.stderr or "")
        except Exception as e:
            logging.debug(f"_run_cmd error for {cmd}: {e}")
            return ""

    def hosts_from_cidr(cidr: str):
        net = ipaddress.ip_network(cidr, strict=False)
        for ip in net.hosts():
            yield str(ip)

    def _try_connect(ip: str, port: int, timeout: float) -> bool:
        try:
            with socket.create_connection((ip, port), timeout=timeout):
                return True
        except Exception:
            return False

    def _arp_prime_ip(ip: str) -> None:
        for p in PRIMING_PORTS:
            _try_connect(ip, p, TIMEOUT_CONNECT)

    def _get_arp_table() -> Dict[str, str]:
        mapping: Dict[str, str] = {}

        neigh = _run_cmd(["ip", "neigh", "show"]).lower()
        if neigh:
            for line in neigh.splitlines():
                s = line.strip().lower()
                parts = [p for p in s.split() if p]
                if len(parts) >= 5 and parts[0].count(".") == 3:
                    ip = parts[0]
                    mac = ""
                    if "lladdr" in parts:
                        try:
                            mac = parts[parts.index("lladdr") + 1]
                        except Exception:
                            mac = ""
                    if ip and mac:
                        mapping[ip] = mac.replace("-", ":").lower()

        arp = _run_cmd(["arp", "-a"]).lower()
        if arp:
            for line in arp.splitlines():
                line = line.strip()
                if not line:
                    continue
                ip = None
                mac = None
                if "(" in line and ")" in line and " at " in line:
                    try:
                        ip = line.split("(")[1].split(")")[0].strip()
                        mac = line.split(" at ")[1].split(" ")[0].strip()
                    except Exception:
                        pass
                else:
                    parts = [tok for tok in line.replace("\t", " ").split(" ") if tok]
                    if len(parts) >= 2:
                        for idx, tok in enumerate(parts):
                            if tok.count(".") == 3:
                                ip = tok
                                for j in range(idx + 1, min(idx + 4, len(parts))):
                                    c = parts[j]
                                    if any(sep in c for c in [":", "-"]) and len(c) >= 11:
                                        mac = c
                                        break
                                break
                if ip and mac:
                    mapping[ip] = mac.replace("-", ":").lower()
        return mapping

    def _is_unicast_host_in(cidr: str, ip: str) -> bool:
        net = ipaddress.ip_network(cidr, strict=False)
        addr = ipaddress.ip_address(ip)
        return (addr in net) and (addr != net.network_address) and (addr != net.broadcast_address)

    def _is_nvidia(mac: str) -> bool:
        if not mac or ":" not in mac:
            return False
        return ":".join(mac.split(":")[0:3]) in NVIDIA_OUIS

    def _rev_name(ip: str) -> str:
        # 고정 CIDR에서도 퍼블릭 IP일 수 있으므로 동일 정책 적용
        try:
            if not ipaddress.ip_address(ip).is_private:
                return ""
        except Exception:
            return ""
        try:
            return socket.gethostbyaddr(ip)[0]
        except Exception:
            return ""

    _dbg_head(f"FIXED SCAN START for {CIDR}")
    logging.debug(f"[PkTexts.SCAN] [CIDR] {CIDR}")

    targets = list(hosts_from_cidr(CIDR))
    _dbg_list("Targets (first few)", targets, max_show=15)

    logging.debug(f"[PkTexts.SCAN] (1/4) ARP priming {CIDR} ...")
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        list(as_completed(ex.submit(_arp_prime_ip, ip) for ip in targets))

    logging.debug(f"[PkTexts.SCAN] (2/4) Reading ARP table...")
    arp_map = _get_arp_table()
    _dbg_list("ARP parsed entries (ip -> mac)", [f"{k} {v}" for k, v in arp_map.items()], max_show=20)

    alive_ips = sorted(
        [ip for ip in arp_map.keys() if _is_unicast_host_in(CIDR, ip)],
        key=lambda s: tuple(int(x) for x in s.split("."))
    )
    _dbg_list("ALIVE via ARP (filtered)", alive_ips, max_show=30)

    if not alive_ips:
        logging.debug(f"[PkTexts.SCAN] [CIDR {CIDR}] No ARP-alive hosts.")
        _dbg_head(f"FIXED SCAN END for {CIDR}")
        return []

    logging.debug(f"[PkTexts.SCAN] (3/4) SSH check on {len(alive_ips)} hosts (ports={SSH_PORT_CANDIDATES})")
    open_map: Dict[str, List[int]] = {ip: [] for ip in alive_ips}
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        fut_map = {}
        for ip in alive_ips:
            for p in SSH_PORT_CANDIDATES:
                fut_map[ex.submit(_try_connect, ip, p, TIMEOUT_CONNECT)] = (ip, p)
        for fut in as_completed(fut_map):
            ip, p = fut_map[fut]
            ok = False
            try:
                ok = fut.result()
            except Exception:
                ok = False
            if ok:
                open_map[ip].append(p)
                logging.debug(f"[PkTexts.SCAN] [SSH OPEN] {ip}:{p}")

    ssh_open_count = sum(1 for v in open_map.values() if v)
    logging.debug(f"[PkTexts.SCAN] SSH open hosts count = {ssh_open_count}")
    if ssh_open_count:
        examples = [f"{ip}:{','.join(map(str, ports))}" for ip, ports in open_map.items() if ports][:10]
        _dbg_list("SSH OPEN examples", examples, max_show=10)

    # Summary (역방향 조회는 비동기 + 타임아웃)
    from concurrent.futures import ThreadPoolExecutor as TPE
    name_pool = TPE(max_workers=32)
    f_name = {ip: name_pool.submit(_rev_name, ip) for ip in alive_ips}

    logging.debug(f"[PkTexts.SCAN] (4/4) Summary for {CIDR}")
    results: List[Dict[str, Any]] = []
    for ip in alive_ips:
        mac = arp_map.get(ip, "")
        try:
            name = f_name[ip].result(timeout=REVERSE_DNS_TIMEOUT)
        except Exception:
            name = ""
        ports = sorted(open_map.get(ip, []))
        r = {
            "cidr": CIDR,
            "ip": ip,
            "name": name,
            "alive": True,
            "ssh_open_any": bool(ports),
            "ssh_open_ports": ports,
            "mac": mac,
            "is_nvidia": _is_nvidia(mac),
        }
        tag = []
        if r["ssh_open_any"]:
            tag.append(f"SSH:{','.join(str(x) for x in ports)}")
        if r["is_nvidia"]:
            tag.append("NVIDIA?")
        tag_s = f" [{' '.join(tag)}]" if tag else ""
        mac_s = f"  MAC={mac}" if mac else ""
        name_s = f"  NAME={name}" if name else ""
        logging.debug(f"{ip}{mac_s}{name_s}{tag_s}")
        results.append(r)

    name_pool.shutdown(wait=False)
    _dbg_head(f"FIXED SCAN END for {CIDR}")
    return results


# =========================
# 최종 엔트리 (자동 → 고정 Fallback)
# =========================
@ensure_seconds_measured
def ensure_device_ssh_available_ips_found():
    import logging
    try:
        results = ensure_device_ssh_available_ips_found_auto_via_ipconfig()
    except Exception as e:
        logging.debug(f"[PkTexts.NET] Auto-detect scan error: {e}")
        results = []

    if results:
        return results

    logging.debug("[PkTexts.NET] Auto scan empty → trying fixed CIDR fallback...")
    try:
        return ensure_device_ssh_available_ips_found_fixed()
    except Exception as e:
        logging.debug(f"[PkTexts.NET] Fixed-CIDR scan error: {e}")
        return []
