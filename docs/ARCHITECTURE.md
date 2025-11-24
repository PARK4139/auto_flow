# Architecture Documentation

## Overview

`auto_flow` is designed as a continuous automation wrapper system that provides an interactive interface for executing automation scripts. The architecture is built around the concept of wrapper scripts organized by category.

## Core Components

### 1. Main Entry Point (`__main__.py`)

The application entry point that runs an infinite loop:

```python
while True:
    ensure_wrapper_started()
    ensure_slept(milliseconds=50)
```

**Responsibilities**:
- Initialize the wrapper selection system
- Handle keyboard interrupts (Ctrl+C)
- Error handling and logging

### 2. Wrapper Launcher (`ensure_wrapper_started.py`)

The core function that manages wrapper selection and execution.

**Key Features**:
- Two-stage selection process (directory → file)
- fzf integration for interactive selection
- History management for quick access
- Performance optimization with caching

**Selection Flow**:
1. User selects wrapper category (directory)
2. If multiple files exist, user selects specific script
3. Selected script executes in new console window
4. History is saved for next run

### 3. Wrapper Organization

Wrappers are organized by category in `source/wrappers/`:

- **Huvitz/**: Business-related automations (EHR, eKiss, mail, etc.)
- **Jung_Hoon_Park/**: Personal automation scripts
- **python mission/**: Python tutorial and educational scripts

### 4. Core Functions (`source/functions/`)

Reusable automation functions that wrappers can utilize:

- `ensure_ehr_login.py`: Opens EHR login page
- `ensure_ekiss_login.py`: Opens eKiss login page
- `ensure_huvitz_mail_opened.py`: Opens Huvitz mail
- `ensure_f_LM_100_spindle_reliability_test_report_opened.py`: Opens Excel files
- `ensure_L_CAM_milling_or_grinding_data_sent.py`: Sends data via email

## Data Flow

```
User Input
    ↓
ensure_wrapper_started()
    ↓
Category Selection (fzf)
    ↓
File Selection (fzf, if multiple files)
    ↓
Script Execution (subprocess.Popen)
    ↓
History Save
    ↓
Loop (50ms delay)
```

## Dependencies

### External

- **pk_system**: Core automation framework
  - Installed via Git: `git+https://github.com/PARK4139/pk_system.git`
  - Provides: window management, file operations, logging, etc.

### Internal

- **Python Standard Library**: sys, os, subprocess, pathlib, etc.
- **fzf**: Interactive file selector (optional)

## Configuration Management

### Path Constants (`source/constants/directory_paths.py`)

Centralized path definitions:
- `D_PROJECT_ROOT_PATH`: Project root directory
- `D_WRAPPERS_PATH`: Wrappers directory
- `D_HUVITS_WRAPPERS_PATH`: Huvitz wrappers
- `D_JUNG_HOON_PARK_WRAPPERS_PATH`: Personal wrappers

### Environment Variables

Sensitive configuration stored in `.env`:
- URLs for web services
- Email addresses
- API endpoints

## Error Handling

- **Import Errors**: Handled with try-except blocks and user-friendly messages
- **Execution Errors**: Logged via `ensure_debug_loged_verbose()`
- **User Cancellation**: Graceful handling of Ctrl+C

## Performance Considerations

- **Caching**: Wrapper file lists are cached
- **Lazy Loading**: Functions imported only when needed
- **Minimal Delay**: 50ms between loop iterations
- **Fast Selection**: fzf for ultra-fast file selection

## Security

- **Environment Variables**: Sensitive data stored in `.env` (not in Git)
- **Path Validation**: All paths validated before use
- **Subprocess Execution**: Safe execution of wrapper scripts

## Extension Points

### Adding New Categories

1. Create directory in `source/wrappers/`
2. Add path constant in `directory_paths.py`
3. Update `ensure_wrapper_started.py` to include new path

### Adding New Functions

1. Create function file in `source/functions/`
2. Follow `ensure_` naming convention
3. Use `pk_system` utilities for automation
4. Add error handling with `ensure_debug_loged_verbose()`

## Future Enhancements

- Plugin system for dynamic wrapper loading
- Configuration file for custom categories
- Web interface for remote execution
- Logging and analytics dashboard

