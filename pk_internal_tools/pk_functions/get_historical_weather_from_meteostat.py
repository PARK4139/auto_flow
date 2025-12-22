import logging
from datetime import datetime

def get_historical_weather_from_meteostat(lat: float, lon: float, start_date: datetime, end_date: datetime) -> list:
    """
    Meteostat API를 통해 특정 위도/경도의 과거 날씨 데이터를 가져옵니다.
    Args:
        lat: 위도.
        lon: 경도.
        start_date: 시작 날짜 (datetime 객체).
        end_date: 종료 날짜 (datetime 객체).
    Returns:
        list: 일별 과거 날씨 데이터 요약 (딕셔너리 목록) 또는 실패 시 빈 목록.
    """
    try:
        from meteostat import Point, Daily
        # Meteostat Point 객체 생성
        location = Point(lat, lon)

        # 과거 일별 데이터 가져오기
        data = Daily(location, start_date, end_date)
        data = data.fetch()

        if data is not None and not data.empty:
            historical_summary = []
            for index, row in data.iterrows():
                day_data = {
                    "date": index.strftime("%Y-%m-%d"),
                    "temp_avg": row.get("tavg", "N/A"), # 평균 기온
                    "temp_min": row.get("tmin", "N/A"), # 최저 기온
                    "temp_max": row.get("tmax", "N/A"), # 최고 기온
                    "prcp": row.get("prcp", "N/A"),     # 강수량
                    "wspd": row.get("wspd", "N/A"),     # 평균 풍속
                    "pres": row.get("pres", "N/A"),     # 해면 기압
                    "tsun": row.get("tsun", "N/A"),     # 일조 시간
                }
                historical_summary.append(day_data)
            logging.info(f"Meteostat를 통한 과거 날씨 데이터 조회 성공: {len(historical_summary)}일치")
            return historical_summary
        else:
            logging.warning(f"Meteostat 과거 날씨 데이터 파싱 실패: {lat}, {lon}, {start_date}, {end_date}")
            return []
    except Exception as e:
        logging.error(f"Meteostat 과거 날씨 데이터 조회 중 오류 발생: {e}")
        return ""