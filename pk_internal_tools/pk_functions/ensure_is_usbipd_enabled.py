
def ensure_is_usbipd_enabled():
    """
    Checks if usbipd-win is enabled and running by executing 'usbipd wsl list'.

    This function attempts to run the 'usbipd wsl list' command. A successful
    execution (return code 0) indicates that the usbipd service is active.
    Any other return code or a FileNotFoundError suggests it is not enabled,
    not installed, or not in the system's PATH.

    Returns:
        bool: True if usbipd appears to be enabled, False otherwise.
    """
    import subprocess
    import logging

    logger = logging.getLogger(__name__)

    try:
        command = ["usbipd", "wsl", "list"]
        logger.debug(f"Executing command: {' '.join(command)}")

        # Execute the command, hiding the console window on Windows.
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        # A return code of 0 indicates the command ran successfully.
        if result.returncode == 0:
            logger.info("usbipd-win is enabled and accessible.")
            return True
        else:
            logger.warning(
                f"usbipd-win check command failed with return code {result.returncode}. "
                f"It might be disabled or not installed correctly."
            )
            if result.stderr:
                logger.debug(f"usbipd stderr: {result.stderr.strip()}")
            return False

    except FileNotFoundError:
        logger.error(
            "The 'usbipd' command was not found. "
            "Please ensure usbipd-win is installed and its location is included in the system's PATH environment variable."
        )
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred while checking usbipd-win status: {e}")
        return False
