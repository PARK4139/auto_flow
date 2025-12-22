from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_police_block_printed(block_text: any):
    import logging
    POLICE_LINE = f"{str(block_text)} " * 22
    logging.debug(POLICE_LINE)
    logging.debug(POLICE_LINE)
    logging.debug(POLICE_LINE)
    logging.debug(POLICE_LINE)
    logging.debug(POLICE_LINE)
