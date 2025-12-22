import logging
import os

import psutil

from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


class ConnectedDrivesReport:
    """Renderable report for connected drives (excluding C:)."""

    def __init__(self, rows: list[dict], totals: dict, header: str, separator: str, tags: dict):
        self.rows = rows
        self.totals = totals
        self.header = header
        self.separator = separator
        self.tags = tags  # {"STARTED":..., "INFO":..., "FINISHED":..., "WARNING":...}

    def __repr__(self):
        try:
            lines = []
            lines.append(self.header)
            lines.append(self.separator)

            for r in self.rows:
                lines.append(
                    f"{r['drive']:<8}{r['type']:<12}{r['file_count']:<12}"
                    f"{r['capacity_mib']:<18.2f}{r['used_mib']:<18.2f}{r['free_mib']:<18.2f}"
                )

            lines.append(self.separator)
            t = self.totals
            lines.append(
                f"{'TOTAL':<8}{'—':<12}{t['file_count']:<12}"
                f"{t['capacity_mib']:<18.2f}{t['used_mib']:<18.2f}{t['free_mib']:<18.2f}"
            )
            return "\n".join(lines)
        except Exception as e:
            return f"{PkColors.RED}[ConnectedDrivesReport __repr__ Error]{PkColors.RESET} {e}"


@ensure_seconds_measured
def get_connected_drives_info() -> ConnectedDrivesReport:
    # Helpers
    def to_mib(n_bytes: int) -> float:
        return n_bytes / (1024 ** 2)

    header = (
        f"{'Drive':<8}"
        f"{'Type':<12}"
        f"{'File Count':<12}"
        f"{'Capacity (MiB)':<18}"
        f"{'Used (MiB)':<18}"
        f"{'Free (MiB)':<18}"
    )
    separator = "-" * len(header)

    # PkTexts 초기화 보장을 위해 함수 내부에서 tags 딕셔너리 생성
    tags = {
        "STARTED": PkTexts.STARTED,
        "INFO": PkTexts.INFO,
        "FINISHED": PkTexts.SUCCEEDED,
        "WARNING": PkTexts.WARNING,
    }

    logging.debug(f"{tags['STARTED']} Drive scan (excluding C:)")
    logging.debug(header)
    logging.debug(separator)

    partitions = psutil.disk_partitions(all=False)

    rows: list[dict] = []
    total_file_count = 0
    total_capacity_bytes = 0
    total_used_bytes = 0
    total_free_bytes = 0

    for part in partitions:
        drive_letter = part.device.rstrip("\\")  # e.g., 'D:'

        # Skip C:
        if drive_letter.upper().startswith("C:"):
            continue

        # Skip inaccessible or transient mountpoints
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            logging.warning(f"{tags['WARNING']} Permission denied: {part.mountpoint}")
            continue
        except FileNotFoundError:
            logging.warning(f"{tags['WARNING']} Mountpoint not found: {part.mountpoint}")
            continue
        except OSError as e:
            logging.warning(f"{tags['WARNING']} OS error on {part.mountpoint}: {e}")
            continue

        # Count files (NOTE: may take time on huge volumes)
        file_count = 0
        for _, _, files in os.walk(part.mountpoint):
            file_count += len(files)

        # Derive drive type
        if "removable" in part.opts:
            drive_type = "Removable"
        elif "cdrom" in part.opts:
            drive_type = "CD-ROM"
        elif "network" in part.opts or "nfs" in part.fstype.lower():
            drive_type = "Network"
        else:
            drive_type = "Fixed"

        capacity_b = int(usage.total)
        free_b = int(usage.free)
        used_b = capacity_b - free_b

        row = {
            "drive": drive_letter,
            "type": drive_type,
            "file_count": file_count,
            "capacity_mib": to_mib(capacity_b),
            "used_mib": to_mib(used_b),
            "free_mib": to_mib(free_b),
        }
        rows.append(row)

        logging.debug(
            f"{tags['INFO']} "
            f"{drive_letter:<8}{drive_type:<12}{file_count:<12}"
            f"{row['capacity_mib']:<18.2f}{row['used_mib']:<18.2f}{row['free_mib']:<18.2f}"
        )

        # Accumulate totals
        total_file_count += file_count
        total_capacity_bytes += capacity_b
        total_used_bytes += used_b
        total_free_bytes += free_b

    logging.debug(separator)
    logging.debug(
        f"{tags['INFO']} "
        f"{'TOTAL':<8}{'—':<12}{total_file_count:<12}"
        f"{to_mib(total_capacity_bytes):<18.2f}"
        f"{to_mib(total_used_bytes):<18.2f}"
        f"{to_mib(total_free_bytes):<18.2f}"
    )
    logging.debug(f"{tags['FINISHED']} Drive scan completed")

    totals = {
        "file_count": total_file_count,
        "capacity_mib": to_mib(total_capacity_bytes),
        "used_mib": to_mib(total_used_bytes),
        "free_mib": to_mib(total_free_bytes),
    }
    return ConnectedDrivesReport(rows, totals, header, separator, tags)
