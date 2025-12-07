def decode_via_pk_system(text_encoded):
    text_encoded = text_encoded.replace("2", "8")
    text_encoded = text_encoded.replace("3", "7")
    text_encoded = text_encoded.replace("4", "6")
    text_encoded = text_encoded.replace("6", "4")
    text_encoded = text_encoded.replace("7", "3")
    text_encoded = text_encoded.replace("8", "2")
    return text_encoded
