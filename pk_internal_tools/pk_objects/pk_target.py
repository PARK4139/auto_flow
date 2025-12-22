from typing import Optional

from pk_internal_tools.pk_objects.pk_identifier import PkIdentifier


class PkTarget(PkIdentifier):
    def __init__(
            self,
            identifier=None,
            ip=None,
            pw=None,
            hostname=None,
            port=None,
            user_name=None,
            f_local_ssh_public_key=None,
            f_local_ssh_private_key=None,
            nick_name=None,
            distro_name=None,
            uvicorn_path: Optional[str] = None,  # Add uvicorn_path parameter
    ):
        if identifier is None:
            raise ValueError("identifier는 반드시 초기화되어야 합니다.")

        if nick_name is None:
            nick_name = f"nick_name_{identifier.value}"
        super().__init__(identifier=identifier, nick_name=nick_name)
        self._ip = ip
        self._pw = pw
        self._hostname = hostname
        self._port = port
        self._user_n = user_name
        self._f_local_ssh_public_key = f_local_ssh_public_key
        self._f_local_ssh_private_key = f_local_ssh_private_key
        self._distro_name = distro_name
        self._uvicorn_path = uvicorn_path  # Initialize _uvicorn_path

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        self._ip = value

    @property
    def distro_name(self):
        return self._distro_name

    @distro_name.setter
    def distro_name(self, value):
        self._distro_name = value

    @property
    def pw(self):
        return self._pw

    @pw.setter
    def pw(self, value):
        self._pw = value

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, value):
        self._hostname = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def user_name(self):
        return self._user_n

    @user_name.setter
    def user_name(self, value):
        self._user_n = value

    @property
    def f_local_ssh_public_key(self):
        return self._f_local_ssh_public_key

    @f_local_ssh_public_key.setter
    def f_local_ssh_public_key(self, value):
        self._f_local_ssh_public_key = value

    @property
    def f_local_ssh_private_key(self):
        return self._f_local_ssh_private_key

    @f_local_ssh_private_key.setter
    def f_local_ssh_private_key(self, value):
        self._f_local_ssh_private_key = value

    _uvicorn_path: Optional[str] = None  # Uvicorn 실행 파일 경로

    @property
    def uvicorn_path(self):
        return self._uvicorn_path

    @uvicorn_path.setter
    def uvicorn_path(self, value: Optional[str]):
        self._uvicorn_path = value

    def to_dict(self):
        """Converts the PkTarget object to a dictionary."""
        return {
            "identifier": self.identifier.value if hasattr(self.identifier, 'value') else self.identifier,
            "ip": self.ip,
            "pw": self.pw,
            "hostname": self.hostname,
            "port": self.port,
            "user_n": self.user_name,
            "f_local_ssh_public_key": str(self.f_local_ssh_public_key) if self.f_local_ssh_public_key else None,
            "f_local_ssh_private_key": str(self.f_local_ssh_private_key) if self.f_local_ssh_private_key else None,
            "nick_name": self.nick_name,
            "distro_name": self.distro_name,
            "uvicorn_path": self.uvicorn_path,
        }

    def get_home_directory(self) -> str:
        """
        원격 타겟의 사용자 홈 디렉토리 경로를 반환합니다.
        예: /home/username
        """
        if self.user_name:
            return f"/home/{self.user_name}"
        return "/home/pk" # Fallback or default
        
    def to_json(self, indent=4, ensure_ascii=False):
        """Converts the PkTarget object to a JSON string."""
        import json
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=ensure_ascii)
