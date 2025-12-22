from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style

import logging


def parse_addup_from_issues_list_csv():  # todo

    issues_list_csv = rf"{D_DOWNLOADS}/Issues_list.csv"
    f_csv = issues_list_csv
    f_csv = get_pnx_unix_style(f_csv)

    ensure_pnx_opened_by_ext(f_csv)

    logging.debug('line_order=')
    line_order = input(":")
    issue_log_index_data = get_issue_log_index_data_from_f_csv(line_order=line_order, issues_list_csv=issues_list_csv)

    import ipdb
    ipdb.set_trace()

    # 노션 이슈발생 템플릿
    print_template_for_notion_issue_reporting(line_order=line_order, issues_list_csv=issues_list_csv)
