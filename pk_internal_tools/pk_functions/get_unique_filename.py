def get_unique_filename(base, d_working):
    import os
    count = 1
    candidate = f"{base}.py"
    while os.path.exists(os.path.join(d_working, candidate)):
        candidate = f"{base}_DUPLICATED_FUNCTION_{count}.py"
        count += 1
    return candidate
