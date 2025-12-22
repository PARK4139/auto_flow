def ensure_korean_ime_activated_in_loop(interval_seconds: float = 0.5):
    import logging
    import time
    import traceback
    from datetime import datetime

    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.spinner import Spinner
    from rich.text import Text

    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    from pk_internal_tools.pk_functions.ensure_korean_ime_activated import ensure_korean_ime_activated
    from pk_internal_tools.pk_functions.get_HH_mm import get_HH_mm
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_etc import PK_WHITE, PK_DARK_GREY, PK_ORANGE, PK_GREY

    func_n = get_caller_name()

    original_log_level = logging.root.level
    logging.root.setLevel(logging.INFO)

    logging.info(f"[b {PK_ORANGE}]{func_n}[/b {PK_ORANGE}]: [{PK_WHITE}]한국어 IME 활성화 루프 시작 (주기: {interval_seconds}초).[/{PK_WHITE}]")

    status_lines = []
    max_status_lines = 5

    def update_layout() -> Layout:
        if ensure_korean_ime_activated():
            ime_status_log_message = f"[{PK_WHITE}]Korean IME is active.[/{PK_WHITE}]"
            status_style = PK_WHITE
        else:
            ime_status_log_message = f"[red]Failed to ensure Korean IME active. Attempting again.[/red]"
            status_style = "red"
        current_time_str = datetime.now().strftime('%H:%M:%S')
        current_status_message = Text.from_markup(f"[[{PK_ORANGE}]{current_time_str}[/{PK_ORANGE}]] {ime_status_log_message}", style=status_style)

        class Sections:
            # spinner_section = Panel()
            spinner_section = Spinner("dots", text=f"[{PK_GREY}]Checking KOREAN IME status...[/{PK_GREY}]", style=PK_ORANGE)
            state_section = Layout(Panel(current_status_message, border_style="none"), name="value2")
            time_section = Layout(Panel(Text(rf"time: {get_HH_mm()}", style=PK_DARK_GREY), border_style="none"), name="time_block")

        layout = Layout(name="root")
        layout.split(
            Layout(name="row1", size=1),
            Layout(name="row2", size=3),
            Layout(name="row3", size=6),
        )

        layout["row1"].update(Sections.spinner_section)
        layout["row2"].update(Sections.state_section)
        layout["row3"].update(Sections.time_section)
        layout_updated = layout
        return layout_updated

    try:
        console = Console()
        with Live(update_layout(), screen=True, refresh_per_second=10, console=console) as live:
            while True:
                live.update(update_layout())
                time.sleep(interval_seconds)
    except KeyboardInterrupt:
        logging.info(f"[b green]{func_n}[/b green]: [red]한국어 IME 활성화 루프 중단 (KeyboardInterrupt).[/red]")
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
        logging.error(f"[b red]{func_n}[/b red]: [red]IME 활성화 루프 중 오류 발생: {e}[/red]", exc_info=True)
    finally:
        logging.root.setLevel(original_log_level)
