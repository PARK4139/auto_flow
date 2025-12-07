def ensure_api_key_return(api_key_id):
    import json
    import os

    import logging

    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    api_key_id = rf"API_KEY_OF_{api_key_id}".upper()

    if os.getenv(api_key_id):
        return os.getenv(api_key_id)

    # 설정 파일에서 확인
    config_dir = os.path.join(os.path.expanduser("~"), ".pk_system")
    config_file = os.path.join(config_dir, f"{api_key_id}.json")

    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                key = config.get('api_key')
                if key:
                    os.environ[api_key_id] = key
                    logging.debug(f"api key is loaded from config file({config_file})")
                    return key
        except Exception as e:
            logging.debug(f"️ 설정 파일 읽기 실패: {e}")

    # 사용자 입력으로 설정
    try:
        logging.debug(f"need api key({api_key_id})")
        key = input(f"{PkTexts.API_KEY_INPUT}=").strip()

        if key:
            # 설정 파일에 저장
            os.makedirs(config_dir, exist_ok=True)
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump({'api_key': key}, f, ensure_ascii=False, indent=2)

            os.environ[api_key_id] = key
            logging.debug("api key is set")
            return key
        else:
            logging.debug("api key가 입력되지 않았습니다")
            return None

    except Exception as e:
        logging.debug(f"api key 설정 실패: {e}")
        return None
