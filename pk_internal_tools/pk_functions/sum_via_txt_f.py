from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT

import logging


def sum_via_txt_f():
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    from pk_internal_tools.pk_objects.pk_directories import D_PK_CONFIG
    f_func_n_txt = D_PK_CONFIG / f'{func_n}.txt'
    ensure_pnx_made(pnx=f_func_n_txt, mode="f")
    ensure_pnx_opened_by_ext(f_func_n_txt)

    texts = get_list_from_f(f=f_func_n_txt)
    # texts=texts.split("\n")
    texts = get_list_striped_element(working_list=texts)
    total = 0
    for text in texts:
        if text is not None:
            total += int(text.strip())
    [logging.debug(item) for item in texts]
    logging.debug(f'''len(texts)={len(texts)}''')
    logging.debug(f'''total={total}''')
