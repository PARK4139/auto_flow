#!/usr/bin/env python3

"""
Docker 기반 Matter 서버 관리 함수
- is_matter_server_running: 서버 실행 여부 확인
- ensure_matter_server_running: 서버 실행 보장
"""

import asyncio
import logging
from typing import Tuple, Optional

async def is_matter_server_running() -> bool:
    """Matter 서버 실행 상태 확인"""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:5580", timeout=aiohttp.ClientTimeout(total=2)) as response:
                return response.status == 200
    except Exception as e:
        return False

async def ensure_matter_server_running() -> Tuple[bool, None]:
    """
    Docker를 사용하여 Matter 서버 실행을 보장합니다.
    이미 실행 중이면 True를 반환하고, 아니면 시작을 시도합니다.
    """
    if await is_matter_server_running():
        logging.info("Matter 서버가 이미 실행 중입니다.")
        return True, None

    logging.info("Docker를 사용하여 Matter 서버를 시작합니다...")
    try:
        from pk_internal_tools.pk_functions.ensure_matter_docker_control import DockerMatterController
        
        controller = DockerMatterController()
        success = await controller.setup_docker_environment()
        
        if success:
            logging.info("Docker Matter 서버가 성공적으로 시작되었습니다.")
            return True, None
        else:
            logging.error("Docker Matter 서버 시작에 실패했습니다.")
            return False, None
            
    except Exception as e:
        logging.error(f"Matter 서버 시작 중 예외 발생: {e}")
        return False, None

if __name__ == '__main__':
    async def main():
        logging.basicConfig(level=logging.INFO)
        
        print("Matter 서버 상태 확인...")
        running = await is_matter_server_running()
        print(f"서버 실행 중: {running}")
        
        if not running:
            print("Matter 서버 시작 시도...")
            success, _ = await ensure_matter_server_running()
            print(f"서버 시작 성공: {success}")
            
            if success:
                print("서버 상태 다시 확인...")
                running = await is_matter_server_running()
                print(f"서버 실행 중: {running}")

    asyncio.run(main())
