def translate_eng_to_kor_via_googletrans(text: str):  # 수정할것 update 되었다는데 googletrans 업데이트 해보자
    if not is_internet_connected_2025_10_21():
        raise
    # translater=Translator()
    # text_translated=translater.translate([text_eng.split(".")], dest='ko')
    # for translation in text_translated:
    #     print(translation.origin, ' ->> ', translation.text)
    # debug_as_gui(context=text_translated, is_app_instance_mode=True)

    # naver papago api 서비스는 2024 년 종료가 된다...
    # translator=Translator(service_urls=['translate.google.com', 'translate.google.co.kr'],user_agent='Mozilla/5.0 (Windows NT 10.0;  x64; Win64)', time_limit=random.randint(0, 99) / 10)
    # tmp=translator.translate(text, src="ko", dest="en")
    # print(rf'tmp : {tmp}')
    # print(rf'type(tmp) : {type(tmp)}')
    # print(rf'len(tmp) : {len(tmp)}')
    # pk_ipdb.set_trace()

    # 한수훈 씨가 만든 모듈 같다. 무료이다. 단, 안정성 보장은 안되며, google 로 부터 ip가 차단이 될 수 있다.
    # 단일 텍스트의 최대 글자수 제한은 15k입니다. 이거 로직으로 제한 하도록.
    # 약간 시간적인 트릭도 넣을 것
    # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
    # translator.translate('안녕하세요.', dest='ja')
    # <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
    # translator.translate('veritas lux mea', src='la')
    # <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>
    # 2023 12 31 01 11 현재시각기준 안된다

    # translator=Translator()
    # translator.detect('이 문장은 한글로 쓰여졌습니다.')
    # # <Detected lang=ko confidence=0.27041003>
    # translator.detect('この文章は日本語で書かれました。')
    # # <Detected lang=ja confidence=0.64889508>
    # translator.detect('This sentence is written in English.')
    # # <Detected lang=en confidence=0.22348526>
    # translator.detect('Tiu frazo estas skribita en Esperanto.')
    # # <Detected lang=eo confidence=0.10538048>
