from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made

from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS


def make_project_tree_for_pk_system():
    leaf_directories = [
        D_PK_EXTERNAL_TOOLS
    ]
    for leaf_directory in leaf_directories:
        ensure_pnx_made(pnx=leaf_directory, mode="d")
    leaf_files = [
        # ...
    ]
    for leaf_file in leaf_files:
        ensure_pnx_made(pnx=leaf_file, mode="f")
