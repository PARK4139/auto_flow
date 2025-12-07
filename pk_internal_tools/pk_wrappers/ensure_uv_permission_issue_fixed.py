#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
import logging
import traceback
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE

def _fix_uv_permission_issue_steps():
    """Internal function to perform the fix steps."""
    logging.info("🔧 UV Permission Issue Fix Start")
    logging.info(PK_UNDERLINE)

    project_root = os.getcwd()
    if platform.system().lower() == "windows":
        venv_path = os.path.join(project_root, ".venv")
    else:
        venv_path = os.path.join(project_root, ".venv")
    lib64_path = os.path.join(venv_path, "lib64")

    logging.info(f"Project Root: {project_root}")
    logging.info(f"Venv Path: {venv_path}")
    logging.info(f"lib64 Path: {lib64_path}")

    logging.info("🔍 Checking current status")
    if os.path.exists(venv_path):
        logging.info("✅ Virtual environment exists.")
        if os.path.exists(lib64_path):
            logging.warning("⚠️ lib64 directory exists - potential permission issue.")
        else:
            logging.info("✅ lib64 directory does not exist.")
    else:
        logging.warning("⚠️ Virtual environment does not exist.")

    logging.info("🔧 Applying solutions")

    logging.info("1️⃣ Cleaning UV cache")
    try:
        result = subprocess.run(['uv', 'cache', 'clean'], capture_output=True, text=True, timeout=30, check=True)
        logging.info("✅ UV cache cleaned successfully.")
    except Exception as e:
        logging.error(f"❌ Error cleaning UV cache: {e}")

    logging.info("2️⃣ Recreating virtual environment")
    if os.path.exists(venv_path):
        try:
            backup_path = venv_path + ".backup"
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
            shutil.move(venv_path, backup_path)
            logging.info(f"📦 Backed up existing venv to: {backup_path}")

            result = subprocess.run(['uv', 'venv'], capture_output=True, text=True, timeout=60, check=True)
            logging.info("✅ New virtual environment created successfully.")
            
            try:
                shutil.rmtree(backup_path)
                logging.info(f"🧹 Backup deleted: {backup_path}")
            except Exception as e:
                logging.warning(f"⚠️ Failed to delete backup: {e}")

        except Exception as e:
            logging.error(f"❌ Error recreating virtual environment: {e}")
    else:
        logging.info("⚠️ Virtual environment does not exist, skipping recreation.")
    
    _create_python_direct_script()

def _create_python_direct_script():
    """Creates a script to run python directly, bypassing uv."""
    logging.info("📝 Creating direct python execution script")
    logging.info(PK_UNDERLINE)

    script_content = '''#!/usr/bin/env python3
"""
Direct Python execution script (bypasses uv)
"""
import os
import sys
import subprocess
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE

def run_python_direct():
    """Run python directly"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    try:
        from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_executed import ensure_pk_wrapper_starter_executed
        logging.info("🚀 Starting system with direct Python execution")
        logging.info(PK_UNDERLINE)
        
        result = ensure_pk_wrapper_starter_executed()
        
        if result:
            logging.info("✅ System started successfully")
        else:
            logging.error("❌ System start failed")
        return result
    except Exception as e:
        logging.error(f"❌ System start error: {e}")
        return False

if __name__ == "__main__":
    run_python_direct()
'''
    script_path = "run_python_direct.py"
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        logging.info(f"✅ Direct execution script created: {script_path}")
        logging.info("💡 Usage: python run_python_direct.py")
    except Exception as e:
        logging.error(f"❌ Failed to create script: {e}")

def ensure_uv_permission_issue_fixed():
    """
    Main function to fix UV permission issues.
    """
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    
    logging.info("🎯 UV Permission Issue Fixer Script")
    logging.info(PK_UNDERLINE)
    
    _fix_uv_permission_issue_steps()
    
    logging.info("🏁 All tasks completed.")
    logging.info(PK_UNDERLINE)
    logging.info("💡 Recommendations:")
    logging.info("1. UV permission issue should be resolved.")
    logging.info("2. Use 'python run_python_direct.py' for improved performance.")

if __name__ == "__main__":
    ensure_uv_permission_issue_fixed()
