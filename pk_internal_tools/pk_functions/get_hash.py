from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_hash(text : str):
    # text = f"담고싶은|것들을|담는다|예를 들어서"
    # TODO : 검증필요
    import hashlib
    key_hash = hashlib.md5(text.encode()).hexdigest()
    return key_hash
