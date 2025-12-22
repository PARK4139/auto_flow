

def gather_pnxs_empty_at_tree(d_src):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    gather_empty_d(d_working=d_src)
