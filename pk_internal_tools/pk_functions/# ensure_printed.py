# def ensure_printed(text_working, flush=True, print_color='', line_feed_mode=1, STAMP=None, highlight_config_dict=None):
#     import logging
#     from pk_internal_tools.pk_objects.pk_texts import PkTexts
#
#     from pk_internal_tools.pk_functions import get_pk_time_2025_10_20_1159
#     from pk_internal_tools.pk_functions.print_light_white import print_light_white
#     from pk_internal_tools.pk_functions.print_magenta import print_magenta
#     try:
#
#         # STAMP_TIME = f"[ {get_pk_time_2025_10_20_1159('now')} ]"
#         STAMP_TIME = f"[ {get_pk_time_2025_10_20_1159('weekday')} ]"
#         print_color = print_color.strip()
#
#         # Safe message getter with fallback
#         def get_safe_message(attr_name, fallback=None):
#             try:
#                 value = getattr(PkTexts, attr_name, None)
#                 if value is None:
#                     return fallback or f"[{attr_name}]"
#                 return value
#             except Exception:
#                 return fallback or f"[{attr_name}]"
#
#         default_stamp_by_color = {
#             'red': rf"[{get_safe_message('ERROR', 'ERROR')}]",
#             'yellow': rf"[{get_safe_message('TEST', 'TEST')}]",
#             'blue': rf"[{get_safe_message('INFO', 'INFO')}]",
#             'green': rf"[{get_safe_message('SUCCEEDED', 'SUCCESS')}]",
#             'white': rf"[{get_safe_message('INTERACTIVE', 'INTERACTIVE')}]",
#             'grey': rf"[{get_safe_message('WARNING', 'WARNING')}]",
#             '': rf"[{get_safe_message('WARNING', 'WARNING')}]",
#         }
#         stamp_to_use = STAMP if STAMP is not None else default_stamp_by_color.get(print_color, f"[ {get_safe_message('WARNING', 'WARNING')} ]")
#
#         if print_color == 'white':
#             print_light_white(f"{STAMP_TIME} {stamp_to_use} {text_working}", line_feed_mode, flush)
#         elif print_color == 'magenta':
#             print_magenta(f"{STAMP_TIME} {text_working}", line_feed_mode, flush)
#         else:
#             config = {
#                 'red': {'red': [stamp_to_use, text_working], 'grey': [STAMP_TIME]},
#                 'yellow': {'yellow': [stamp_to_use], 'white': [text_working], 'grey': [STAMP_TIME]},
#                 'blue': {'blue': [stamp_to_use], 'white': [text_working], 'grey': [STAMP_TIME]},
#                 'green': {'green': [stamp_to_use], 'white': [text_working], 'grey': [STAMP_TIME]},
#                 'grey': {'grey': [STAMP_TIME, stamp_to_use, text_working]},
#                 '': {'grey': [STAMP_TIME, stamp_to_use, text_working]},
#             }.get(print_color, {'grey': [STAMP_TIME, stamp_to_use, text_working]})
#             # 콘솔에는 색상이 적용된 출력
#             # print(get_txt_highlighted(f"{STAMP_TIME} {stamp_to_use} {text_working}", config))
#             clean_text = f"{STAMP_TIME} {stamp_to_use} {text_working}"
#             logging.debug(clean_text)
#
#     except Exception as e:
#         try:
#             # print(f"[ENSURE_PRINTED_FALLBACK] {text_working}")
#             logging.debug(f"[ENSURE_PRINTED_FALLBACK] {text_working}")
#         except Exception:
#             # print(text_working)
#             logging.debug(text_working)
