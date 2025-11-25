# Installation Guide

## Prerequisites

### Required

- **Python 3.12+** (3.13 recommended)
  - Download from [python.org](https://www.python.org/downloads/)
  - Verify: `python --version`

### Recommended

- **uv** - Fast Python package manager
  - Install: `pip install uv`
  - Or download from [github.com/astral-sh/uv](https://github.com/astral-sh/uv)
  - Verify: `uv --version`

- **fzf** - Interactive file selector
  - Windows: `scoop install fzf` or download from [github.com/junegunn/fzf](https://github.com/junegunn/fzf)
  - Linux/WSL: `sudo apt install fzf` or `brew install fzf`
  - Verify: `fzf --version`

## Installation Steps

### Method 1: Using uv (Recommended)

1. **Clone the repository**:
```bash
git clone https://github.com/PARK4139/auto_flow.git
cd auto_flow
```

2. **Install dependencies**:
```bash
uv sync
```

This will:
- Create a virtual environment (`.venv`)
- Install all dependencies including `pk_system`
- Lock dependencies in `uv.lock`

3. **Verify installation**:
```bash
# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/WSL:
source .venv/bin/activate

# Test import
python -c "from pk_system.pk_sources.pk_objects.pk_system_directories import get_pk_system_root; print(get_pk_system_root())"
```

### Method 2: Manual Installation

1. **Clone the repository**:
```bash
git clone https://github.com/PARK4139/auto_flow.git
cd auto_flow
```

2. **Create virtual environment**:
```bash
python -m venv .venv
```

3. **Activate virtual environment**:
```bash
# Windows:
.venv\Scripts\activate
# Linux/WSL:
source .venv/bin/activate
```

4. **Install pk_system**:
```bash
# Using pip
pip install git+https://github.com/PARK4139/pk_system.git

# Or using the installer script
python scripts/install_pk_system.py
```

### Method 3: Using the Installer Script

The project includes an automated installer:

```bash
# Windows
scripts\install_pk_system.cmd

# Linux/WSL
bash scripts/install_pk_system.sh

# Or directly
python scripts/install_pk_system.py
```

## Post-Installation Setup

### 1. Configure Environment Variables

Create a `.env` file in the project root (or parent directory):

```env
# Huvitz Services
EHR_URL=https://ehr.example.com
EKISS_URL=https://ekiss.example.com
HUVITZ_MAIL_URL=https://mail.example.com

# Email Configuration
L_CAM_RECIPIENT_EMAIL=recipient@example.com
```

**Note**: The `.env` file is gitignored for security. Never commit sensitive information.

### 2. Verify Installation

Run the application:

```bash
# Windows
run.bat
# Or double-click run.lnk

# Linux/WSL
./bin/run.sh
```

You should see the wrapper selection menu.

## Troubleshooting

### Issue: "pk_system 모듈을 가져오는 데 실패했습니다"

**Solution**:
```bash
python scripts/install_pk_system.py
```

Or manually:
```bash
uv add git+https://github.com/PARK4139/pk_system.git
```

### Issue: "가상환경을 찾을 수 없습니다"

**Solution**:
```bash
uv sync
```

Or manually:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/WSL
```

### Issue: "fzf를 찾을 수 없습니다"

**Solution**: Install fzf (see Prerequisites) or the system will use alternative selection method.

### Issue: Import errors

**Solution**:
1. Ensure virtual environment is activated
2. Reinstall dependencies: `uv sync` or `pip install -r requirements.txt`
3. Verify pk_system installation: `python -c "import pk_system; print(pk_system.__file__)"`

### Issue: Permission errors (Linux/WSL)

**Solution**:
```bash
chmod +x bin/run.sh
chmod +x scripts/install_pk_system.sh
```

## Updating

To update the project and dependencies:

```bash
# Pull latest changes
git pull

# Update dependencies
uv sync --upgrade

# Or reinstall pk_system
python scripts/install_pk_system.py --upgrade
```

## Uninstallation

To remove the project:

1. Deactivate virtual environment: `deactivate`
2. Delete project directory: `rm -rf auto_flow` (Linux/WSL) or delete folder (Windows)
3. Remove from PATH if added

## Platform-Specific Notes

### Windows

- Use `run.bat` or `run.lnk` for execution
- Ensure PowerShell execution policy allows scripts: `Set-ExecutionPolicy RemoteSigned`

### Linux/WSL

- Use `bin/run.sh` for execution
- May need to install additional dependencies: `sudo apt install python3-venv`

### macOS

- Similar to Linux installation
- May need to install Xcode Command Line Tools: `xcode-select --install`

## Next Steps

After installation:
1. Read [README.md](../README.md) for usage instructions
2. Check [API.md](API.md) for function documentation
3. Review [ARCHITECTURE.md](ARCHITECTURE.md) for system overview
4. Start creating your own wrappers!

