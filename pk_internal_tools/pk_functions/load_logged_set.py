

# pickle 기반 1회 출력

def load_logged_set(PKL_PATH):
    import pickle

    import os
    if os.path.exists(PKL_PATH):
        with open(PKL_PATH, 'rb') as f_obj:
            return pickle.load(f_obj)
    return set()
