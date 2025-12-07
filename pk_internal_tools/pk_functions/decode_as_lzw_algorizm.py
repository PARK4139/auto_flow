

def decode_as_lzw_algorizm(encrypted_text):
    import zlib

    return zlib.decompress(encrypted_text.decode('utf-8'))
