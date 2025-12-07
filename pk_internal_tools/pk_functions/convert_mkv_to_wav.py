



def convert_mkv_to_wav(file_mkv):
    ensure_command_executed_like_human_as_admin(rf'ffmpeg -i "{file_mkv}" -ab 160k -ac 2 -ar 44100 -vn {get_pn(file_mkv)}.wav')
