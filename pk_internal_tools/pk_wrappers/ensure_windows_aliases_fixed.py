import os
import subprocess
import logging
import traceback
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

def ensure_windows_aliases_fixed():
    """
    Fixes Windows command prompt aliases by setting up a doskey batch file
    and configuring the AutoRun registry key to point to it.
    """
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)

    logging.info("========================================")
    logging.info("Windows Alias Fixer")
    logging.info("========================================")

    pk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    cache_dir = os.path.join(pk_path, 'pk_cache_private')
    batch_file_path = os.path.join(cache_dir, 'pk_doskey.bat')

    os.makedirs(cache_dir, exist_ok=True)

    aliases = {
        "0": f"cd \"{pk_path}\",
        "1": f"cd \"{os.path.join(pk_path, 'pk_external_tools')}\",
        "2": f"cd \"{os.path.join(pk_path, 'pk_os_layer_resources')}\",
        "3": f"cd \"%USERPROFILE%\\pk_working\"",
        "4": f"cd \"%USERPROFILE%\\pk_memo\"",
        "5": f"cd \"%USERPROFILE%\\business_flow\"",
        "pk": f"python \"{os.path.join(pk_path, 'pk_internal_tools', 'pk_wrappers', 'pk_ensure_pk_enabled.py')}\"",
        "venv": f"\"{os.path.join(pk_path, '.venv', 'Scripts', 'activate')}\"",
        "ls": "dir",
        "cat": "type",
        "which": "where",
        "pwd": "cd",
        "gpt": "start https://chat.openai.com",
        "x": "exit"
    }
    
    # 1. Create the doskey batch file
    logging.info(f"1. Creating doskey batch file at: {batch_file_path}")
    try:
        with open(batch_file_path, 'w', encoding='utf-8') as f:
            f.write("@echo off\n")
            for alias, command in aliases.items():
                f.write(f"doskey {alias}={command}\n")
        logging.info("✅ Batch file created successfully.")
    except Exception as e:
        logging.error(f"❌ Failed to create batch file: {e}")
        return

    # 2. Set the AutoRun registry key
    logging.info(f"\n2. Setting AutoRun registry key to point to {batch_file_path}")
    try:
        subprocess.run(
            ['reg', 'add', 'HKCU\Software\Microsoft\Command Processor', '/v', 'AutoRun', '/t', 'REG_SZ', '/d', batch_file_path, '/f'],
            check=True,
            capture_output=True,
            text=True
        )
        logging.info("✅ AutoRun registry key set successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Failed to set AutoRun registry key: {e.stderr}")
    except FileNotFoundError:
        logging.error("`reg.exe` not found. This script is intended for Windows.")
        return

    logging.info("\nFix process completed!")
    logging.info("Please open a new CMD window to test the changes.")

if __name__ == '__main__':
    ensure_windows_aliases_fixed()
