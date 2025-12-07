import os
from pathlib import Path
from typing import Dict, Optional, Any

import logging

from pk_internal_tools.pk_objects.pk_directories import D_PK_RECYCLE_BIN


class ConfigManager:
    def __init__(self):
        self.config = {}
        self.config_path = self._find_config_file()
        self._load_config()

    def _find_config_file(self) -> Path:
        config_path = D_PK_RECYCLE_BIN / "temp.toml"
        logging.info(f"TTS 설정 파일 경로: {config_path}")
        return config_path


    def _load_config(self):
        if self.config_path and self.config_path.exists():
            try:
                from pk_internal_tools.pk_functions.get_data_from_f_toml import get_data_from_f_toml
                self.config = get_data_from_f_toml(self.config_path)
                logging.info(f"TTS 설정 로드 완료: {self.config_path}")
            except Exception as e:
                logging.error(f"TTS 설정 로드 실패: {e}")
                self.config = {}
        else:
            # 기본 설정
            self.config = self._get_default_config()
            logging.info("기본 TTS 설정 사용")

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "tts_services": {
                "elevenlabs": {
                    "enabled": False,
                    "api_key": "",
                    "default_voice": "Rachel",
                    "model": "eleven_monolingual_v1"
                },
                "azure": {
                    "enabled": False,
                    "api_key": "",
                    "region": ""
                },
                "aws_polly": {
                    "enabled": False,
                    "access_key_id": "",
                    "secret_access_key": "",
                    "region": ""
                }
            },
            "usage_limits": {
                "elevenlabs": {
                    "monthly_limit": 10000,
                    "reset_day": 1
                }
            }
        }

    def get_service_config(self, service_name: str) -> Optional[Dict[str, Any]]:
        """특정 서비스 설정 반환"""
        services = self.config.get("tts_services", {})
        return services.get(service_name)

    def is_service_enabled(self, service_name: str) -> bool:
        """서비스 활성화 여부 확인"""
        service_config = self.get_service_config(service_name)
        if not service_config:
            return False

        return service_config.get("enabled", False)

    def get_api_key(self, service_name: str) -> Optional[str]:
        """서비스 API 키 반환"""
        service_config = self.get_service_config(service_name)
        if not service_config:
            return None

        return service_config.get("api_key", "")

    def get_voice_config(self, service_name: str) -> Dict[str, Any]:
        """서비스 음성 설정 반환"""
        service_config = self.get_service_config(service_name)
        if not service_config:
            return {}

        return {
            "default_voice": service_config.get("default_voice", ""),
            "model": service_config.get("model", ""),
            "region": service_config.get("region", "")
        }

    def get_usage_limit(self, service_name: str) -> Optional[Dict[str, Any]]:
        """서비스 사용량 한도 반환"""
        limits = self.config.get("usage_limits", {})
        return limits.get(service_name)

    def create_user_config_template(self):
        """사용자 설정 파일 템플릿 생성 (TOML 형식)"""
        target_path = self.config_path.parent

        if target_path:
            target_path.mkdir(parents=True, exist_ok=True)

            template_config = {
                "tts_services": {
                    "elevenlabs": {
                        "enabled": True,
                        "api_key": "여기에_실제_API_키_입력",
                        "default_voice": "Rachel",
                        "model": "eleven_monolingual_v1"
                    }
                },
                "usage_limits": {
                    "elevenlabs": {
                        "monthly_limit": 10000,
                        "reset_day": 1
                    }
                }
            }

            try:
                # 기존 TOML 저장 함수 활용
                from pk_internal_tools.pk_functions.add_data_to_f_toml import add_data_to_f_toml
                add_data_to_f_toml(self.config_path, template_config)

                logging.info(f"사용자 설정 템플릿 생성됨: {self.config_path}")
                print(f"✅ TOML 설정 파일이 생성되었습니다: {self.config_path}")
                print("📝 이 파일에 실제 API 키를 입력하세요!")

            except Exception as e:
                logging.error(f"TOML 설정 파일 생성 실패: {e}")
                print(f"❌ TOML 설정 파일 생성 실패: {e}")

    def prompt_user_for_api_key(self, service_name: str = "elevenlabs"):
        """사용자로부터 API 키 입력받아 TOML 파일에 저장"""
        print(f"\n🔑 {service_name} API 키 설정")
        print("=" * 40)

        # 현재 설정 확인
        current_api_key = self.get_api_key(service_name)
        if current_api_key and current_api_key != "여기에_실제_API_키_입력":
            print(f"현재 설정된 API 키: {current_api_key[:10]}...")
            response = input("새로운 API 키로 변경하시겠습니까? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("API 키 변경을 취소했습니다.")
                return False

        # 새 API 키 입력
        new_api_key = input(f"{service_name} API 키를 입력하세요: ").strip()

        if not new_api_key:
            print("API 키가 입력되지 않았습니다.")
            return False

        if len(new_api_key) < 10:
            print("API 키가 너무 짧습니다. 올바른 API 키를 입력해주세요.")
            return False

        try:
            # TOML 파일에 API 키 저장
            api_key_data = {
                "tts_services": {
                    service_name: {
                        "enabled": True,
                        "api_key": new_api_key
                    }
                }
            }

            # 기존 TOML 저장 함수 활용
            from pk_internal_tools.pk_functions.add_data_to_f_toml import add_data_to_f_toml
            add_data_to_f_toml(self.config_path, api_key_data)

            # 메모리에도 업데이트
            if "tts_services" not in self.config:
                self.config["tts_services"] = {}
            if service_name not in self.config["tts_services"]:
                self.config["tts_services"][service_name] = {}

            self.config["tts_services"][service_name]["enabled"] = True
            self.config["tts_services"][service_name]["api_key"] = new_api_key

            print(f"✅ {service_name} API 키가 성공적으로 저장되었습니다!")
            return True

        except Exception as e:
            logging.error(f"API 키 저장 실패: {e}")
            print(f"❌ API 키 저장 실패: {e}")
            return False

    def ensure_api_key_exists(self, service_name: str = "elevenlabs"):
        """API 키가 없으면 사용자 입력을 받아 설정"""
        api_key = self.get_api_key(service_name)

        if not api_key or api_key == "여기에_실제_API_키_입력":
            print(f"\n⚠️ {service_name} API 키가 설정되지 않았습니다.")
            print("🔧 API 키를 입력해주세요.")

            if self.prompt_user_for_api_key(service_name):
                # 설정 다시 로드
                self._load_config()
                return True
            else:
                return False
        else:
            return True

    def validate_config(self) -> Dict[str, Any]:
        """설정 유효성 검사"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "enabled_services": []
        }

        services = self.config.get("tts_services", {})

        for service_name, service_config in services.items():
            if service_config.get("enabled", False):
                validation_result["enabled_services"].append(service_name)

                # API 키 검사
                api_key = service_config.get("api_key", "")
                if not api_key or api_key == "여기에_실제_API_키_입력":
                    validation_result["errors"].append(f"{service_name}: API 키가 설정되지 않음")
                    validation_result["valid"] = False
                elif len(api_key) < 10:
                    validation_result["warnings"].append(f"{service_name}: API 키가 너무 짧음")

        return validation_result

    def _save_config(self):
        """TOML 설정 파일 저장"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

            # 기존 TOML 저장 함수 활용
            from pk_internal_tools.pk_functions.add_data_to_f_toml import add_data_to_f_toml
            add_data_to_f_toml(self.config_path, self.config)

        except Exception as e:
            logging.error(f"TOML 설정 저장 실패: {e}")


_config_manager = None


def get_pk_tts_config_manager() -> ConfigManager:
    """전역 TTSConfigManager 인스턴스 반환"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
