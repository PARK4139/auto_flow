def does_text_exist_in_region_ocr(region: dict, text: str) -> bool:
    """
    Checks if a given text exists within a specific region of the screen using OCR.

    Args:
        region (dict): A dictionary defining the region with keys "x1", "y1", "x2", "y2".
        text (str): The text to search for within the region.

    Returns:
        bool: True if the text is found, False otherwise.
    """
    import logging
    # Lazy import to keep startup time low and follow project conventions.
    try:
        import easyocr
        from PIL import ImageGrab
        import numpy as np
    except ImportError as e:
        logging.error(f"Missing necessary libraries for OCR: {e}. Please install easyocr, Pillow, and numpy.")
        return False

    # Define the bounding box for the screenshot from the region dictionary
    try:
        bbox = (region['x1'], region['y1'], region['x2'], region['y2'])
    except KeyError:
        logging.error("Invalid 'region' dictionary passed. It must contain 'x1', 'y1', 'x2', 'y2'.")
        return False

    # Grab a screenshot of the specified region
    try:
        screenshot = ImageGrab.grab(bbox=bbox)
    except Exception as e:
        logging.error(f"Failed to grab screenshot for region {bbox}. Error: {e}")
        return False

    # Initialize the OCR reader. It's better to initialize it once if this function is called frequently.
    # For simplicity here, we initialize it on each call. Caching could be used for optimization.
    try:
        # TODO: The reader could be cached in a global object to speed up subsequent calls.
        reader = easyocr.Reader(['ko', 'en'])  # Add languages as needed
    except Exception as e:
        logging.error(f"Failed to initialize EasyOCR Reader. Error: {e}")
        return False
        
    # Convert the PIL Image to a NumPy array, which is the expected input format for EasyOCR.
    screenshot_np = np.array(screenshot)

    # Perform OCR on the screenshot array
    # We use detail=0 because we only need the text, not the bounding boxes within the ROI.
    results = reader.readtext(screenshot_np, detail=0)

    # Check if the desired text is in the OCR results
    for found_text in results:
        if text in found_text:
            logging.debug(f"Found text '{text}' in region {bbox}.")
            return True
            
    logging.debug(f"Text '{text}' not found in region {bbox}.")
    return False
