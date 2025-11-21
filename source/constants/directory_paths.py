from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PK_SYSTEM_PATH = PROJECT_ROOT / "assets" / "pk_system"
PK_SYSTEM_SOURCES_PATH = PK_SYSTEM_PATH / "pk_system_sources"


D_ROOT =  Path(__file__).parent.parent
D_FUNCTIONS = D_ROOT / "functions"
D_WRAPPERS = D_FUNCTIONS