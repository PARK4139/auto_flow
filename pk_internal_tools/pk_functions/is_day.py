from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from dataclasses import dataclass
from base64 import b64decode


def is_day(dd):
    from datetime import datetime
    return datetime.today().day == int(dd)
