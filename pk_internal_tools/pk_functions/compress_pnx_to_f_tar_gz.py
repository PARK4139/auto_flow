from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style


def compress_pnx_to_f_tar_gz(pnx, dst):
    import tarfile
    import os

    pnx = get_pnx_windows_style(pnx)
    dst = get_pnx_windows_style(dst)

    # Ensure the source exists
    if not os.path.exists(pnx):
        raise FileNotFoundError(f"Source path '{pnx}' does not exist.")

    # Create a tar.gz archive
    with tarfile.open(dst, "w:gz") as tar:
        def preserve_metadata(tarinfo):
            """
            Preserve file metadata (permissions, ownership, timestamps).
            """
            tarinfo.preserve = True  # Ensure extended metadata is kept
            return tarinfo

        # Add the source directory, preserving metadata
        tar.add(pnx, arcname=os.path.basename(pnx), recursive=True, filter=preserve_metadata)
