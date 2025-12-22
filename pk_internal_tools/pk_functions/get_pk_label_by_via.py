# @ensure_seconds_measured
def get_pk_label_by_via(file_id):
    prompt_label = f"{file_id.split('_via_')[0]}"
    return prompt_label
