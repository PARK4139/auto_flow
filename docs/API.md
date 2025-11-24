# API Documentation

## Core Functions

### `ensure_wrapper_started(pk_wrapper_files=None, mode_window_front=False)`

Main wrapper launcher function that provides interactive selection and execution of wrapper scripts.

**Parameters**:
- `pk_wrapper_files` (list, optional): Pre-defined list of wrapper files. If None, automatically discovers wrappers from configured directories.
- `mode_window_front` (bool, optional): If True, brings the execution window to front after launch.

**Returns**:
- `bool`: True if wrapper was executed successfully, False otherwise.

**Example**:
```python
from source.functions.ensure_wrapper_started import ensure_wrapper_started

# Interactive selection
ensure_wrapper_started()

# With specific files
files = ["path/to/wrapper1.py", "path/to/wrapper2.py"]
ensure_wrapper_started(pk_wrapper_files=files)
```

---

### `ensure_ehr_login(ehr_url=None)`

Opens EHR login page in browser and focuses the window.

**Parameters**:
- `ehr_url` (str, optional): EHR login URL. If None, reads from `EHR_URL` environment variable.

**Raises**:
- `ValueError`: If `EHR_URL` environment variable is not set and `ehr_url` is None.

**Example**:
```python
from source.functions.ensure_ehr_login import ensure_ehr_login

# Use environment variable
ensure_ehr_login()

# Or specify URL directly
ensure_ehr_login("https://ehr.example.com")
```

---

### `ensure_ekiss_login(ekiss_url=None)`

Opens eKiss login page in browser and focuses the window.

**Parameters**:
- `ekiss_url` (str, optional): eKiss login URL. If None, reads from `EKISS_URL` environment variable.

**Raises**:
- `ValueError`: If `EKISS_URL` environment variable is not set and `ekiss_url` is None.

---

### `ensure_huvitz_mail_opened(mail_url=None)`

Opens Huvitz mail in browser or mail client.

**Parameters**:
- `mail_url` (str, optional): Mail URL. If None, reads from `HUVITZ_MAIL_URL` environment variable.

**Raises**:
- `ValueError`: If `HUVITZ_MAIL_URL` environment variable is not set and `mail_url` is None.

---

### `ensure_f_LM_100_spindle_reliability_test_report_opened(file_path=None)`

Opens LM-100 spindle reliability test report Excel file.

**Parameters**:
- `file_path` (str or Path, optional): Path to Excel file. If None, searches for latest file in `etc/archived/` directory.

**Returns**:
- `bool`: True if file was opened successfully, False otherwise.

**Example**:
```python
from source.functions.ensure_f_LM_100_spindle_reliability_test_report_opened import \
    ensure_f_LM_100_spindle_reliability_test_report_opened

# Auto-search for latest file
ensure_f_LM_100_spindle_reliability_test_report_opened()

# Or specify path
ensure_f_LM_100_spindle_reliability_test_report_opened("path/to/file.xlsx")
```

---

### `ensure_L_CAM_milling_or_grinding_data_sent(data_file_path=None, recipient_email=None, subject=None, body=None)`

Sends L-CAM milling or grinding data via email.

**Parameters**:
- `data_file_path` (str or Path, required): Path to data file to send.
- `recipient_email` (str, optional): Recipient email address. If None, reads from `L_CAM_RECIPIENT_EMAIL` environment variable.
- `subject` (str, optional): Email subject. If None, generates default subject.
- `body` (str, optional): Email body. If None, generates default body.

**Returns**:
- `bool`: True if email client was opened successfully, False otherwise.

**Raises**:
- `ValueError`: If `L_CAM_RECIPIENT_EMAIL` environment variable is not set and `recipient_email` is None.

**Note**: File path is copied to clipboard for manual attachment.

---

### `ensure_d_pk_system_opened()`

Opens pk_system directory in file explorer.

**Returns**:
- `bool`: True if directory was opened successfully, False otherwise.

---

### `get_pk_path()`

Gets the pk_system root directory path.

**Returns**:
- `Path`: pk_system root directory path, or None if not found.

---

## Constants

### Directory Paths (`source.constants.directory_paths`)

- `D_PROJECT_ROOT_PATH`: Project root directory
- `D_SOURCE_PATH`: Source directory
- `D_FUNCTIONS_PATH`: Functions directory
- `D_WRAPPERS_PATH`: Wrappers directory
- `D_HUVITS_WRAPPERS_PATH`: Huvitz wrappers directory
- `D_JUNG_HOON_PARK_WRAPPERS_PATH`: Personal wrappers directory
- `D_DOWNLOADS_PATH`: User downloads directory

### File Paths (`source.constants.file_paths`)

- `F_GITIGNORE_PATH`: .gitignore file path
- `F_ENV_PATH`: .env file path
- `F_PYPROJECT_TOML_PATH`: pyproject.toml file path
- And more...

## Error Handling

All functions use `ensure_debug_loged_verbose(traceback)` for error logging. Errors are logged to the pk_system error log file.

## Environment Variables

Required environment variables (set in `.env` file):

- `EHR_URL`: EHR login URL
- `EKISS_URL`: eKiss login URL
- `HUVITZ_MAIL_URL`: Huvitz mail URL
- `L_CAM_RECIPIENT_EMAIL`: L-CAM data recipient email

## Dependencies

All functions depend on `pk_system` framework utilities:
- Window management
- File operations
- Logging
- Clipboard operations
- Sleep/delay functions

