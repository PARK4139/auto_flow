def here(item_str=None):
    import logging
    if item_str is None:
        item_str = ''
    logging.debug(rf"{str(str(item_str) + ' ') * 242:.100} here!")
