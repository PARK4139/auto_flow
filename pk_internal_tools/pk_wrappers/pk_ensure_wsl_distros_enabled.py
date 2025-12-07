from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForPkWirelessTargetController
from pk_internal_tools.pk_objects.pk_wireless_target_controller import PkWirelessTargetController

if __name__ == "__main__":

    import traceback
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        tm = PkWirelessTargetController(identifier=PkDevice.undefined, setup_op=SetupOpsForPkWirelessTargetController.INITIALIZE_NONE)
        for distro_name in tm.get_wsl_distro_names_installed():
            tm.ensure_wsl_distros_enabled(distro_name)
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
