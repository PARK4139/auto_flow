import logging


def ensure_driver_navigates_to_url_and_switches_to_new_tab_and_wait_loaded(url, driver):
    import json

    ensure_driver_navigates_to_url_and_switches_to_new_tab(url=url, driver=driver)

    # 네트워크 로그 가져오기
    logs = driver.get_log("performance")
    events = [json.loads(entry["message"])["message"] for entry in logs]

    # 가장 늦게 로드된 네트워크 요청 찾기
    latest_time = 0
    latest_url = None

    for event in events:
        if event["method"] == "Network.responseReceived":
            response_time = event["params"]["timestamp"]
            request_url = event["params"]["response"]["url"]

            if response_time > latest_time:
                latest_time = response_time
                latest_url = request_url

    logging.debug(f"가장 늦게 로드된 요소 URL: {latest_url}")
    logging.debug(f"로드 완료 시간: {latest_time}")
    return latest_url, latest_time
