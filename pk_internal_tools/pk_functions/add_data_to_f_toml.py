#!/usr/bin/env python3


import os

import toml

from pk_internal_tools.pk_objects.pk_encodings import PkEncoding


def add_data_to_f_toml(f_toml, data_new):
    """TOML 파일에 새로운 데이터 추가/병합"""

    # TOML 파일이 존재하지 않으면 새로 생성
    if not os.path.exists(f_toml):
        toml_data = {}
    else:
        # TOML 파일 읽기
        with open(file=f_toml, mode="r", encoding=PkEncoding.UTF8.value) as f:
            toml_data = toml.load(f)

    # 새로운 데이터 추가/병합
    for key, value in data_new.items():
        if key in toml_data:
            # 기존 데이터와 병합
            if isinstance(toml_data[key], dict) and isinstance(value, dict):
                toml_data[key].update(value)
            else:
                # 딕셔너리가 아니면 덮어쓰기
                toml_data[key] = value
        else:
            # 새로운 키 추가
            toml_data[key] = value

    # TOML 파일 다시 저장
    with open(file=f_toml, mode="w", encoding=PkEncoding.UTF8.value) as f:
        toml.dump(toml_data, f)
