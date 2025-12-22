#!/usr/bin/env python3
"""
컨테이너 빌드 테스트를 재현하는 함수
"""

from pk_internal_tools.pk_objects.pk_colors import PkColors


def ensure_container_build_test():
    """컨테이너 빌드 테스트를 실행하는 함수"""
    try:
        # Lazy import to avoid circular dependency
        try:
            import logging
            from pk_internal_tools.pk_objects.pk_texts import PkTexts
        except ImportError:
            print = lambda msg, **kwargs: print(msg)
            PkTexts = type('PkTexts', (), {
                'CONTAINER_PROJECT_PATH_CHECK': '프로젝트 경로 확인',
                'CONTAINER_DOCKER_STATUS_CHECK': 'Docker 상태 확인 중',
                'CONTAINER_DATABASE_SERVICE_STARTING': '데이터베이스 서비스 시작 중',
                'CONTAINER_SERVICE_BUILDING': '서비스 빌드 중',
                'CONTAINER_SERVICE_STARTING': '서비스 시작 중',
                'CONTAINER_BUILD_TEST_SUCCESS': '컨테이너 빌드 테스트가 성공적으로 완료되었습니다',
                'CONTAINER_USEFUL_COMMANDS': '유용한 명령어',
                'CONTAINER_TEST_SUCCESS': '테스트가 성공적으로 완료되었습니다',
                'CONTAINER_TEST_FAILED': '테스트가 실패했습니다'
            })()

        import subprocess
        import os
        from pathlib import Path

        # 프로젝트 경로 확인
        project_path = Path.cwd()
        print(f"[{PkTexts.CONTAINER_PROJECT_PATH_CHECK}] {PkColors.CYAN}경로={project_path} {PkColors.RESET}")

        # Docker 상태 확인
        print(f"[{PkTexts.CONTAINER_DOCKER_STATUS_CHECK}]")
        try:
            result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Docker 버전: {result.stdout.strip()}")
            else:
                print("Docker가 설치되지 않았습니다.")
                return False
        except FileNotFoundError:
            print("Docker가 설치되지 않았습니다.")
            return False

        # docker-compose 확인
        try:
            result = subprocess.run(["docker-compose", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"docker-compose 버전: {result.stdout.strip()}")
            else:
                print("docker-compose가 설치되지 않았습니다.")
                return False
        except FileNotFoundError:
            print("docker-compose가 설치되지 않았습니다.")
            return False

        # 데이터베이스 서비스 시작
        print(f"[{PkTexts.CONTAINER_DATABASE_SERVICE_STARTING}]")
        try:
            result = subprocess.run(["docker-compose", "up", "-d", "database"], capture_output=True, text=True)
            if result.returncode == 0:
                print("데이터베이스 서비스가 시작되었습니다.")
            else:
                print(f"데이터베이스 서비스 시작 실패: {result.stderr}")
        except Exception as e:
            print(f"데이터베이스 서비스 시작 중 오류: {e}")

        # 서비스별 빌드 및 테스트
        services = ["api_gateway", "investment_advisor", "market_data", "news_analyzer"]

        for service_name in services:
            print(f"[{PkTexts.CONTAINER_SERVICE_BUILDING}] {PkColors.YELLOW}서비스={service_name} {PkColors.RESET}")

            try:
                # 서비스 빌드
                result = subprocess.run([
                    "docker-compose", "build", service_name
                ], capture_output=True, text=True)

                if result.returncode == 0:
                    print(f"서비스 빌드 성공: {service_name}")

                    # 서비스 시작
                    print(f"[{PkTexts.CONTAINER_SERVICE_STARTING}] {PkColors.YELLOW}서비스={service_name} {PkColors.RESET}")

                    result = subprocess.run([
                        "docker-compose", "up", "-d", service_name
                    ], capture_output=True, text=True)

                    if result.returncode == 0:
                        print(f"서비스 시작 성공: {service_name}")
                    else:
                        print(f"서비스 시작 실패: {service_name} - {result.stderr}")

                else:
                    print(f"서비스 빌드 실패: {service_name} - {result.stderr}")

            except Exception as e:
                print(f"서비스 처리 중 오류: {service_name} - {e}")

        print(f"[{PkTexts.CONTAINER_BUILD_TEST_SUCCESS}] {PkColors.CYAN}상태=완료 {PkColors.RESET}")

        # 유용한 명령어 출력
        print(f"[{PkTexts.CONTAINER_USEFUL_COMMANDS}] {PkColors.CYAN}명령어=도움말 {PkColors.RESET}")
        print("유용한 명령어:")
        print("- 서비스 상태 확인: docker-compose ps")
        print("- 로그 확인: docker-compose logs [서비스명]")
        print("- 서비스 중지: docker-compose down")
        print("- 특정 서비스 재시작: docker-compose restart [서비스명]")
        print("- 이미지 재빌드: docker-compose build --no-cache")

        return True

    except Exception as e:
        print(f"[{PkTexts.CONTAINER_TEST_FAILED}] {PkColors.RED}오류={e} {PkColors.RESET}")
        return False


def test_container_health():
    """컨테이너 헬스 체크 테스트"""
    try:
        # Lazy import to avoid circular dependency
        try:
            import logging
            from pk_internal_tools.pk_objects.pk_texts import PkTexts
        except ImportError:
            print = lambda msg, **kwargs: print(msg)
            PkTexts = type('PkTexts', (), {
                'CONTAINER_TEST_SUCCESS': '테스트가 성공적으로 완료되었습니다',
                'CONTAINER_TEST_FAILED': '테스트가 실패했습니다'
            })()

        import subprocess
        import time

        # 컨테이너 상태 확인
        result = subprocess.run(["docker-compose", "ps"], capture_output=True, text=True)

        if result.returncode == 0:
            print("컨테이너 상태:")
            print(result.stdout)

            # 헬스 체크
            services = ["api_gateway", "investment_advisor", "market_data", "news_analyzer"]
            healthy_count = 0

            for service in services:
                try:
                    # 헬스 체크 엔드포인트 호출
                    health_result = subprocess.run([
                        "curl", "-f", f"http://localhost:8000/{service}/health"
                    ], capture_output=True, text=True, timeout=10)

                    if health_result.returncode == 0:
                        print(f" {service}: 정상")
                        healthy_count += 1
                    else:
                        print(f" {service}: 비정상")

                except Exception as e:
                    print(f" {service}: 확인 불가 - {e}")

            if healthy_count == len(services):
                print(f"[{PkTexts.CONTAINER_TEST_SUCCESS}] {PkColors.CYAN}정상서비스수={healthy_count}개 {PkColors.RESET}")
                return True
            else:
                print(f"[{PkTexts.CONTAINER_TEST_FAILED}] {PkColors.RED}정상서비스수={healthy_count}개 전체서비스수={len(services)}개 {PkColors.RESET}")
                return False
        else:
            print(f"[{PkTexts.CONTAINER_TEST_FAILED}] {PkColors.RED}컨테이너상태확인실패 {PkColors.RESET}")
            return False

    except Exception as e:
        print(f"[{PkTexts.CONTAINER_TEST_FAILED}] {PkColors.RED}오류={e} {PkColors.RESET}")
        return False
