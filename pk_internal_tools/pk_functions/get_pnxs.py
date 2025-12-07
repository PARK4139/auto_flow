def get_pnxs(with_walking: bool = False, filtered=None, d_working=None):
    from pk_internal_tools.pk_functions.is_d import is_d
    import os
    if with_walking:
        if d_working is None:
            d_working = os.getcwd()

        f_list = []
        d_list = []

        for root, d_nx_list, file_nxs in os.walk(d_working):
            d = os.path.abspath(root)
            d_list.append(d)

            for f_nx in file_nxs:
                f = os.path.join(root, f_nx)
                f_list.append(f)

            # 하위 d 탐색을 원하지 않는 경우
            if filtered == "d":  # d만 원하면 아래 항목에서 멈춤
                del d_nx_list[:]

        # 원하는 mode에 따라 결과 반환
        if filtered == "f":
            pnx_list = f_list
        elif filtered == "d":
            pnx_list = d_list
        else:
            pnx_list = f_list + d_list

        # 출력제한
        print_limit = 100000000
        if len(f_list) <= print_limit:
            # logging.debug(f'''files={files}''')
            # logging.debug(f'''directories={directories}''')
            pass

        return pnx_list
    elif not with_walking:
        import os
        if d_working is None:
            d_working = os.getcwd()

        # 절대경로로 변환
        d_working = os.path.abspath(d_working)

        pnx_nxs = os.listdir(d_working)
        f_list = []
        d_list = []

        for pnx_nx in pnx_nxs:
            pnx = os.path.join(d_working, pnx_nx)  # 절대경로로 결합
            if is_d(pnx):
                d_list.append(pnx)  # d의 절대경로 추가
            else:
                f_list.append(pnx)  # f의 절대경로 추가

        # 원하는 mode에 따라 결과 반환
        if filtered == "f":
            pnx_list = f_list
        elif filtered == "d":
            pnx_list = d_list
        else:
            pnx_list = f_list + d_list
        return pnx_list
    return None
