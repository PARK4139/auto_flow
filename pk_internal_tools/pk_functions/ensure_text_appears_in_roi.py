def ensure_text_appears_in_roi(key_name: str, text: str, timeout: int = 20, history_reset: bool = False) -> bool:
    """
    Waits for a specific text to appear within a predefined Region of Interest (ROI).

    Args:
        key_name (str): The key_name of the ROI to monitor, as defined in the rois.json file.
        text (str): The text to wait for within the ROI.
        timeout (int): The maximum time to wait in seconds. Defaults to 20.
        history_reset (bool): If True, forces the re-registration of the ROI for the given key_name.

    Returns:
        bool: True if the text is found within the timeout, False otherwise.
    """
    import time
    import logging
    # Lazy imports to follow project conventions
    from pk_internal_tools.pk_functions.get_roi_coordinates import get_roi_coordinates
    from pk_internal_tools.pk_functions.does_text_exist_in_region_ocr import does_text_exist_in_region_ocr
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_roi_defined_interactively import ensure_roi_defined_interactively

    # If history_reset is True, force re-registration of the ROI
    if history_reset:
        logging.info(f"history_reset=True: Forcing re-registration of ROI for key '{key_name}'.")
        if not ensure_roi_defined_interactively(key_name):
            logging.error(f"Forced ROI re-registration for '{key_name}' failed or was cancelled.")
            ensure_spoken("Area re-definition was cancelled.")
            return False
        logging.info(f"ROI for '{key_name}' re-registered successfully.")

    # Retrieve the ROI coordinates from the central file
    roi = get_roi_coordinates(key_name)
    if not roi:
        logging.warning(f"ROI for key '{key_name}' not found. Starting registration process.")

        # Trigger the visual registration process
        if ensure_roi_defined_interactively(key_name):
            # Try to get the coordinates again after successful registration
            roi = get_roi_coordinates(key_name)
            if not roi:
                logging.error(f"Failed to retrieve ROI for '{key_name}' even after registration.")
                ensure_spoken("Failed to retrieve the area after saving.")
                return False
        else:
            # Registration was cancelled or failed
            logging.error(f"ROI registration for '{key_name}' failed or was cancelled.")
            ensure_spoken("Area definition was cancelled.")
            return False

    message = f"Waiting for text '{text}' to appear in the '{key_name}' area."
    logging.info(message)
    ensure_spoken(message)

    start_time = time.time()
    while time.time() - start_time < timeout:
        if does_text_exist_in_region_ocr(region=roi, text=text):
            success_message = f"Success: Found text '{text}' in the '{key_name}' area."
            logging.info(success_message)
            ensure_spoken(success_message)
            return True
        time.sleep(0.5)  # Polling interval

    warning_message = f"Timeout: Did not find text '{text}' in the '{key_name}' area after {timeout} seconds."
    logging.warning(warning_message)
    ensure_spoken(warning_message)
    return False
