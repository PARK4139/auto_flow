import shutil
import pywintypes

import nest_asyncio
from tkinter import UNDERLINE
from PySide6.QtWidgets import QApplication


from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
import logging

from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING

from fastapi import HTTPException
from datetime import timedelta
from datetime import datetime
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
import logging


def get_deleted_f_list(previous_state, current_state):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    return DataStructureUtil.get_elements_that_list1_only_have(list1=previous_state, list2=current_state)
