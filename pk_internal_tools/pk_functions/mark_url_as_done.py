from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


def mark_url_as_done(f, original_url):
    #
    import os
    if not os.path.exists(f):
        return

    with open(f, 'r', encoding='utf-8') as r:
        lines = r.readlines()

    changed = False
    new_lines = []
    for line in lines:
        line_strip = line.strip()
        if line_strip == original_url and not line_strip.startswith("#"):
            new_lines.append(f"# {line_strip}\n")
            changed = True
        else:
            new_lines.append(line)

    if changed:
        with open(f, 'w', encoding='utf-8') as w:
            w.writelines(new_lines)
        ensure_window_to_front(get_nx(f))
