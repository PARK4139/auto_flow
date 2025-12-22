import logging

from pk_internal_tools.pk_functions.get_pk_interesting_infos import get_pk_interesting_infos
from pk_internal_tools.pk_functions.get_text_cyan import get_text_cyan
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_modes import PkModesForGetPkInterestingInfo  # Import PkModesForGetPkInterestingInfo


def ensure_pk_interesting_infos_printed_2024(
        flags: PkModesForGetPkInterestingInfo = PkModesForGetPkInterestingInfo.ALL
):
    data = get_pk_interesting_infos(
        flags=flags
    )
    logging.info(PK_UNDERLINE)
    logging.info(get_text_cyan(f"현재 정보"))
    #   TODO : 랩퍼적용 get_text_as_title(text) / get_text_pk_theme_colored(text)
    if flags & PkModesForGetPkInterestingInfo.DATE and data.date:
        logging.info(f"날짜정보: {data.date}")
    if flags & PkModesForGetPkInterestingInfo.DAY_OF_WEEK and data.day_of_week:
        logging.info(f"요일정보: {data.day_of_week}")
    if flags & PkModesForGetPkInterestingInfo.TIME and data.time:
        logging.info(f"시간정보: {data.time}")
    if flags & PkModesForGetPkInterestingInfo.LOCATION_WEATHER and data.location:
        logging.info(f"위치정보: {data.location}")
    if flags & PkModesForGetPkInterestingInfo.LOCATION_WEATHER and data.weather:
        logging.info(f"기상정보: {data.weather}")
    if flags & PkModesForGetPkInterestingInfo.STOCK and data.stock_info:
        logging.info(f"주식정보: {data.stock_info}")
