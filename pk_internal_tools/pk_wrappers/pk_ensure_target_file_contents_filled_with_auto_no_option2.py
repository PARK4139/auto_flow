def pk_ensure_target_file_contents_filled_with_auto_no_option2(template_str: str, word_monitored: str, auto_cnt_starting_no=0):
    """
    input
    --------
    -----1--
    ---1----
    ---1----
    -------1
    ouput
    --------
    -----1--
    ---2----
    ---3----
    -------4
    """
    line_splited_by_word_monitored_list = template_str.split(word_monitored)

    line_list_filtered = []
    for index, line_splited_by_word_monitored in enumerate(line_splited_by_word_monitored_list):
        if index != len(line_splited_by_word_monitored_list) - 1:
            line_list_filtered.append(line_splited_by_word_monitored + str(auto_cnt_starting_no))
            auto_cnt_starting_no = auto_cnt_starting_no + 1
        else:
            line_list_filtered.append(line_splited_by_word_monitored)
    lines_new_as_str = "".join(line_list_filtered)
    return lines_new_as_str
