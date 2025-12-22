

def ensure_aifw_running (target_device_data, remote_device_target_config):
    if target_device_data.target_device_type == 'no':
        while 1:
            if not is_aifw_docker_container_running():
                run_target_aifw_docker_container (target_device_data, remote_device_target_config)
                if is_aifw_docker_container_running():
                    break
    elif target_device_data.target_device_type == 'nx':
        # cd ~/works/ai_framework/bin
        # ./TODO_component_front_launcher cfg_pack_merge_front.cfg
        # ./TODO_component_merge_launcher cfg_pack_merge_front.cfg
        pass
    elif target_device_data.target_device_type == 'xc':
        # exec ai_framework
        # vscode/Remote Explorer/SSH/192.168.2.114/~/works/ai_framework/bin
        # vscode/Remote Explorer/SSH/192.168.2.114/~/works/ai_framework/bin ./TODO_component_front_launcher cfg_pack_merge_front.cfg
        # vscode/Remote Explorer/SSH/192.168.2.114/~/works/ai_framework/bin ./TODO_component_merge_launcher cfg_pack_merge_front.cfg
        pass
