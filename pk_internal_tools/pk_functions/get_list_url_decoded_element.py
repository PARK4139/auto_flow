

def get_list_url_decoded_element(working_list):
    import urllib.parse
    return [urllib.parse.unquote(item) for item in working_list]
