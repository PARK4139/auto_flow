def is_all_included_in_prompt(prompt, txt_list):
    if all(keyword in prompt for keyword in txt_list):
        return 1
    else:
        return 0
