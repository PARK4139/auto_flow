

def save_logged_set(logged_set, PKL_PATH):
    import pickle

    with open(PKL_PATH, 'wb') as f_obj:
        pickle.dump(logged_set, f_obj)
