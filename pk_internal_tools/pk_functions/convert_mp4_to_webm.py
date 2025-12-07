import logging

from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE


def convert_mp4_to_webm(src):
    import os

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    '''테스트 필요'''

    logging.debug(f'from : {src}')
    file_edited = f'{os.path.splitext(os.path.basename(src))[0]}.webm'
    logging.debug(f'to   : {file_edited}')

    path_started = os.getcwd()
    os.system("chcp 65001 >NUL")
    os.system('mkdir storage >NUL')
    os.chdir('storage')
    os.system(f'"{F_FFMPEG_EXE}" -i "{src}" -f webm -c:v libvpx -b:v 1M -acodec libvorbis "{file_edited}" -hide_banner')
    os.chdir(path_started)
