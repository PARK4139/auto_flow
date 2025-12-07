

def convert_lf_to_crlf(f_from, f_to):
    import chardet
    # f의 인코딩 감지
    with open(f_from, 'rb') as infile:
        raw_data = infile.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    # 감지된 인코딩으로 f을 읽고 CRLF로 변환하여 저장
    with open(f_from, 'r', encoding=encoding) as infile:
        lines = infile.readlines()  # Read all lines (LF format)

    with open(f_to, 'w', encoding='utf-8', newline='\r\n') as outfile:
        outfile.writelines(lines)
