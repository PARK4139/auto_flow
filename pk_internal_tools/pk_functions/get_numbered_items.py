from typing import List

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_numbered_items(items: List):
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    import logging
    numbered_prompts = []
    for i, prompt in enumerate(items):
        numbered_prompts.append(f"{i + 1}. {prompt}")
        if QC_MODE:
            # logging.debug(f"{i + 1}. {prompt}")
            pass
    return numbered_prompts
