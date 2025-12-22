from enum import Enum, auto

class SetupOpsForEnsurePkWebServerExecuted(Enum):
    """
    ensure_pk_web_server_executed 함수에 대한 옵션을 정의합니다.
    """
    HOST = "HOST"
    PORT = "PORT"
    REMOTE_TARGET = "REMOTE_TARGET"

