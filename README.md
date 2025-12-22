![Preview](pk_internal_necessary/pk_images/auto_flow_preview_lighten.gif)

**PREVIEW**

# pk_system

A CLI utility system based on `fzf` for streamlined MVP development and interactive automation.

## Overview

`pk_system` is a robust Python library and toolchain designed to accelerate the creation of Minimum Viable Products (MVPs) through powerful command-line utilities and interactive user experiences. By leveraging `fzf` for fuzzy finding and structured automation workflows, it aims to provide a highly efficient and adaptable development environment.

## Features

*   **Interactive CLI**: Utilizes `fzf` for dynamic, user-guided command execution and input collection.
*   **Rapid MVP Development**: Offers a suite of pre-built utilities to quickly bootstrap and automate common tasks.
*   **Modular Architecture**: Organized with a flat-layout structure for easy module import and extension.
*   **Cross-Platform Ready**: Designed for Windows 10+, with ongoing development for Ubuntu 22.04 LTS compatibility.
*   **Sensitive Data Management**: Dedicated `.pk_system` directory for secure handling of user-specific configurations and secrets.

## Requirements

### Operating System Support

`pk_system` is primarily developed for and fully supports **Windows 10 and later** environments.
Compatibility with **Ubuntu 22.04 LTS** is currently under active development and is expected to be fully supported in future releases.

### Core Dependencies
*   **Python**: Version `3.12` or `3.13` is required (`requires-python = ">=3.12, <3.14"`).
*   **uv**: Essential for fast dependency management and script execution.
*   **fzf**: Core interactive CLI features rely on `fzf`. An `fzf.exe` is provided for Windows, or install via package manager for Linux/macOS.

## Installation Guide

Setting up `pk_system` for development is a straightforward process.

### Step 1: Install Prerequisites

Ensure the following tools are installed and configured:

1.  **Python (Version 3.12 or 3.13)**
    *   [Official Website](https://www.python.org/)
    *   Ensure Python is added to your system's `PATH`.

2.  **uv (Python Package Manager)**
    *   **Windows (PowerShell):** `irm https://astral.sh/uv/install.ps1 | iex`
    *   **Linux/macOS:** `curl -LsSf https://astral.sh/uv/install.sh | sh`

3.  **fzf (Command-Line Fuzzy Finder)**
    *   **Windows:** `fzf.exe` is included in this repository. Add the project root to your system's `PATH`.
    *   **Linux/macOS:** Install via Homebrew (`brew install fzf`) or apt (`sudo apt-get install fzf`).

### Step 2: Clone the Repository

```bash
git clone https://github.com/PARK4139/pk_system.git
cd pk_system
```

### Step 3: Create Environment and Install Dependencies

```bash
uv sync
```
This command will:
*   Read `pyproject.toml` and `uv.lock`.
*   Create a local virtual environment (`.venv`).
*   Install all required packages.
*   Perform an **editable install** of `pk_system`, reflecting code changes immediately.

## Usage

`pk_system` is designed for interactive command-line operations and modular integration.

### Running CLI Wrappers

The `pk_system` provides various CLI wrapper scripts in `pk_internal_tools/pk_wrappers/`. These scripts leverage `fzf` and `ensure_value_completed()` for interactive input.

1.  **Activate the virtual environment**:
    *   **Windows (PowerShell/CMD):** `.\.venv\Scripts\activate`
    *   **Linux/WSL (Bash/Zsh):** `source ./.venv/bin/activate`

2.  **Execute the script**:
    Example: Convert a GIF using `ensure_ffmpeg_gif_converted.py`.
    ```bash
    python pk_internal_tools/pk_wrappers/ensure_ffmpeg_gif_converted.py
    ```
    The script will interactively prompt for parameters like input/output paths and conversion settings.

### Importing Modules

Given the flat-layout structure, you can import modules directly from `pk_internal_tools` in your Python projects.

```python
# Example of importing commonly used functions
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken

# Example of importing an object
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT
```

## Project Structure

This project adopts a **flat-layout**, where `pk_internal_tools` is the top-level Python package.

```
pk_system/ (Project Root)
├── .pk_system/            # User-specific configurations and sensitive data
├── pk_internal_tools/     # Top-level Python package
│   ├── __init__.py
│   ├── pk_functions/      # Function modules
│   ├── pk_objects/        # Object classes
│   └── pk_wrappers/       # CLI wrappers
├── pk_external_tools/     # External executables and static resources
├── pk_docs/               # Project documentation
├── pyproject.toml
└── README.md
```

## Configuration & Security Notes

The `.pk_system/` directory is crucial for storing user-specific configurations, environment variables, API keys, tokens, and other sensitive information, including data interactively provided by the user.

*   **Version Control Exclusion**: Files within this directory are intentionally excluded from version control (`.gitignore`) to prevent accidental exposure.
*   **Security Caution**: Users should exercise extreme caution as these files may contain sensitive data. Secure management of this directory is paramount. Do not share its contents.

## License

This project is licensed under the MIT License.

## Author

junghoon.park (park4139@google.com)
