

def get_pk_key_from_f(f):
    from pathlib import Path
    f = Path(f)
    with open(f, "r", encoding="utf-8") as f:
        key_byte = f.read().strip().encode()  # 문자열을 bytes로
        return key_byte
