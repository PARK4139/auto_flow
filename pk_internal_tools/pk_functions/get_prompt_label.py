from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

@ensure_seconds_measured
def get_prompt_label(file_id):
    prompt_label = f"{file_id.split('_via_')[0]}"
    return prompt_label