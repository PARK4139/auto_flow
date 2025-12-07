

def get_list_aligned_words_gap(working_list, size):
    item_str = get_str_from_list(working_list=working_list, item_connector="%%%LF%%%")
    extracted_words = extract_words(item_str)
    replacements = create_replacements(extracted_words, size=size)
    transformed_data = transform_data(item_str, replacements)
    transformed_data_list = get_list_from_str(item_str=transformed_data, delimiter="%%%LF%%%")
    return transformed_data_list
