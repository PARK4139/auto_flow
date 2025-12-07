def set_target_ip(target_device_data, **remote_device_target_config):
    from pk_internal_tools.pk_functions.set_wired_connection import set_wired_connection
    set_wired_connection(target_device_data.target_device_wired_connection_1_new, **remote_device_target_config)
    set_wired_connection(target_device_data.target_device_wired_connection_3_new, **remote_device_target_config)
