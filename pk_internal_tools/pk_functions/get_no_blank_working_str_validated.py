import logging


def get_no_blank_text_working_validated(text_working):
    name = text_working.strip()
    if not name:
        logging.debug("blank text is not allowed")
        raise ValueError("text is blank")
    return name
