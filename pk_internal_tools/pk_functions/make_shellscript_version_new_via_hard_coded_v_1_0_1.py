

from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed


def make_shellscript_version_new_via_hard_coded_v_1_0_1():
    import os.path
    import re
    import shutil

    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    def get_f_next_versioned(f_nx):
        import inspect
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()

        name, ext = os.path.splitext(f_nx)
        files = os.listdir("..")

        # 정규표현식으로 "v1.x.y" 형태의 버전을 찾기
        versioned_files = [f for f in files if re.match(fr"{re.escape(name)}_v\d+\.\d+\.\d+{re.escape(ext)}", f)]

        if versioned_files:
            latest_version = max(versioned_files, key=lambda x: list(map(int, re.findall(r"\d+", x)[-3:])))
            major, minor, patch = map(int, re.findall(r"\d+", latest_version)[-3:])
            patch += 1
            next_version = f"{major}.{minor}.{patch}"
        else:
            next_version = "1.0.0"

        return f"{name}_v{next_version}{ext}"

    def copy_with_version(f):
        import inspect
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()

        if not os.path.isfile(f):
            print(f"{f} f을 찾을 수 없습니다.")
            return

        f_new = get_f_next_versioned(os.path.basename(f))
        shutil.copy2(f, f_new)
        print(f"''{f}'를  {f_new}'로 복사되었습니다.")
        manage_versions(os.path.basename(f))

    def manage_versions(original_file_name):
        import inspect
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()

        name, ext = os.path.splitext(original_file_name)
        files = os.listdir("..")

        # 해당 f의 모든 버전 f을 찾기

        versioned_files = sorted(
            [f for f in files if re.match(fr"{re.escape(name)}_v\d+\.\d+\.\d+{re.escape(ext)}", f)],
            key=lambda x: list(map(int, re.findall(r"\d+", x)[-3:]))
        )

        # 최신 버전 f을 제외한 나머지 버전 f을 archive _d_로 이동
        dst = D_PK_ARCHIVED
        if len(versioned_files) > 1:
            latest_version = versioned_files[-1]
            os.makedirs(dst, exist_ok=True)

            for f in versioned_files[:-1]:
                shutil.move(f, dst)
                print(f"'{f}' f이 '{dst}' _d_로 이동되었습니다.")

    file_pnxs = [  # 상대경로
        os.path.expanduser(r"~/Downloads/pk_working/pk_system/vpc_info_collector.sh"),
        os.path.expanduser(r"~/Downloads/pk_working/pk_system/pk_ip_connection_update_for_114.sh"),
        os.path.expanduser(r"~/Downloads/pk_working/pk_system/pk_ip_connection_update_for_front.sh"),
        os.path.expanduser(r"~/Downloads/pk_working/pk_system/pk_ip_connection_update_for_rear.sh"),
        os.path.expanduser(r"~/Downloads/pk_working/pk_system/pk_ip_connection_update_for_reset.sh"),
        os.path.expanduser(r"~/Downloads/pk_working/pk_system/pk_evm_updater_for_front.sh"),
        # os.path.expanduser(r"~/Downloads/pk_working/pk_system/pk_evm_updater_for_rear.sh"),
    ]

    for file_pnx in file_pnxs:
        copy_with_version(file_pnx)

    ensure_iterable_data_printed(iterable_data=file_pnxs, iterable_data_n="다운로드완료")
