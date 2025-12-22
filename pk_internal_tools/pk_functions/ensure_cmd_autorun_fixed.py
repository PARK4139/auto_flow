import subprocess
import os
import logging
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done
import traceback

def ensure_cmd_autorun_fixed():
    """
    Fixes CMD AutoRun issues by removing the AutoRun registry key and setting up doskey aliases.
    """
    ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)

    logging.info("========================================")
    logging.info("CMD AutoRun Fixer")
    logging.info("========================================")

    # 1. Remove existing AutoRun registry setting
    logging.info("1. Removing existing AutoRun registry setting...")
    try:
        subprocess.run(
            ['reg', 'delete', 'HKCU\Software\Microsoft\Command Processor', '/v', 'AutoRun', '/f'],
            check=True,
            capture_output=True,
            text=True
        )
        logging.info("Successfully removed AutoRun setting.")
    except subprocess.CalledProcessError as e:
        if "The system was unable to find the specified registry key or value." in e.stderr:
            logging.info("AutoRun setting not found, no action needed.")
        else:
            logging.warning(f"⚠️ Failed to remove AutoRun setting: {e.stderr}")
    except FileNotFoundError:
        logging.error("`reg.exe` not found. This script is intended for Windows.")
        return

    # 2. Setup doskey aliases
    logging.info("\n2. Setting up doskey aliases...")
    pk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    aliases = {
        "0": f"cd \"{pk_path}\"",
        "1": f"cd \"{os.path.join(pk_path, 'pk_external_tools')}\"",
        "2": f"cd \"{os.path.join(pk_path, 'pk_os_layer_resources')}\"",
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

    success_count = 0
    for alias, command in aliases.items():
        try:
            doskey_cmd = f"doskey {alias}={command}"
            result = subprocess.run(doskey_cmd, shell=True, check=True, capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"✅ {alias} = {command}")
                success_count += 1
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Failed to register alias '{alias}': {e.stderr}")
        except Exception as e:
            logging.error(f"❌ An error occurred while registering alias '{alias}': {e}")
    
    logging.info(f"\n📊 Registered aliases: {success_count}개")
    logging.info("\nFix process completed!")
    logging.info("Please open a new CMD window to test the changes.")

