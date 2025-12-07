import logging
import pyperclip
from pathlib import Path
import sys

# Add project root for imports if the script is run directly
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized

def ensure_max_and_min_value_printed_by_text_seperator(input_string: str):
    """
    Parses a string containing numbers and number pairs with various separators,
    finds the minimum and maximum values among all numbers, and prints them.
    Handles spaces, tabs, hyphens, and no-space inputs according to user's logic.
    """
    if not input_string or not input_string.strip():
        logging.warning("Input string is empty or contains only whitespace.")
        return None, None

    # n. Normalize separators using the robust logic developed
    processed_input = input_string
    processed_input = processed_input.replace("\t", " ")
    while "  " in processed_input:
        processed_input = processed_input.replace("  ", " ")
    
    processed_input = processed_input.replace(" ", ",")
    processed_input = processed_input.replace("-", ",")
    
    while ",," in processed_input:
        processed_input = processed_input.replace(",,", ",")
    
    processed_input = processed_input.strip(',')

    # n. Extract numbers
    # This handles the "282-297252-274" case as per user's clarification
    # by splitting it into ['282', '297252', '274', ...]
    nums_str = [s for s in processed_input.split(',') if s.strip().isdigit()]

    if not nums_str:
        logging.warning(f"No numbers found in the input string: '{input_string}'")
        return None, None

    # 3. Convert to integers and find min/max
    try:
        nums = [int(s) for s in nums_str]
        min_val = min(nums)
        max_val = max(nums)
    except (ValueError, TypeError) as e:
        logging.error(f"Error converting numbers or finding min/max: {e}")
        return None, None


    # 4. Print the result
    output_text = f"min: {min_val}, max: {max_val}"
    logging.info("="*30)
    logging.info(f"Input String : '{input_string}'")
    logging.info(f"Parsed Numbers : {nums}")
    logging.info(f"Result         : {output_text}")
    logging.info("="*30)
    
    return min_val, max_val

if __name__ == '__main__':
    ensure_pk_log_initialized(__file__)
    
    # Example usage with clipboard content
    try:
        clipboard_content = pyperclip.paste()
        if clipboard_content and clipboard_content.strip():
            logging.info("Processing content from clipboard...")
            ensure_max_and_min_value_printed_by_text_seperator(clipboard_content)
        else:
            logging.info("Clipboard is empty. Testing with predefined cases.")
            test_cases = [
                "80-297 252-274\t210-264  260-442",
                "282-297  252-274  210-264  260-281",
                "282-297252-274210-264260-281",
                "282-297-252-274-210-264-260-281"
            ]
            for i, case in enumerate(test_cases, 1):
                print(f"\n--- Running Test Case {i} ---")
                ensure_max_and_min_value_printed_by_text_seperator(case)

    except Exception as e:
        logging.error(f"An error occurred in main execution: {e}", exc_info=True)
