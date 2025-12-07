from pk_internal_tools.pk_functions.get_list_deduplicated import get_list_deduplicated
from pk_internal_tools.pk_functions.get_list_without_none import get_list_without_none

def get_list_without_none_and_duplicates(working_list):
    working_list = get_list_deduplicated(working_list)
    working_list = get_list_without_none(working_list)
    return working_list