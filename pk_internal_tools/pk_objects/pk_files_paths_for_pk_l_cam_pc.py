from pathlib import Path

from pk_internal_tools.pk_objects.pk_directories_paths_for_pk_l_cam_pc import D_PROJECT_ROOT_PATH, D_JUNG_HOON_PARK_WRAPPERS_PATH

F_GITIGNORE_PATH = D_PROJECT_ROOT_PATH / ".gitignore"
F_GITIGNORE_PUBLIC_PATH = D_PROJECT_ROOT_PATH / ".gitignore_for_public"
F_GEMINI_MD_PATH = D_PROJECT_ROOT_PATH / "GEMINI.md"
F_PYPROJECT_TOML_PATH = D_PROJECT_ROOT_PATH / "pyproject.toml"
F_RUN_CMD_PATH = D_PROJECT_ROOT_PATH / "run.cmd"
F_SETUP_CMD_PATH = D_PROJECT_ROOT_PATH / "setup.cmd"
F_TEARDOWN_CMD_PATH = D_PROJECT_ROOT_PATH / "teardown.cmd"
F_GITATTRIBUTES_PATH = D_PROJECT_ROOT_PATH / ".gitattributes"
F_ENV_PATH = Path(D_PROJECT_ROOT_PATH).parent / '.env'
F_AUTO_FLOW_터미널_실행_PY = D_JUNG_HOON_PARK_WRAPPERS_PATH / "auto_flow_터미널_실행.py"
