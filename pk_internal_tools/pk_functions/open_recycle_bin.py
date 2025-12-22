import requests
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT

from collections import Counter



def open_recycle_bin():
    ensure_command_executed(cmd='explorer.exe shell:RecycleBinFolder')
