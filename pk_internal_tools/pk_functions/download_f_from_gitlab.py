def download_f_from_gitlab(f_nx_remote_src, d_local_dst, gitlab_repo_url):
    """
        TODO
    """
    import os
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    while 1:
        os.chdir(d_local_dst)
        ensure_command_executed(cmd=f'git init')
        cmd = rf"git remote add -f origin http://{gitlab_repo_url}"
        std_list = ensure_command_executed(cmd=cmd)

        ensure_command_executed(cmd=f'git fetch')
        ensure_command_executed(cmd=f'git checkout origin/main -- {f_nx_remote_src}')
        # ensure_command_executed(cmd = f'git remote remove origin') # 로그인 실패시 # todo

        # todo
        # f_remote_src = 현재 디렉토리의 + f_nx_remote_src
        # if not does_pnx_exist(pnx=f_remote_src):
        #     continue
        # if does_pnx_exist(pnx=f_remote_src):
        #     break
