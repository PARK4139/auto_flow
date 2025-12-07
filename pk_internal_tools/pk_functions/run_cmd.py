

import logging


def run_cmd(cmd):
    import subprocess

    """Run a shell cmd and return 1 if successful."""
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        logging.debug(f"cmd failed: {cmd}, Error: {e}")
        return 0
