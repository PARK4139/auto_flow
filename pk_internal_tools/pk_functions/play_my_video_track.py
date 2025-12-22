from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_files import F_VIDEO_POTPLAYER64_DPL
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed


def play_my_video_track():
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    potplayer_play_list_folder_path = D_PK_WORKING
    ensure_pnx_made(pnx=potplayer_play_list_folder_path, mode='f')
    ensure_command_executed(cmd=rf'explorer "{F_VIDEO_POTPLAYER64_DPL}" ')
