def create_replacements(extracted_words, size):
    unique_words = set(extracted_words)
    replacements = {f'{word}': f'{word:{size}s}' for word in unique_words}
    return replacements
