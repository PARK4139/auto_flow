from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
from pk_internal_tools.pk_functions.ensure_list_written_to_f_with_delimiter import ensure_list_written_to_f_with_delimiter


def set_values_to_historical_file(f_historical, values):
    ensure_pnx_made(pnx=f_historical, mode='f')
    ensure_list_written_to_f_with_delimiter(f=f_historical, working_list=values, mode="w")