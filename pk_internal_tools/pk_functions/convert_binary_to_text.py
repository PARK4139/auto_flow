def convert_binary_to_text(binary_f, txt_f):
    # todo : chore : 내가 기대한 대로 fix 안됨. 재시도 필요
    # 바이너리 f을 'rb' 모드로 열고 데이터를 읽습니다.
    with open(binary_f, 'rb') as bin_file:
        binary_data = bin_file.read()

    # 읽은 바이너리 데이터를 'utf-8'로 디코딩하여 텍스트로 변환
    try:
        text_data = binary_data.decode('utf-8')
    except UnicodeDecodeError:
        # utf-8로 디코딩이 실패할 경우 다른 인코딩을 시도
        print(f"Failed to decode with utf-8, trying cp949...")
        text_data = binary_data.decode('cp949', errors='ignore')  # 잘못된 인코딩은 무시

    # 변환된 텍스트 데이터를 텍스트 f로 저장
    with open(txt_f, 'w', encoding='utf-8') as text_file:
        text_file.write(text_data)
