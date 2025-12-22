def ensure_roi_defined_interactively(key_name: str) -> bool:
    """
    Visually and interactively prompts the user to define a Region of Interest (ROI)
    using a draggable/resizable window and saves it to the central JSON file.

    Args:
        key_name (str): The unique key to identify this ROI.

    Returns:
        bool: True if the ROI was successfully defined and saved, False otherwise.
    """
    import json
    import logging
    from pathlib import Path
    
    # Lazy import of the new visual selector class
    from pk_internal_tools.pk_objects.pk_roi_selector import ROISelector
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken

    # Announce the action
    ensure_spoken(f"Starting visual selection for the '{key_name}' area.")
    
    # Create and run the ROI selector window
    selector_title = f"Define area for '{key_name}'"
    selector = ROISelector(key_name=key_name, title=selector_title)
    roi_coords = selector.run()

    # If the user cancelled the selection
    if not roi_coords:
        logging.warning("ROI selection was cancelled by the user.")
        ensure_spoken("Area selection cancelled.")
        return False

    # Path to the central ROI storage file
    roi_file_path = Path(r"C:\Users\CRAIS\Downloads\pk_system\.pk_system\pk_cache\rois.json")

    # Read existing data from the file
    if roi_file_path.exists():
        try:
            with open(roi_file_path, 'r', encoding='utf-8') as f:
                all_rois = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            all_rois = {}
    else:
        all_rois = {}
        roi_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Add or update the new ROI data
    all_rois[key_name] = roi_coords

    # Write the updated data back to the file
    try:
        with open(roi_file_path, 'w', encoding='utf-8') as f:
            json.dump(all_rois, f, indent=4)
    except IOError as e:
        logging.error(f"Failed to write to ROI file at {roi_file_path}: {e}")
        ensure_spoken("Error saving the area.")
        return False

    ensure_spoken(f"The '{key_name}' area has been saved successfully.")
    logging.info(f"ROI '{key_name}' was saved with coordinates {roi_coords}")
    return True
