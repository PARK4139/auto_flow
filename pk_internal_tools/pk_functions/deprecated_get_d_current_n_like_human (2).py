def deprecated_get_d_current_n_like_human():
    texts_removed_duplicated_element = []
    current_d = ensure_command_executed_like_human_as_admin(rf'echo %cd%')
    for text in current_d:  # remove_duplication
        if text not in texts_removed_duplicated_element:
            if text is not None:
                texts_removed_duplicated_element.append(text)
    current_d = texts_removed_duplicated_element
    current_d = [item.strip() for item in current_d]  # strip_list_element_each
    current_d = [item for item in current_d if item and item.strip()]
    current_d = " ".join(current_d)  # convert_from_list_to_str
    return current_d
