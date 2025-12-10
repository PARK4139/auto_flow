# auto_flow

Task Automation Utility Assistant - A Python-based automation framework for streamlining repetitive workflows and business processes.

## Overview

`auto_flow` is a wrapper system that provides an interactive CLI interface for executing automation scripts. Built on top of the `pk_system` framework, it enables users to automate various tasks through a two-stage selection process using `fzf`.

## Features

- **Interactive Wrapper Selection**: Two-stage selection (directory → file) using `fzf`
- **Multi-Category Support**: Organized wrappers by category (Huvitz, Personal, Python Mission)
- **Continuous Execution Loop**: Automatically restarts after each wrapper execution
- **History Support**: Remembers last selected wrapper for quick access
- **Cross-Platform**: Works on Windows, Linux, and WSL
- **pk_system Integration**: Leverages robust automation capabilities from pk_system

## Requirements

- **Python**: 3.12+ (3.13 recommended)
- **Package Manager**: `uv` (recommended) or `pip`
- **Optional**: `fzf` for interactive file selection (falls back to alternative selection if not available)

## Installation

### Prerequisites

1. Install `uv` (recommended):
   - Download from [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
   - Or use: `pip install uv`

2. Install `fzf` (optional but recommended):
   - Windows: `scoop install fzf` or download from [https://github.com/junegunn/fzf](https://github.com/junegunn/fzf)
   - Linux/WSL: `sudo apt install fzf` or `brew install fzf`

### Setup Steps

1. **Clone the repository**:
```bash
git clone https://github.com/PARK4139/auto_flow.git
cd auto_flow
```

2. **Install dependencies using uv**:
```bash
uv sync
```

3. **Install pk_system**:
```bash
python scripts/install_pk_system.py
```

   Or manually:
```bash
uv add git+https://github.com/PARK4139/pk_system.git
```

### Manual Installation (Alternative)

If you prefer using `pip`:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/WSL:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt  # (if available)
# Or install pk_system directly:
pip install git+https://github.com/PARK4139/pk_system.git
```

## Usage

### Quick Start

**Windows**:
```bash
# Double-click run.lnk or run.bat
# Or from command line:
run.bat
# Or:
bin\run.bat
```

**Linux/WSL**:
```bash
./bin/run.sh
```

**Direct Python execution**:
```bash
python __main__.py
```

### How It Works

1. **Start the application**: Run `run.bat` (Windows) or `bin/run.sh` (Linux/WSL)
2. **Select wrapper category**: Choose from available categories (Huvitz, Jung_Hoon_Park, etc.)
3. **Select specific wrapper**: If multiple files exist in the category, select the specific script
4. **Execution**: The selected wrapper script runs in a new console window
5. **Loop**: After execution, the selection menu appears again for continuous workflow

### Example Workflow

```
1. Run: run.bat
2. Select category: "Huvitz"
3. Select wrapper: "ehr 로그인.py"
4. Script executes in new window
5. Selection menu appears again
6. Press Ctrl+C to exit
```

## Project Structure

```
auto_flow/
├── __main__.py                 # Main entry point (infinite loop)
├── bin/                        # Executable scripts
│   ├── run.bat                # Windows runner
│   └── run.sh                 # Linux/WSL runner
├── scripts/                    # Installation and setup scripts
│   ├── install_pk_system.py  # pk_system installer
│   ├── install_pk_system.cmd  # Windows installer wrapper
│   └── install_pk_system.sh   # Linux/WSL installer wrapper
├── source/                     # Source code
│   ├── constants/             # Path and file constants
│   │   ├── directory_paths.py
│   │   └── file_paths.py
│   ├── functions/             # Core automation functions
│   │   ├── ensure_custom_cli_started.py  # Main wrapper launcher
│   │   ├── ensure_ehr_login.py
│   │   ├── ensure_ekiss_login.py
│   │   ├── ensure_huvitz_mail_opened.py
│   │   └── ...
│   ├── wrappers/              # Automation wrapper scripts
│   │   ├── Huvitz/            # Huvitz-related automations
│   │   │   ├── ehr 로그인.py
│   │   │   ├── eskiss 로그인.py
│   │   │   └── ...
│   │   ├── Jung_Hoon_Park/    # Personal automations
│   │   │   └── ...
│   │   └── python mission/    # Python tutorial scripts
│   │       └── ...
│   └── internal_setup.py      # Path setup utility
├── tests/                      # Test files
│   └── test_debug_log.py
├── etc/                        # Miscellaneous files
│   └── archived/              # Archived files
├── pyproject.toml             # Project configuration
├── uv.lock                    # Dependency lock file
├── run.bat                    # Root-level wrapper (calls bin/run.bat)
├── run.lnk                    # Windows shortcut
└── README.md                  # This file
```

## Configuration

### Environment Variables

Create a `.env` file in the project root (or parent directory) with the following variables:

```env
# Huvitz-related URLs
EHR_URL=https://ehr.example.com
EKISS_URL=https://ekiss.example.com
HUVITZ_MAIL_URL=https://mail.example.com

# Email settings
L_CAM_RECIPIENT_EMAIL=recipient@example.com
```

**Note**: The `.env` file is ignored by Git for security reasons. See `.gitignore`.

## Development

### Adding New Wrappers

1. **Create wrapper file** in appropriate category directory:
   - `source/wrappers/Huvitz/` for Huvitz-related automations
   - `source/wrappers/Jung_Hoon_Park/` for personal automations
   - Or create a new category directory

2. **Follow naming conventions**:
   - Use descriptive Korean or English names
   - File extension: `.py`

3. **Implement automation logic**:
   - Use `pk_system` functions for automation
   - Follow the `ensure_` prefix pattern for functions

4. **Automatic discovery**: The wrapper will be automatically available in the selection menu

### Code Style

- **Function naming**: Use `ensure_` prefix (except for `is_` or `get_` functions)
- **File naming**: Use `ensure_` prefix for function files (except for `is_` or `get_` files)
- **Comments**: Korean for code comments, English for technical documentation
- **Type hints**: Use where appropriate
- **PEP 8**: Follow Python style guidelines

### Core Functions

The project includes several core automation functions in `source/functions/`:

- `ensure_custom_cli_started.py`: Main wrapper launcher with fzf integration
- `ensure_ehr_login.py`: EHR login automation
- `ensure_ekiss_login.py`: eKiss login automation
- `ensure_huvitz_mail_opened.py`: Huvitz mail automation
- `ensure_f_LM_100_spindle_reliability_test_report_opened.py`: Excel file opener
- `ensure_L_CAM_milling_or_grinding_data_sent.py`: Data transmission automation

## Architecture

### Main Loop

The application runs in an infinite loop:
1. `__main__.py` calls `ensure_custom_cli_started()`
2. User selects wrapper through interactive menu
3. Wrapper executes in new console window
4. Loop continues after 50ms delay
5. Press Ctrl+C to exit

### Two-Stage Selection

1. **Directory Selection**: Choose wrapper category (e.g., "Huvitz")
2. **File Selection**: If multiple files exist, select specific script

### History Management

- Last selected wrapper is saved to history
- Next run will highlight the last selection
- History stored in project cache directory

## Troubleshooting

### Common Issues

1. **"모듈을 가져오는 데 실패했습니다"**
   - Solution: Run `python scripts/install_pk_system.py`

2. **"가상환경을 찾을 수 없습니다"**
   - Solution: Run `uv sync` to create virtual environment

3. **"fzf를 찾을 수 없습니다"**
   - Solution: Install fzf or the system will fall back to alternative selection

4. **Import errors**
   - Solution: Ensure `pk_system` is properly installed via `uv sync` or `pip install`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Add your license here]

## Author

PARK4139

## Acknowledgments

- Built on [pk_system](https://github.com/PARK4139/pk_system) framework
- Uses [fzf](https://github.com/junegunn/fzf) for interactive selection
- Powered by [uv](https://github.com/astral-sh/uv) for dependency management

## Related Documentation

- **Project Rules**: See `GEMINI.md` (in Korean) for detailed development rules and guidelines
- **pk_system Documentation**: Refer to pk_system repository for framework documentation

---

For more detailed information, see the `docs/` directory.
