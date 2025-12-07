import traceback

from pk_internal_tools.pk_functions.ensure_magnets_loaded_to_bittorrent import ensure_magnets_loaded_to_bittorrent
from pk_internal_tools.pk_functions.ensure_magnets_collected_from_nyaa_si import ensure_magnets_collected_from_nyaa_si
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_functions.get_selenium_driver import get_selenium_driver
from pk_internal_tools.pk_objects.pk_directories import d_pk_root

if __name__ == "__main__":
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        func_n = get_caller_name()
        while 1:
            key_name = 'animation_title_keyword'
            options = ['Kaijuu']
            animation_title_keyword = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options).strip()

            key_name = 'nyaa_si_supplier'
            options = ['SubsPlease','Erai-raws']
            nyaa_si_supplier = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)

            key_name = 'resolution_keyword'
            options = ['1080', '720']
            resolution_keyword = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options).strip()
            pages = None

            driver = get_selenium_driver(headless_mode=False)
            ensure_magnets_collected_from_nyaa_si(animation_title_keyword=animation_title_keyword, nyaa_si_supplier=nyaa_si_supplier, resolution_keyword=resolution_keyword, driver=driver, pages=pages)

            ensure_magnets_loaded_to_bittorrent()

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
