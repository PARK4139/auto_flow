def is_prompt_in_text(prompt, text):
    if prompt.lower() in text.lower():
        return 1
    return 0
