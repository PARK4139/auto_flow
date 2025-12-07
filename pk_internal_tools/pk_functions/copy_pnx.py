import zipfile

import win32com.client
import uuid
import time
import random
import cv2
import clipboard
from PySide6.QtWidgets import QApplication
from pynput import mouse
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from fastapi import HTTPException
from enum import Enum
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000


def copy_pnx(pnx_woking, d_dst, with_overwrite=0):
    if with_overwrite == 1:
        copy_pnx_with_overwrite(pnx_woking, d_dst)
    elif with_overwrite == 0:
        copy_pnx_without_overwrite(pnx_woking, d_dst)
