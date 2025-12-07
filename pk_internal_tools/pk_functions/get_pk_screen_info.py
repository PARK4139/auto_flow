import traceback

from screeninfo import get_monitors

from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


class PkMonitor:
    """Class representing a single monitor."""

    def __init__(self, index, width, height, x, y):
        self.index = index
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def __repr__(self):
        return (
            f"Monitor {self.index}:\n"
            f"  Resolution: {self.width} x {self.height}\n"
            f"  Position:   (x={self.x}, y={self.y})"
        )


class PkScreenInfo:
    """Class representing overall screen configuration."""

    def __init__(self, monitors, total_resolution, bounding_box):
        self.monitors = monitors  # List of monitor objects
        self.count = len(monitors)  # Number of monitors
        self.total_resolution = total_resolution  # Total resolution (summed horizontally)
        self.bounding_box = bounding_box  # Bounding box resolution (OS layout)

    def __repr__(self):
        try:
            if self.monitors and isinstance(self.monitors, list):
                monitors_repr = "\n\n".join([repr(m) for m in self.monitors])

                return (
                    f"Number of monitors: {self.count}\n\n"
                    f"{monitors_repr}\n\n"
                    f"Total Resolution (Horizontal Sum): "
                    f"{self.total_resolution['width']} x {self.total_resolution['height']}\n"
                    f"Total Resolution (Bounding Box): "
                    f"{self.bounding_box['width']} x {self.bounding_box['height']}"
                )
            else:
                return (
                    f"Failed to detect {PK_ANSI_COLOR_MAP['RED']}monitors{PK_ANSI_COLOR_MAP['RESET']}.\n"
                    f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}Debug Info: "
                    f"monitors = {self.monitors}, type = {type(self.monitors)}"
                    f"{PK_ANSI_COLOR_MAP['RESET']}"
                )
        except Exception as e:
            return f"{PK_ANSI_COLOR_MAP['RED']}[PkScreenInfo __repr__ Error]{PK_ANSI_COLOR_MAP['RESET']} {e}"


@ensure_seconds_measured
def get_pk_screen_info():
    try:
        monitors_raw = get_monitors()
        monitors = []

        total_width = 0
        max_height = 0

        # bounding box 계산용
        min_x = min_y = float("inf")
        max_x = max_y = float("-inf")

        for i, m in enumerate(monitors_raw, start=1):
            monitor = PkMonitor(i, m.width, m.height, m.x, m.y)
            monitors.append(monitor)

            # 가로 합산 계산
            total_width += m.width
            if m.height > max_height:
                max_height = m.height

            # bounding box 계산
            min_x = min(min_x, m.x)
            min_y = min(min_y, m.y)
            max_x = max(max_x, m.x + m.width)
            max_y = max(max_y, m.y + m.height)

        total_resolution = {
            "width": total_width,
            "height": max_height
        }

        bounding_box = {
            "width": max_x - min_x,
            "height": max_y - min_y
        }

        return PkScreenInfo(monitors, total_resolution, bounding_box)
    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
