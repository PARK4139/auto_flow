def get_roi_coordinates(key_name: str) -> dict | None:
    """
    Retrieves the coordinates for a given key_name from the central ROI JSON file.

    Args:
        key_name (str): The unique key of the ROI to retrieve.

    Returns:
        dict | None: A dictionary with ROI coordinates (x1, y1, x2, y2) if found, otherwise None.
    """
    import json
    import logging
    from pathlib import Path

    # Central path to the ROI storage file
    roi_file_path = Path(r"C:\Users\CRAIS\Downloads\pk_system\.pk_system\pk_cache\rois.json")

    if not roi_file_path.exists():
        logging.warning(f"ROI storage file not found at: {roi_file_path}")
        return None

    try:
        with open(roi_file_path, 'r', encoding='utf-8') as f:
            all_rois = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        logging.warning(f"Could not read or parse ROI file: {roi_file_path}")
        return None

    if key_name not in all_rois:
        logging.warning(f"ROI with key '{key_name}' not found in {roi_file_path}")
        return None
        
    return all_rois.get(key_name)

