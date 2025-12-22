import subprocess
import logging
import platform
import os

def ensure_java_installed() -> bool:
    """
    Checks if Java is installed and accessible via the system's PATH.
    If not, it prints detailed instructions for manual installation.

    Returns:
        bool: True if Java is found and accessible, False otherwise.
    """
    logging.info("Checking if Java is installed and accessible...")
    try:
        # Run 'java -version' command
        result = subprocess.run(
            ['java', '-version'],
            capture_output=True,
            text=True,
            check=False, # Do not raise an exception for non-zero exit codes
            encoding='utf-8' # Ensure proper encoding for output
        )

        if result.returncode == 0:
            logging.info("Java is installed and accessible.")
            logging.debug(f"Java version output:\n{result.stdout}{result.stderr}")
            return True
        else:
            logging.error("Java is NOT found or not accessible via system PATH.")
            logging.error(f"Command output:\n{result.stdout}{result.stderr}")
            logging.error("--- Manual Java Installation Required ---")
            logging.error("Please follow these steps to install Java JDK (version 8 or higher):")
            logging.error("1. Download Java JDK: Visit https://www.oracle.com/java/technologies/downloads/ or OpenJDK website.")
            logging.error("2. Install Java JDK: Run the downloaded installer. Install to a standard path (e.g., C:\\Program Files\\Java\\jdk-11).")
            logging.error("3. Set JAVA_HOME Environment Variable (if not set by installer):")
            if platform.system() == "Windows":
                logging.error("   - Search '환경 변수' (Environment Variables) in Windows search, open '시스템 환경 변수 편집' (Edit system environment variables).")
                logging.error("   - Click '환경 변수' (Environment Variables) button.")
                logging.error("   - Under '시스템 변수' (System variables), click '새로 만들기' (New).")
                logging.error("   - Variable name: JAVA_HOME, Variable value: C:\\Program Files\\Java\\jdk-11 (replace with your actual JDK path).")
                logging.error("   - Find 'Path' in '시스템 변수', click '편집' (Edit).")
                logging.error("   - Click '새로 만들기' (New) and add %JAVA_HOME%\\bin.")
                logging.error("   - Click OK on all windows.")
            else: # Linux/macOS
                logging.error("   - Add to your shell profile (e.g., ~/.bashrc, ~/.zshrc):")
                logging.error("     export JAVA_HOME=/path/to/your/jdk")
                logging.error("     export PATH=$PATH:$JAVA_HOME/bin")
                logging.error("   - Run 'source ~/.bashrc' (or your profile file) to apply changes.")
            logging.error("4. Restart Command Prompt/Terminal: Close all current command prompt/terminal windows and open new ones.")
            logging.error("5. Verify: Run 'java -version' again to confirm Java is recognized.")
            logging.error("---------------------------------------")
            return False
    except FileNotFoundError:
        logging.error("The 'java' command was not found. Java is likely not installed or not in your system's PATH.")
        logging.error("--- Manual Java Installation Required ---")
        logging.error("Please follow the steps above to install Java JDK.")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred while checking Java installation: {e}", exc_info=True)
        return False

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    print("Running Java installation check...")
    if ensure_java_installed():
        print("Java check passed.")
    else:
        print("Java check failed. Please see the logs above for instructions.")
