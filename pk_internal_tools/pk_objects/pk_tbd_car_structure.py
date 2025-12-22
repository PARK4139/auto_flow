from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.print_pk_divider import print_pk_divider


class TODOCarDataStructure:
    # target_device_data_orm
    class RemoteDeviceDataStructure:
        target_device_local_ssh_public_key = None
        target_device_local_ssh_private_key = None
        target_device_purpose = None
        target_device_type = None
        target_device_ip = None
        target_device_port = None
        target_device_user_n = None
        target_device_pw = None
        target_device_side = None
        target_device_aifw_version = None
        target_device_aifw_packing_mode = None
        target_device_aifw_branch_n = None
        target_device_with_flash_image = None
        target_device_flash_image_version = None
        target_device_core_cnt = None
        target_device_proceser_name = None
        target_device_nvidia_serial = None
        target_device_os_distro_name = None
        target_device_identifier = None
        target_device_identifier_number = None
        target_device_jetpack_version = None
        target_device_wired_connection_reset = {}
        target_device_wired_connection_initial = {}
        target_device_wired_connection_1_new = {}
        target_device_wired_connection_3_new = {}
        target_device_available_test_ip_set = set()

        def __init__(self):
            pass

        def set_remote_device_data_field_all(self, pk_structure):
            try:
                # self.identifier = pk_structure.identifier
                # self.jetpack_ver = pk_structure.jetpack_ver
                # self.target_device_flash_image = pk_structure.target_device_flash_image

                # swallow copy all field of pk_structure
                for key, value in pk_structure.__dict__.items():
                    setattr(self, key, value)

            except Exception as e:
                import traceback
                logging.debug(rf"{traceback.format_exc()}   ")

        def print_remote_device_data_field_all(self, instance_name, with_none=0):
            if instance_name is None:
                instance_name = self.__class__.__name__
            print_pk_divider('%%%FOO%%%')
            if with_none == 1:
                for key, value in self.__dict__.items():
                    logging.debug(f'''{instance_name}.{key}={value} ''')
            else:
                for key, value in self.__dict__.items():
                    if value is not None:
                        logging.debug(f'''{instance_name}.{key}={value} ''')
            print_pk_divider('%%%FOO%%%')
