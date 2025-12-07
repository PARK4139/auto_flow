from pk_internal_tools.pk_functions.get_d_working_in_python import get_pwd_in_python
from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once

ensure_pk_colorama_initialized_once()
pwd = get_pwd_in_python()
print(pwd)
