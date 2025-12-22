

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def guide_pk_error_mssage():
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    import logging
    ensure_not_prepared_yet_guided()
