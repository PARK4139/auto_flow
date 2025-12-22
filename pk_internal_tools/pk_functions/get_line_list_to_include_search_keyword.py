from pk_internal_tools.pk_functions.get_list_from_f import get_list_from_f


def get_line_list_to_include_search_keyword(f, search_keywords):
    lines_list = get_list_from_f(f=f)
    target_lines = []

    for line in lines_list:
        if any(keyword in line for keyword in search_keywords):
            target_lines.append(line)

    return target_lines
