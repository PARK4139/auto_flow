# auto_flow

Task Automation Utility Assistant

## Description

`auto_flow` is a Python-based task automation utility assistant designed to streamline repetitive workflows and automate various business processes. The project provides a wrapper system that enables users to execute automation scripts through an interactive CLI interface.

## Purpose

Supply Task Assistant for People - This project aims to help users automate their daily tasks and workflows efficiently, reducing manual work and improving productivity.

## Features

- **Interactive Wrapper Selection**: Choose and execute automation scripts through fzf-based interactive selection
- **Multi-Environment Support**: Works on Windows, Linux, and WSL
- **Modular Architecture**: Organized wrapper system for different use cases (Huvitz, personal automation, etc.)
- **pk_system Integration**: Built on top of the pk_system framework for robust automation capabilities

## Requirements

- Python 3.13+
- `uv` package manager (recommended)
- `fzf` (for interactive file selection)

## Installation

### Using uv (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/PARK4139/auto_flow.git
cd auto_flow
```

2. Install dependencies:
```bash
uv sync
```

3. Install pk_system:
```bash
python scripts/install_pk_system.py
```

### Manual Installation

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
- Windows: `.venv\Scripts\activate`
- Linux/WSL: `source .venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the main script:
```bash
# Windows
run.bat
# or
bin\run.bat

# Linux/WSL
./bin/run.sh
```

### Project Structure

```
auto_flow/
├── bin/                    # Executable scripts
│   ├── run.bat            # Windows runner
│   └── run.sh             # Linux/WSL runner
├── scripts/                # Installation and setup scripts
│   ├── install_pk_system.py
│   └── ...
├── source/                 # Source code
│   ├── constants/         # Path and file constants
│   ├── functions/         # Core functions
│   └── wrappers/          # Automation wrappers
│       ├── Huvitz/        # Huvitz-related automations
│       └── Jung_Hoon_Park/ # Personal automations
└── __main__.py            # Main entry point
```

## Development

### Adding New Wrappers

1. Create a new Python file in `source/wrappers/` directory
2. Follow the naming convention: use descriptive names
3. Implement your automation logic
4. The wrapper will be automatically available in the selection menu

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write clear, descriptive function names with `ensure_` prefix (except for `is_` or `get_` functions)
- Add docstrings in Korean for code comments, but keep technical documentation in English

## Configuration

### Environment Variables

Create a `.env` file in the project root (or parent directory) with the following variables:

```env
EHR_URL=https://ehr.example.com
EKISS_URL=https://ekiss.example.com
HUVITZ_MAIL_URL=https://mail.example.com
L_CAM_RECIPIENT_EMAIL=recipient@example.com
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license here]

## Used AI Tools

- Cursor AI
- Gemini CLI

## Author

PARK4139

---

For detailed project rules and guidelines, see `GEMINI.md` (in Korean).
