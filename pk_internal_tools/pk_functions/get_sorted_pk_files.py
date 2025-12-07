from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
# @ensure_pk_ttl_cached(ttl_seconds=300, maxsize=16)  # 5분 캐시 활성화, not QC_MODE 모드에서 활성화
def get_excutable_pk_wrappers():
    from pk_internal_tools.pk_objects.pk_directories import d_pk_wrappers
    import os
    from glob import glob

    result = sorted(
        f for f in glob(os.path.join(d_pk_wrappers, "*.py"))
    )
    return result
