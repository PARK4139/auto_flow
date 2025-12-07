
def get_list_removed_element_contain_prompt(working_list, prompt):
    return [item for item in working_list if prompt not in item]
