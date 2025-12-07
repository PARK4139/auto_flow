

def restore_workspace_from_latest_archive(D_PKG_ARCHIVED, d_working):
    import logging
    import logging
    import os
    import shutil
    import tarfile
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    archives = sorted(
        [f for f in os.listdir(D_PKG_ARCHIVED) if f.endswith('.tar.bz2')],
        key=lambda f: os.path.getmtime(os.path.join(D_PKG_ARCHIVED, f)),
        reverse=True
    )
    if not archives:
        logging.warning(f"[{PkTexts.ERROR}] No backup archive found in {D_PKG_ARCHIVED}")
        return

    latest_archive = os.path.join(D_PKG_ARCHIVED, archives[0])
    logging.debug(f"[{PkTexts.REVERT}] Restoring from {latest_archive}")

    if os.path.exists(d_working):
        shutil.rmtree(d_working)
    os.makedirs(d_working, exist_ok=True)

    with tarfile.open(latest_archive, "r:bz2") as tar:
        # 내부 최상위 디렉토리명 추출
        members = tar.getmembers()
        root_dir_name = members[0].name.split('/')[0]  # 'workspace1/something.py' → 'workspace1'

        for member in members:
            if member.name.startswith(root_dir_name + '/'):
                member.name = member.name[len(root_dir_name) + 1:]  # 디렉토리명 제거
                if member.name:  # 비어있으면 무시
                    tar.extract(member, path=d_working)

    logging.debug(f"[{PkTexts.REVERT}] Restored to {d_working}")
