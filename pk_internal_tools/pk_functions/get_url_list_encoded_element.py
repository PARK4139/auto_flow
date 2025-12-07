def get_url_list_encoded_element(working_list):
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    import urllib.parse

    logging.debug(f'''working_list={working_list}  ''')
    return [urllib.parse.quote(item) for item in working_list]
