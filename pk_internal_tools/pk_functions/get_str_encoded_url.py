def get_str_encoded_url(text_working):
    import urllib
    from urllib.parse import quote
    return urllib.parse.quote(f"{text_working}")
