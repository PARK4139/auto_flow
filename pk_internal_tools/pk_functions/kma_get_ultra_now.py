import httpx
from datetime import datetime, timedelta, timezone

# KST definition (assuming it's a common constant)
KST = timezone(timedelta(hours=9))

def kma_get_ultra_now(x, y, service_key):
    """초단기실황(getUltraSrtNcst) – 관측 기반 '지금' 값"""
    base = datetime.now(KST)
    base_date = base.strftime("%Y%m%d")
    base_time = (base - timedelta(minutes=40)).strftime("%H%M")
    url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
    params = {"serviceKey": service_key, "pageNo": 1, "numOfRows": 1000, "dataType": "JSON",
              "base_date": base_date, "base_time": base_time, "nx": x, "ny": y}
    r = httpx.get(url, params=params, timeout=10)
    r.raise_for_for_status()
    return r.json()