from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def recmd_console_color():
    import inspect
    import os
    import traceback

    import ipdb
    import clipboard
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    while 1:
        try:
            for color_bg in colors:
                for color_text in colors:
                    if color_bg != color_text:
                        os.system('cls')
                        for setting_key, setting_value in get_display_info().items():
                            pass
                            # logging.debug(f'setting_key: {setting_key}  ,setting_value: {setting_value}  ')
                        # logging.debug(f"color {color_bg}{color_text}")
                        for i in range(0, 32):
                            logging.debug('')
                        to_right_nbsp = ''
                        for i in range(0, 150):
                            to_right_nbsp = to_right_nbsp + ' '
                        logging.debug(f"{to_right_nbsp}color {color_bg}{color_text}")
                        for i in range(0, 32):
                            logging.debug('')
                        os.system(f"color {color_bg}{color_text}")
                        clipboard.copy(f'color {color_bg}{color_text}')

                        ipdb.set_trace()

        except Exception as e:
            logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
            # ctrl c 가 입력이 제대로 되지 않는 현상이 있어 ctrl c 로 콘솔을 종료하는데 불편...이는 어떻게 해결하지? 일단 코드 반응속도는 마음에 드는데...
