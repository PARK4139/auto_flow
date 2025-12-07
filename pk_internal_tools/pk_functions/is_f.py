

def is_f(pnx):
    import os
    if os.path.isfile(pnx):
        return 1
    else:
        return 0
