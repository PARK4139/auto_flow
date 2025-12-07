from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def copy_pnx_from_local_os_to_remote_os_via_rsync(d_pnx):
    # todo
    import os
    import shutil
    import traceback
    from dirsync import sync

    if not is_internet_connected_2025_10_21():
        raise
    try:

        d_pnx = d_pnx
        d_pnx_new = rf"{d_pnx}_sync"
        logging.debug(f'''d_pnx_new={d_pnx_new}  ''')

        # 기존 작업 d가 없는 경우
        if not os.path.exists(d_pnx_new):
            shutil.copytree(d_pnx, d_pnx_new)
        else:
            # remove_target_parmanently(DIRSYNC_LOG)
            # # logging 설정 및 DIRSYNC_LOG 생성
            # logging.basicConfig(filename=DIRSYNC_LOG, level=logging.DEBUG, filemode='w', encoding=Encoding.UTF8.value)
            # dirsync_logger=logging.getLogger('dirsync')

            # result_sync=sync(sourcedir=pnx_todo, targetdir=pnx_todo_new, action='sync', verbose=True, logger=dirsync_logger) #success
            # result_sync=sync(sourcedir=pnx_todo, targetdir=pnx_todo_new, action="sync", options=["--purge", "--verbose", "--force"], logger=dirsync_logger)
            result_sync = sync(sourcedir=d_pnx, targetdir=d_pnx_new, action="sync",
                               options=["--purge", "--verbose", "--force"])
            # sync(sourcedir=pnx_todo_new, targetdir=pnx_todo , action='sync',verbose=True , logger=dirsync_logger)  # 양방향 으로 로컬동기화d를 만드려면 sync() 코드를 추가하여 sync() 함수가 총 2개가 targetdir 간에 sourcedir 서로 자리바뀌어 있도록 작성
            # if result_sync:
            #     # DIRSYNC_LOG 내용 가져오기
            #     if os.path.exists(DIRSYNC_LOG):
            #         lines=get_lines_of_file(DIRSYNC_LOG)[-4:-1]
            #         lines=[sample.strip() for sample in lines]
            #         for sample in lines:
            #             # print(translate_eng_to_kor_via_googletrans(sample))
            #             print_ment_light_white(rf'sample : {sample}')
            #         print_ment_light_white(rf'len(lines) : {len(lines)}')
            #         remove_target_parmanently(DIRSYNC_LOG)
            #         lines=[x for x in lines if x.strip("\n")]  # 리스트 요소 "" remove,  from ["", A] to [A]       [""] to []
            #         # speak_ments(f"타겟의 동기화가 성공 되었습니다", sleep_after_play=0.65, thread_join_mode=True)
            #         print_ment_success("타겟동기화 성공")
            #         PkGui.pop_up_as_complete(title_="작업성공보고", ment=f"타겟의 동기화가 성공 되었습니다\n{pnx_todo_new}", auto_click_positive_btn_after_seconds=1)
            logging.debug("타겟동기화 성공")
    except:
        logging.debug("타겟동기화 실패")
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")

    # sources=[r'C:\Users\seon\Desktop\오리지널',
    #            r'C:\Users\seon\Desktop\오리지널2',
    #            r'C:\Users\seon\Desktop\오리지널3']
    # pnxs=[r'C:\Users\seon\Desktop\테스트',
    #            r'C:\Users\seon\Desktop\테스트2',
    #            r'C:\Users\seon\Desktop\테스트3']
    # total=dict(zip(sources, pnxs))
    # for source, target in total.items():
    #     sync(sourcedir=source, targetdir=target, action='sync', verbose=True, purge=True, create=True,  delete=True, update=True)  # 이것이 sync() default 파라미터들이다.
    #     sync(sourcedir=source, targetdir=target, action='sync', verbose=True, purge=True, create=True,  delete=True, update=True)  # purge=True 이면 targetdir 에 이물질 같은 f이 있으면 삭제를 합니다, delete=False 이면 어떻게 되는거지? # verbose=True 이면 상세설명출력

    # 윈도우 d를 WSL 경로로 변환
    # try:
    #     server_time=get_pk_time_2025_10_20_1159('%Y_%m_%d_%H_%M_%S_%f')
    #     pnx_todo=rf"/mnt/c/{pnx_todo}" \ 에서 / 로 바꿔야한다
    #     # pnx_todo_new=rf"/mnt/c/{pnx_todo}_{server_time}"
    #     pnx_todo_new=rf"/mnt/c/{pnx_todo}_sync"
    #     cmd=f"rsync -avz {pnx_todo} {pnx_todo_new}"
    #     print(cmd)
    #     subprocess.call(cmd, shell=True)
    # except:
    #     pass
