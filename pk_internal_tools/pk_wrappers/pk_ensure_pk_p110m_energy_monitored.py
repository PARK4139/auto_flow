#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 래퍼: P110M 에너지 모니터링 (Matter 1.3 지원)

사용법:
    python pk_ensure_pk_p110m_energy_monitored.py
    python pk_ensure_pk_p110m_energy_monitored.py --continuous
    python pk_ensure_pk_p110m_energy_monitored.py --threshold 1000
"""
import logging
import sys
import time
import argparse
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from pk_internal_tools.pk_functions.ensure_pk_p110m_advanced_modes import (
    get_p110m_energy_data,
    ensure_pk_p110m_energy_saving_mode,
    EnergySavingConfig,
)


def format_energy_data(energy_data: dict) -> str:
    """에너지 데이터를 읽기 쉬운 형식으로 포맷"""
    if not energy_data:
        return "에너지 데이터를 조회할 수 없습니다."
    
    lines = []
    lines.append("=" * 50)
    lines.append("P110M 에너지 모니터링 (Matter 1.3)")
    lines.append("=" * 50)
    
    if energy_data.get("power_watts") is not None:
        power = energy_data["power_watts"]
        lines.append(f"⚡ 실시간 전력: {power:.2f} W")
        
        # 전력 상태 설명
        if power < 1:
            lines.append("   상태: 대기 중 (거의 전력 사용 안 함)")
        elif power < 50:
            lines.append("   상태: 저전력 사용 중")
        elif power < 200:
            lines.append("   상태: 일반 전력 사용 중")
        elif power < 1000:
            lines.append("   상태: 고전력 사용 중")
        else:
            lines.append("   상태: ⚠️ 매우 높은 전력 사용 중")
    else:
        lines.append("⚡ 실시간 전력: N/A")
    
    if energy_data.get("energy_kwh") is not None:
        energy = energy_data["energy_kwh"]
        lines.append(f"📊 누적 에너지: {energy:.3f} kWh")
        
        # 비용 추정 (예: kWh당 150원)
        cost_per_kwh = 150  # 환경변수로 설정 가능
        estimated_cost = energy * cost_per_kwh
        lines.append(f"💰 예상 비용: {estimated_cost:,.0f}원 (kWh당 {cost_per_kwh}원 기준)")
    else:
        lines.append("📊 누적 에너지: N/A")
    
    if energy_data.get("power_entity_id"):
        lines.append(f"🔌 전력 센서: {energy_data['power_entity_id']}")
    if energy_data.get("energy_entity_id"):
        lines.append(f"📈 에너지 센서: {energy_data['energy_entity_id']}")
    
    if energy_data.get("timestamp"):
        lines.append(f"🕐 조회 시간: {energy_data['timestamp']}")
    
    lines.append("=" * 50)
    
    return "\n".join(lines)


def main() -> int:
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description="P110M 에너지 모니터링 (Matter 1.3 지원)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  # 한 번 조회
  python pk_ensure_pk_p110m_energy_monitored.py
  
  # 지속 모니터링 (5초마다)
  python pk_ensure_pk_p110m_energy_monitored.py --continuous
  
  # 전력 임계값 모니터링
  python pk_ensure_pk_p110m_energy_monitored.py --threshold 1000 --interval 60
        """
    )
    parser.add_argument(
        "--continuous", "-c",
        action="store_true",
        help="지속적으로 모니터링 (Ctrl+C로 중단)"
    )
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=5,
        help="모니터링 간격 (초, 기본값: 5)"
    )
    parser.add_argument(
        "--threshold", "-t",
        type=float,
        help="전력 임계값 (W). 이 값을 초과하면 경고"
    )
    parser.add_argument(
        "--entity-id",
        help="P110M Entity ID (예: switch.tapo_p110m_plug)"
    )
    parser.add_argument(
        "--ha-url",
        help="Home Assistant URL (예: http://119.207.161.56:8123)"
    )
    
    args = parser.parse_args()
    
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    
    try:
        if args.threshold:
            # 전력 임계값 모니터링 모드
            logging.info("전력 임계값 모니터링 모드 시작: %sW", args.threshold)
            
            config = EnergySavingConfig(
                power_threshold_watts=args.threshold,
                check_interval_seconds=args.interval,
            )
            
            def on_threshold_exceeded(state: str, data: dict):
                if state == "power_threshold_exceeded":
                    print("\n" + "!" * 50)
                    print(f"⚠️  전력 임계값 초과 경고!")
                    print(f"   현재 전력: {data['current_power']:.2f}W")
                    print(f"   임계값: {data['threshold']:.2f}W")
                    print(f"   초과량: {data['current_power'] - data['threshold']:.2f}W")
                    print("!" * 50 + "\n")
            
            ensure_pk_p110m_energy_saving_mode(
                config,
                entity_id=args.entity_id,
                ha_url=args.ha_url,
                callback=on_threshold_exceeded,
            )
        elif args.continuous:
            # 지속 모니터링 모드
            logging.info("지속 모니터링 모드 시작 (간격: %d초, Ctrl+C로 중단)", args.interval)
            
            try:
                while True:
                    energy_data = get_p110m_energy_data(
                        entity_id=args.entity_id,
                        ha_url=args.ha_url,
                    )
                    
                    # 화면 클리어 (선택사항)
                    print("\033[2J\033[H", end="")  # ANSI escape code
                    
                    print(format_energy_data(energy_data))
                    print(f"\n다음 업데이트까지 {args.interval}초 대기 중... (Ctrl+C로 중단)")
                    
                    time.sleep(args.interval)
            except KeyboardInterrupt:
                print("\n\n모니터링이 중단되었습니다.")
                return 0
        else:
            # 한 번 조회 모드
            energy_data = get_p110m_energy_data(
                entity_id=args.entity_id,
                ha_url=args.ha_url,
            )
            
            print(format_energy_data(energy_data))
            
            if not energy_data:
                logging.error("에너지 데이터를 조회할 수 없습니다.")
                logging.info("다음을 확인하세요:")
                logging.info("1. P110M이 Home Assistant에 등록되어 있는지")
                logging.info("2. Matter 1.3 펌웨어(1.3.2 이상)가 설치되어 있는지")
                logging.info("3. 에너지 센서가 생성되어 있는지")
                return 1
        
        return 0
        
    except KeyboardInterrupt:
        logging.info("사용자에 의해 중단되었습니다.")
        return 130
    except Exception as e:
        logging.error("오류 발생: %s", e, exc_info=True)
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logging.info("사용자에 의해 중단되었습니다.")
        sys.exit(130)
    except Exception as e:
        logging.error("오류 발생: %s", e, exc_info=True)
        sys.exit(1)

