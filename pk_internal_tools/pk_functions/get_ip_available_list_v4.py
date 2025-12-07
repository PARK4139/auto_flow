

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def get_ip_available_list_v4(timeout_ms=500, max_workers=None):
    # lazy import

    from concurrent.futures import ThreadPoolExecutor
    ip_allowed_set = get_ip_allowed_set()
    ip_set = ip_allowed_set
    ip_connected_list = []
    if not ip_set:
        return []

    # 스레드 개수 결정 (IP 개수 vs max_workers 중 작은 쪽)
    workers = max_workers or min(len(ip_set), 20)

    # 병렬로 ping 실행
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # executor.map 에서는 순서대로 ip, 결과(True/False)가 반환됨
        results = list(executor.map(lambda ip: (ip, ensure_pinged(ip)), ip_set))

    # 성공한 IP만 추출
    ip_connected_list = [ip for ip, ok in results if ok]
    logging.debug(f'''ip_connected_list={ip_connected_list} ''')
    return ip_connected_list
