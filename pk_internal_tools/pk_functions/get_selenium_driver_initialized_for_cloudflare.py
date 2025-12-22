import os
import tempfile
from seleniumbase import Driver

def get_selenium_driver_initialized_for_cloudflare(headless_mode=True, download_dir=None):
    # Get a temporary directory
    temp_dir = tempfile.gettempdir()
    
    # Save the original directory
    original_dir = os.getcwd()
    
    try:
        # Change to the temporary directory
        os.chdir(temp_dir)
        
        # Create the driver. It will create downloaded_files in the temp_dir
        driver = Driver(uc=True, headless=headless_mode)
    finally:
        # Change back to the original directory
        os.chdir(original_dir)
        
    return driver
