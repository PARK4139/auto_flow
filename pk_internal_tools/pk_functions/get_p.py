def get_p(pnx):
    import logging
    from pathlib import Path

    if pnx is None:
        # Early, explicit failure with your logging convention
        logging.error("get_p() received None (pnx is None).")
        raise TypeError("get_p() expected a path-like value, got None")

    # Determine original input type
    is_str_input = isinstance(pnx, str)

    # Convert to Path object to perform .parent operation
    path_obj = Path(pnx)

    # Get the parent path
    parent_path_obj = path_obj.parent

    # Return in original input type
    if is_str_input:
        return str(parent_path_obj)
    else:  # It was a Path object
        return parent_path_obj
