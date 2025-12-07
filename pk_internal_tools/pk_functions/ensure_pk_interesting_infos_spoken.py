import logging
from pk_internal_tools.pk_functions.get_pk_interesting_infos import get_pk_interesting_infos
from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForGetPkInterestingInfo # Import SetupOpsForGetPkInterestingInfo

def ensure_pk_interesting_infos_spoken(
    flags: SetupOpsForGetPkInterestingInfo = SetupOpsForGetPkInterestingInfo.ALL
):
    """
    현재 정보를 선택적으로 수집하여 음성으로 알려줍니다.
    인자 없이 호출하면 모든 정보를 말합니다.
    """
    # 효율성을 위해 말할 정보만 가져오도록 get_pk_interesting_infos에 플래그를 전달합니다.
    data = get_pk_interesting_infos(
        flags=flags
    )

    # 음성으로 출력할 문장 생성
    speech_parts = []
    if flags & SetupOpsForGetPkInterestingInfo.DATE and data.date and data.day_of_week:
        speech_parts.append(f"오늘은 {data.date} {data.day_of_week}")
    elif flags & SetupOpsForGetPkInterestingInfo.DATE and data.date:
        speech_parts.append(f"오늘은 {data.date}")
        
    if flags & SetupOpsForGetPkInterestingInfo.TIME and data.time:
        speech_parts.append(f"현재 시간은 {data.time}입니다")
        
    if flags & SetupOpsForGetPkInterestingInfo.LOCATION_WEATHER and data.location:
        speech_parts.append(f"현재 계신 곳은 {data.location}이며")
        
    if flags & SetupOpsForGetPkInterestingInfo.LOCATION_WEATHER and data.weather:
        speech_parts.append(f"날씨는 {data.weather}입니다")
        
    if flags & SetupOpsForGetPkInterestingInfo.STOCK and data.stock_info:
        speech_parts.append(f"주식 정보, {data.stock_info}입니다")

    # 쉼표로 각 부분을 연결하여 자연스러운 멈춤 효과
    full_speech = ", ".join(filter(None, speech_parts))

    if full_speech:
        ensure_spoken(full_speech, wait=True) # 음성이 끝날 때까지 대기
    else:
        ensure_spoken("알려드릴 정보가 없습니다.", wait=True)