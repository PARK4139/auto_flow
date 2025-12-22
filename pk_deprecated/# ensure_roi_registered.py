def ensure_roi_registered(key_name: str):
    """
    Guides the user to select a Region of Interest (ROI) with the mouse
    and saves it to a central JSON file with a given key_name.

    Args:
        key_name (str): The unique key to identify this ROI.
    """
    import json
    import logging
    from pathlib import Path
    # Assuming the project conventions allow for lazy imports inside functions.
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.get_mouse_position_on_click import get_mouse_position_on_click

    # As per the project description, .pk_system is at the root.
    # A robust solution would use a centralized path manager.
    roi_file_path = Path(r"C:\Users\CRAIS\Downloads\pk_system\.pk_system\pk_cache\rois.json")

    # Guide the user via voice
    ensure_spoken(f"Please click the top-left corner of the '{key_name}' area.")
    p1 = get_mouse_position_on_click()
    if not p1:
        logging.error("Failed to get the first click position. Aborting.")
        ensure_spoken("Failed to register the area.")
        return False
    logging.info(f"First point captured: ({p1.x}, {p1.y})")

    ensure_spoken(f"Great. Now, please click the bottom-right corner of the '{key_name}' area.")
    p2 = get_mouse_position_on_click()
    if not p2:
        logging.error("Failed to get the second click position. Aborting.")
        ensure_spoken("Failed to register the area.")
        return False
    logging.info(f"Second point captured: ({p2.x}, {p2.y})")

    # Sort coordinates to handle any click order (top-left then bottom-right, or vice-versa)
    x1 = min(p1.x, p2.x)
    y1 = min(p1.y, p2.y)
    x2 = max(p1.x, p2.x)
    y2 = max(p1.y, p2.y)

    roi_data = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}

    # Read existing data from the file
    if roi_file_path.exists():
        try:
            with open(roi_file_path, 'r', encoding='utf-8') as f:
                all_rois = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            all_rois = {}
    else:
        all_rois = {}
        # Ensure parent directory exists
        roi_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Add or update the new ROI data
    all_rois[key_name] = roi_data

    # Write the updated data back to the file
    try:
        with open(roi_file_path, 'w', encoding='utf-8') as f:
            json.dump(all_rois, f, indent=4)
    except IOError as e:
        logging.error(f"Failed to write to ROI file at {roi_file_path}: {e}")
        ensure_spoken("Error saving the area.")
        return False

    ensure_spoken(f"The '{key_name}' area has been saved successfully.")
    logging.info(f"ROI '{key_name}' was saved with coordinates {roi_data}")
    return True
