from pk_internal_tools.pk_functions.ensure_drag_changed_printed import get_list_striped_element
from pk_internal_tools.pk_functions.get_selenium_driver import get_selenium_driver
from pk_internal_tools.pk_functions.get_list_deduplicated import get_list_deduplicated
from pk_internal_tools.pk_functions.get_list_from_f import get_list_from_f
from pk_internal_tools.pk_functions.get_list_removed_element_empty import get_list_removed_empty
from pk_internal_tools.pk_functions.get_list_url_decoded_element import get_list_url_decoded_element
from pk_internal_tools.pk_functions.is_internet_connected_2025_10_21 import is_internet_connected_2025_10_21
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
import logging
from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list


def collect_magnet_set_from_nyaa_si(search_keyword=None, driver=None, via_f_txt=False, via_input=False):
    import inspect

    from urllib.parse import unquote, urlparse, parse_qs

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    if not is_internet_connected_2025_10_21():
        raise

    from pk_internal_tools.pk_objects.pk_directories import d_pk_config
    f = d_pk_config / 'pk_magnets.txt'
    ensure_pnx_made(pnx=f, mode="f")
    # answer = ensure_value_completed(key_name=f'can i open {get_nx(f)} (o/x)=', options=['o', 'x'])
    # if is_os_windows():
    #     if answer == 'o':
    #         ensure_command_executed(cmd=rf'explorer "{get_pnx_windows_style(f)}"', mode="a")
    # else:
    #     logging.debug(rf'''{get_pnx_unix_style(f)}  ''')
    #     pass # todo

    from pk_internal_tools.pk_objects.pk_directories import d_pk_config
    f_func_n_txt = d_pk_config / f'{func_n}.txt'
    ensure_pnx_made(pnx=f_func_n_txt, mode="f")
    # window_title_seg = get_nx(f_func_n_txt)

    # include_elements_all = ['1080']
    # include_elements_any = ['SubsPlease', 'Moozzi']
    # exclude_elements_all = ["[New-raws]", "[LoliHouse]", "[Erai-raws]", "[Koi-Raws]", '[EMBER]', '[Lilith-Raws]', '[Yameii]', '[ASW]', '[shincaps]', '[AsukaRaws]']
    magnets_set = set()
    search_keyword_list = []

    ensure_pnx_made(pnx=rf'historical_{func_n}.txt', mode='f')
    historical_search_keyword_list = get_historical_list(f=rf'historical_{func_n}.txt')
    options = ['', '1080 [Batch]'] + historical_search_keyword_list
    search_keyword = ensure_value_completed(key_name='search_keyword', options=options)
    search_keyword = search_keyword.strip()
    ensure_list_written_to_f(f=rf'historical_{func_n}.txt', working_list=[search_keyword] + historical_search_keyword_list,
                             mode="w")

    search_keyword = search_keyword.strip()
    search_keyword_list.append(search_keyword)

    # if via_f_txt:
    #     logging.debug(f'''mode is via_f_txt mode''')
    #     logging.debug(f'''via_f_txt={via_f_txt}  ''')
    #     search_keyword_list = get_list_from_f(f=f_func_n_txt)
    #     search_keyword_list = get_list_removed_element_contain_prompt(working_list=search_keyword_list, prompt="#")
    #     search_keyword_list = get_list_replaced_element_from_str_to_str(working_list=search_keyword_list, from_str='pk_ani ', to_str='')
    #     search_keyword_list = get_list_replaced_element_from_str_to_str(working_list=search_keyword_list, from_str='pk_movie ', to_str='')
    #     search_keyword_list = get_list_replaced_element_from_str_to_str(working_list=search_keyword_list, from_str='pk_music ', to_str='')

    logging.debug(f'''len(search_keyword_list)={len(search_keyword_list)}  ''')
    # ensure_iterable_log_as_vertical(item_iterable=search_keyword_list, item_iterable_n="search_keyword_list")

    search_keyword_list = get_list_striped_element(working_list=search_keyword_list)
    search_keyword_list = get_list_deduplicated(working_list=search_keyword_list)

    if driver is None:
        driver = get_selenium_driver(headless_mode=False)

    nyaa_si_supplier = ensure_value_completed(key_name='nyaa_si_supplier', options=['SubsPlease', '', 'Erai-raws'])
    magnets_set = magnets_set | get_magnets_set_from_nyaa_si(nyaa_si_supplier=nyaa_si_supplier,
                                                             search_keyword=search_keyword, driver=driver)

    magnets_set_filtered = set()

    positive_filter_keywords = ensure_value_completed(key_name='positive_filter_keywords', options=['1080'])
    for magnet in magnets_set:
        decoded_magnet = unquote(magnet)
        parsed = urlparse(decoded_magnet)
        qs = parse_qs(parsed.query)
        dn = qs.get('dn', [''])[0]
        if all(keyword in dn for keyword in positive_filter_keywords):
            magnets_set_filtered.add(magnet)
    magnets_set = magnets_set_filtered
    logging.debug(f'''len(magnets_set)={len(magnets_set)}  ''')

    magnets_set_filtered = set()
    negative_filter_keywords = [
        "Yami Shibai 8",
        "Yami Shibai 9",
        "360p",
        "720p",
        "480p",
    ]
    ensure_iterable_log_as_vertical(iterable_data=negative_filter_keywords, iterable_data_n="negative_filter_keywords")
    for magnet in magnets_set:
        decoded_magnet = unquote(magnet)
        parsed = urlparse(decoded_magnet)
        qs = parse_qs(parsed.query)
        dn = qs.get('dn', [''])[0]
        if not any(keyword in dn for keyword in negative_filter_keywords):
            magnets_set_filtered.add(magnet)
    magnets_set = magnets_set_filtered

    from pk_internal_tools.pk_objects.pk_directories import d_pk_config
    f = d_pk_config / 'pk_magnets.txt'
    magnets_list = get_list_url_decoded_element(magnets_set)
    magnets_list = [magnet for magnet in
                    sorted(magnets_list, key=lambda magnet: magnet.split("&dn=")[1] if "&dn=" in magnet else "")]
    ensure_list_written_to_f(f=f, working_list=magnets_list, mode="a")

    # magnets 중복remove
    magnets_list = get_list_from_f(f=f)
    magnets_list = get_list_striped_element(working_list=magnets_list)
    magnets_list = get_list_removed_empty(working_list=magnets_list)
    magnets_list = get_list_deduplicated(working_list=magnets_list)
    ensure_list_written_to_f(f=f, working_list=magnets_list, mode="w")

    # search_keyword_list 목록추가, search_keyword_list 중복remove
    search_keyword_list = get_list_from_f(f=f_func_n_txt) + search_keyword_list
    search_keyword_list = get_list_striped_element(working_list=search_keyword_list)
    search_keyword_list = get_list_removed_empty(working_list=search_keyword_list)
    search_keyword_list = get_list_deduplicated(working_list=search_keyword_list)
    ensure_list_written_to_f(f=f_func_n_txt, working_list=search_keyword_list, mode="w")
