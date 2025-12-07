from typing import List


def ensure_stand_output_streams_watched(cmds: List[str], milliseconds: int = 500, encoding: str = None):
    import logging
    import textwrap
    import traceback

    from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.get_str_dedented_from_list import get_str_dedented_from_list
    from pk_internal_tools.pk_functions.get_text_cyan import get_text_cyan
    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
    from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForEnsureSlept

    # title_str = " | ".join(cmds)
    # ensure_window_title_replaced(f"Watching {len(cmds)} commands: '{title_str}'")
    # ensure_window_title_replaced(f"Watching {len(cmds)} commands")

    try:
        previous_outputs = [None] * len(cmds)

        while True:
            current_outputs = []
            for cmd in cmds:
                stdouts, _ = ensure_command_executed(cmd, encoding=encoding, mode_silent=True)
                current_outputs.append(stdouts)
            if previous_outputs != current_outputs:
                previous_outputs = current_outputs

                ensure_console_cleared()

                full_output_list = []
                full_output_list.append(PK_UNDERLINE)  # Separator
                title = textwrap.dedent(f"""
                    --- {len(cmds)} standard output streams watched (watch -n {milliseconds / 1000}) ---
                """)
                full_output_list.append(title)

                for i, (cmd, output_lines) in enumerate(zip(cmds, current_outputs)):
                    side_seperator = "-" * int(len(PK_UNDERLINE) / 2 - len(cmd) - 2)
                    cmd_header = f"{side_seperator} {cmd} {side_seperator}"
                    full_output_list.append(cmd_header)
                    if output_lines:
                        full_output_list.extend(output_lines)

                text_to_print = get_str_dedented_from_list(full_output_list)
                logging.info(get_text_cyan(text_to_print))
            ensure_slept(milliseconds=milliseconds, setup_op=SetupOpsForEnsureSlept.SILENT)

    except KeyboardInterrupt:
        pass
    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
