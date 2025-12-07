from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE

import logging


def convert_mp4_to_flac(pnx):
    import inspect
    import os
    import subprocess

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    '''테스트 필요'''

    os.system("chcp 65001 >NUL")
    logging.debug(f'from : {pnx}')
    file_edited = f'{os.path.splitext(os.path.basename(pnx))[0]}.flac'
    logging.debug(f'to   : {file_edited}')

    path_started = os.getcwd()

    ffmpeg_exe = F_FFMPEG_EXE
    destination = 'storage'
    try:
        os.makedirs(destination)
    except Exception as e:
        pass
    os.chdir(destination)
    logging.debug(f'"{ffmpeg_exe}" -i "{pnx}" -c:a flac "{file_edited}"        를 수행합니다.')
    subprocess.check_output(f'"{ffmpeg_exe}" -i "{pnx}" -c:a flac "{file_edited}"', shell=True)

    os.chdir(path_started)
