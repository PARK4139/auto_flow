from pathlib import Path


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def save_d_to_f(d, f):
    with open(f, "w", encoding='utf-8') as f_obj:
        d = Path(d)
        f_obj.write(d)
        if QC_MODE:
            logging.debug(f'''d={d} %%%FOO%%%''')
