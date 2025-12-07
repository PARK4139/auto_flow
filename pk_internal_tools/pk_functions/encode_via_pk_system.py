

def encode_via_pk_system(text_plain):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    text_plain = text_plain.replace("8", "2")
    text_plain = text_plain.replace("7", "3")
    text_plain = text_plain.replace("6", "4")
    text_plain = text_plain.replace("4", "6")
    text_plain = text_plain.replace("3", "7")
    text_plain = text_plain.replace("2", "8")
    return text_plain
