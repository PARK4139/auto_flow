from datetime import datetime


def get_test_scenario_result_filename(func_name: str, middle_name: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"test_scenario_{func_name}_{middle_name}_{timestamp}_result.json"
