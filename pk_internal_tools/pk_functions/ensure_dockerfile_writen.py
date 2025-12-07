

def ensure_dockerfile_writen(f, f_dockerfile_script_list):
    f_dockerfile_script_list = get_list_added_suffix_each_element(working_list=f_dockerfile_script_list, suffix='\n')
    ensure_pnx_made(pnx=f, mode='f', script_list=f_dockerfile_script_list)
