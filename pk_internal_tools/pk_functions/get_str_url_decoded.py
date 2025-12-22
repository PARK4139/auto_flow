def get_str_url_decoded(text_working):
    import urllib
    from urllib.parse import quote
    return urllib.parse.unquote(text_working)
