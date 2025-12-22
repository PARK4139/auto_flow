from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front


def get_pk_macro_code(key_name, func_n, history_reset=False):
    import logging
    import subprocess
    import textwrap
    import time
    import traceback

    from pynput import mouse, keyboard

    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.ensure_window_minimized import ensure_window_minimized
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_current_console_title import get_current_console_title
    from pk_internal_tools.pk_functions.get_easy_speakable_text import get_easy_speakable_text
    from pk_internal_tools.pk_functions.get_file_id import get_file_id
    from pk_internal_tools.pk_objects.pk_files import F_UV_PYTHON_EXE
    from pk_internal_tools.pk_functions.ensure_target_opened_advanced import ensure_target_opened_advanced
    from pk_internal_tools.pk_objects.pk_directories import D_MACROS

    """
    마우스/키보드/시간을 측정하여 매크로 코드를 작성 또는 기존 매크로를 실행합니다.
    - key_name, func_n을 조합하여 파일 ID를 생성하고 파일을 관리합니다.
    - 기존 파일이 있으면 해당 매크로 코드를 실행합니다.
    - 파일이 없거나 history_reset=True이면 마우스/키보드/시간을 측정하여 매크로 코드를 파일에 작성합니다.
    - 작성이 완료되면 ensure_target_opened_advanced를 호출하여 생성된 파일을 엽니다.
    """

    D_MACROS = D_MACROS
    D_MACROS.mkdir(exist_ok=True)
    file_id = get_file_id(key_name, func_n)
    macro_file_path = D_MACROS / f"{file_id}.py"

    should_record = history_reset or not macro_file_path.exists()

    if should_record:
        logging.info(f"Recording new macro to: {macro_file_path}. Press 'Esc' to stop.")
        text = f'{get_easy_speakable_text(key_name)} 매크로 녹화를 시작합니다. 종료하려면 Esc 키를 누르세요.'
        ensure_window_minimized(get_current_console_title())
        logging.debug(f'text={text}')
        # ensure_spoken(text)

        events = []
        last_time = time.time()

        # --- Hotkey detection logic START ---
        pressed_modifiers = set()
        modifier_keys = {
            keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
            keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r,
            keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r,
            keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r,
        }

        # --- Hotkey detection logic END ---

        def add_event(event_type, **kwargs):
            logging.info(f"Event recorded: {event_type}, details: {kwargs}")
            nonlocal last_time
            current_time = time.time()
            delay = (current_time - last_time) * 1000  # milliseconds
            if delay > 100:  # 최소 100ms 이상일 때만 시간 기록
                events.append(f"ensure_slept(milliseconds={int(delay)})")
            if event_type == 'click':
                button_name = kwargs['button'].name
                events.append(f"ensure_mouse_clicked({kwargs['x']}, {kwargs['y']}, button='{button_name}')")
            elif event_type == 'hotkey':
                formatted_keys = ", ".join([f"'{k}'" for k in kwargs['keys']])
                events.append(f"ensure_pressed({formatted_keys})")
            elif event_type == 'press':
                key = kwargs['key']
                key_name = None
                if hasattr(key, 'name'):  # Special keys (e.g., Key.cmd, Key.space)
                    key_name = key.name
                    if key_name == 'cmd':  # pynput의 cmd를 pyautogui의 win으로 변환
                        key_name = 'win'
                elif hasattr(key, 'char'):  # Normal character keys
                    key_name = key.char
                if key_name:
                    if key_name == "'":
                        key_name = "\\'"
                    events.append(f"ensure_pressed('{key_name}')")
                else:
                    logging.warning(f"Could not determine key name for: {key}")

            last_time = current_time

        def on_click(x, y, button, pressed):
            if pressed:
                add_event('click', x=x, y=y, button=button)

        def on_press(key):
            if key == keyboard.Key.esc:
                return False  # Stop listener

            if key in modifier_keys:
                pressed_modifiers.add(key)
                return

            # It's a non-modifier key
            if pressed_modifiers:
                # This is a hotkey
                mod_names = {
                    mod.name.replace('_l', '').replace('_r', '') for mod in pressed_modifiers
                }
                mod_names = {'win' if name == 'cmd' else name for name in mod_names}

                final_key_name = key.char if hasattr(key, 'char') else key.name

                all_keys = sorted(list(mod_names)) + [final_key_name]
                add_event('hotkey', keys=all_keys)
            else:
                # This is a single key press
                add_event('press', key=key)

        def on_release(key):
            if key in pressed_modifiers:
                pressed_modifiers.discard(key)

        listener_mouse = mouse.Listener(on_click=on_click)
        listener_keyboard = keyboard.Listener(on_press=on_press, on_release=on_release)

        listener_mouse.start()
        listener_keyboard.start()

        listener_keyboard.join()  # Wait until 'Esc' is pressed
        listener_mouse.stop()

        _wrapper_creation_template = textwrap.dedent('''\
            if __name__ == "__main__":
                import traceback
                from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import ensure_pk_wrapper_exception_routine_done
                from pk_internal_tools.pk_functions.ensure_pk_wrapper_finally_routine_done import ensure_pk_wrapper_finally_routine_done
                from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT
                from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done

                ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
                try:
                    {macro_code}
                except Exception as e:
                    ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
                finally:
                    ensure_pk_wrapper_finally_routine_done(traced_file=__file__, project_root_directory=D_PK_ROOT)
        ''')

        imports_and_header = textwrap.dedent("""
            from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
            from pk_internal_tools.pk_functions.ensure_typed import ensure_typed
            from pk_internal_tools.pk_functions.get_easy_speakable_text import get_easy_speakable_text
            from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
            from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
            from pk_internal_tools.pk_functions.ensure_mouse_clicked import ensure_mouse_clicked
            from pk_internal_tools.pk_functions.get_nx import get_nx

            ensure_spoken(f'{rf"{get_easy_speakable_text(get_nx(__file__).removeprefix('routine_macro_').split('_via_')[0])} 매크로 실행 시작"}')
        """)
        events_code = None
        if events:
            events_code = "\n".join(events)
        else:
            logging.warning("No events were recorded.")
            # ensure_spoken(text="기록된 매크로 이벤트가 없습니다.")
        while 1:

            full_macro_logic = imports_and_header + "\n" + events_code
            indented_macro_logic = textwrap.indent(full_macro_logic, ' ' * 8)

            final_code = _wrapper_creation_template.format(macro_code=indented_macro_logic)

            with open(macro_file_path, "w", encoding="utf-8") as f:
                f.write(final_code)

            logging.info(f"Macro recording finished. Saved to {macro_file_path}")
            # ensure_spoken(text="매크로 녹화가 완료되었습니다.")
            ensure_target_opened_advanced(str(macro_file_path))

            # pk_* -> time limit loop
            current_console_title = get_current_console_title()
            current_console_title = get_nx(current_console_title)
            logging.debug(f'current_console_title={current_console_title}')
            timeout_seconds_limit = 3
            time_s = time.time()
            while True:
                if time.time() - time_s > timeout_seconds_limit:
                    logging.debug("timeout")
                    break
                if is_window_title_front(window_title=current_console_title):
                    break
                ensure_window_to_front(current_console_title)
                ensure_slept(milliseconds=10)

            question = "매크로 녹화가 완료되었습니다. 다음 작업을 선택하세요."
            options = ["실행", "재녹화", "종료"]
            choice = ensure_value_completed(key_name=question, options=options)

            if choice == "실행":
                logging.info("사용자가 '실행'을 선택했습니다. 녹화된 매크로를 실행합니다.")
                return get_pk_macro_code(key_name, func_n, history_reset=False)
            elif choice == "재녹화":
                logging.info("사용자가 '재녹화'를 선택했습니다. 매크로를 다시 녹화합니다.")
                continue
            else:  # 종료 or other cases
                logging.info("사용자가 '종료'를 선택했습니다. 작업을 마칩니다.")
                return

    else:
        logging.info(f"Executing existing macro: {macro_file_path}")
        # ensure_spoken(text=f"{key_name} {func_n} 매크로를 실행합니다.")
        try:
            # spec = importlib.util.spec_from_file_location(macro_file_path.stem, macro_file_path)
            # macro_module = importlib.util.module_from_spec(spec)
            # spec.loader.exec_module(macro_module)

            file_to_execute = macro_file_path
            subprocess.Popen([F_UV_PYTHON_EXE, file_to_execute], creationflags=subprocess.CREATE_NEW_CONSOLE)
            logging.info("Macro execution completed.")
            # ensure_spoken(text="매크로 실행이 완료되었습니다.")
        except Exception as e:
            ensure_debugged_verbose(traceback, e)
            # ensure_spoken(text="매크로 실행 중 오류가 발생했습니다.")
