import asyncio
import logging
try:
    import chip.native
    from chip.ChipDeviceCtrl import ChipDeviceController
    from chip.clusters import OnOff
    from chip.FabricAdmin import FabricAdmin
    from chip.CertificateAuthority import CertificateAuthorityManager
except ImportError:
    print("오류: 'chip' 모듈(Matter SDK 파이썬 바인딩)을 찾을 수 없습니다.")
    print("이 모듈은 일반적으로 pip/uv를 통해 설치되지 않고, 공식 Matter SDK의 일부로 설치됩니다.")
    print("Matter 개발 환경이 올바르게 설정되어 있고 파이썬 바인딩이 빌드 및 설치되었는지 확인해주세요.")
    print("설치 지침은 공식 Matter SDK 문서를 참조하십시오.")
    import sys
    sys.exit(1)

# 제어할 Matter 기기의 정보 (수정 필요 시 여기에만)
# pk_option
NODE_ID_TO_CONTROL = 111
FABRIC_ID = 1

# 로깅 설정
logging.basicConfig(level=logging.INFO)

async def turn_on_plug():
    """
    Matter 스마트 플러그를 찾아 전원을 웁니다.
    """
    ca_manager = CertificateAuthorityManager()
    await ca_manager.LoadAuthoritiesFromStorage()
    
    # FabricAdmin을 사용하여 컨트롤러 생성
    fabric_admin = FabricAdmin(ca_manager.GetFabricAdmin())
    dev_ctrl = fabric_admin.NewController()
    
    try:
        logging.info(f"Resolving node {NODE_ID_TO_CONTROL} on fabric {FABRIC_ID}...")
        # 노드 ID를 사용하여 기기의 IP 주소를 동적으로 찾습니다.
        resolved_node = await dev_ctrl.ResolveNode(FABRIC_ID, NODE_ID_TO_CONTROL)
        
        if not resolved_node:
            logging.error(f"Could not resolve node {NODE_ID_TO_CONTROL}. Make sure it is on the network.")
            return

        logging.info(f"Node {NODE_ID_TO_CONTROL} resolved to IP: {resolved_node.ipAddress}")

        # OnOff 클러스터의 'On' 명령을 전송합니다.
        # 엔드포인트 0은 일반적으로 유틸리티 클러스터를 포함하며, 실제 OnOff 클러스터는 다른 엔드포인트(예: 1)에 있을 수 있습니다.
        # 기기 설명서에 따라 엔드포인트 ID를 확인해야 할 수 있습니다.
        endpoint_id = 1 
        logging.info(f"Sending 'On' command to node {NODE_ID_TO_CONTROL}, endpoint {endpoint_id}...")
        await dev_ctrl.SendCommand(NODE_ID_TO_CONTROL, endpoint_id, OnOff.Commands.On())
        
        logging.info("Successfully sent 'On' command to the smart plug.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        logging.info("Shutting down the controller.")
        ca_manager.Shutdown()
        dev_ctrl.Shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(turn_on_plug())
    except KeyboardInterrupt:
        logging.info("Cancelled by user.")
