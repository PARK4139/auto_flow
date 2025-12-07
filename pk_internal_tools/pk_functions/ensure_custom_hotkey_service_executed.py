def ensure_custom_hotkey_service_executed(hotkey_map):
    import logging

    import keyboard

    logging.info("Starting custom hotkey service...")
    if not isinstance(hotkey_map, dict):
        logging.error("hotkey_map must be a dictionary.")
        return

    # Unhook all existing hotkeys to ensure a clean state
    keyboard.unhook_all()

    for hotkey, func in hotkey_map.items():
        try:
            # The `suppress=True` argument prevents the hotkey from being passed to other applications
            keyboard.add_hotkey(hotkey, func, suppress=True)
            logging.info(f"Registered hotkey: '{hotkey}' -> {func.__name__}")
        except Exception as e:
            logging.error(f"Failed to register hotkey '{hotkey}': {e}")

    logging.info("All hotkeys registered. Waiting for input... (Press Ctrl+C in console to stop)")

    try:
        # keyboard.wait() blocks the program and waits for hotkey events indefinitely.
        # This is the most efficient way to listen for global hotkeys.
        keyboard.wait()
    except KeyboardInterrupt:
        logging.info("Hotkey service stopped by user (KeyboardInterrupt).")
    except Exception as e:
        logging.error(f"Hotkey service stopped due to an unexpected error: {e}")
    finally:
        # Clean up all registered hotkeys when the service stops
        keyboard.unhook_all()
        logging.info("All hotkeys have been unhooked. Service terminated.")
