def get_values_sanitize_for_cp949(text):
    # 유사 문자 수동 치환
    replacements = {
        '–': '-',  # EN DASH
        '—': '-',  # EM DASH
        '“': '"', '”': '"',
        '‘': "'", '’': "'",
        '…': '...', '•': '*',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text
    # return text.encode('cp949', errors='replace').decode('cp949')
    # return text.encode('cp949', errors='replace').decode('cp949')


