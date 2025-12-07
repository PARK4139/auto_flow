

def ensure_target_config_right (target_device_data, remote_device_target_config):
    if target_device_data.target_device_type == 'no':
        # ensure_target_config_py_debug_true
        # config.py 에서 마지막 10줄을 가져오고, 그 아래에서 특정항목의 debug=True를 설정확인
        # run_container -b 옵션으로 container에 접속이 가능
        todo('%%%FOO%%%')
    if target_device_data.target_device_type == 'nx':
        # ai_framework config custom
        # vi ~/works/remote_release/cam_merge_f.cfg
        # vi cam_merge_f.cfg
        # vi cam_merge_lf.cfg
        # vi cam_merge_rf.cfg
        # vi cfg_pack_merge_front.cfg
        # vi env_merge_front.cfg
        todo('%%%FOO%%%')
    if target_device_data.target_device_type == 'xc':
        # 192.168.2.114/~/works/ai_framework/config/env_f.cfg
        # 192.168.2.114/~/works/ai_framework/config/env_lf.cfg
        # 192.168.2.114/~/works/ai_framework/config/env_rf.cfg

        todo('%%%FOO%%%')
