#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
from datetime import datetime, date
from dataclasses import dataclass, asdict
from typing import Dict, Optional, List
import logging

@dataclass
class TTSUsage:
    """TTS 사용량 정보"""
    service_name: str
    characters_used: int
    characters_limit: int
    reset_date: str  # YYYY-MM-DD 형식
    last_used: str   # ISO 형식
    is_active: bool = True

class TTSUsageTracker:
    """TTS 서비스 사용량 추적 및 한도 관리"""
    
    def __init__(self, config_file: str = None):
        from pk_internal_tools.pk_objects.pk_directories import d_pk_logs
        if config_file is None:
            config_file = str(d_pk_logs / "tts_usage.json")
        self.config_file = config_file
        self.usage_data: Dict[str, TTSUsage] = {}
        self._load_usage_data()
        self._cleanup_expired_usage()
    
    def _load_usage_data(self):
        """사용량 데이터 로드"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for service_name, usage_dict in data.items():
                        self.usage_data[service_name] = TTSUsage(**usage_dict)
            else:
                # 기본 무료 서비스 설정
                self._initialize_default_services()
        except Exception as e:
            logging.error(f"사용량 데이터 로드 실패: {e}")
            self._initialize_default_services()
    
    def _initialize_default_services(self):
        """기본 무료 서비스 초기화"""
        today = date.today().isoformat()
        
        # ElevenLabs: 월 10,000자 (무료)
        self.usage_data["elevenlabs"] = TTSUsage(
            service_name="elevenlabs",
            characters_used=0,
            characters_limit=10000,
            reset_date=today,
            last_used=today,
            is_active=True
        )
        
        # gTTS: 무제한 (하지만 품질 낮음)
        self.usage_data["gtts"] = TTSUsage(
            service_name="gtts",
            characters_used=0,
            characters_limit=999999,
            reset_date=today,
            last_used=today,
            is_active=True
        )
        
        # pyttsx3: 무제한 (로컬)
        self.usage_data["pyttsx3"] = TTSUsage(
            service_name="pyttsx3",
            characters_used=0,
            characters_limit=999999,
            reset_date=today,
            last_used=today,
            is_active=True
        )
    
    def _save_usage_data(self):
        """사용량 데이터 저장"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({k: asdict(v) for k, v in self.usage_data.items()}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"사용량 데이터 저장 실패: {e}")
    
    def _cleanup_expired_usage(self):
        """만료된 사용량 정리 (월별 리셋)"""
        today = date.today()
        
        for service_name, usage in self.usage_data.items():
            try:
                reset_date = datetime.fromisoformat(usage.reset_date).date()
                
                # 월이 바뀌었으면 사용량 리셋
                if today.month != reset_date.month or today.year != reset_date.year:
                    usage.characters_used = 0
                    usage.reset_date = today.isoformat()
                    logging.info(f"{service_name} 사용량 리셋됨")
                    
            except Exception as e:
                logging.error(f"{service_name} 사용량 정리 실패: {e}")
        
        self._save_usage_data()
    
    def can_use_service(self, service_name: str, text_length: int) -> bool:
        """서비스 사용 가능 여부 확인"""
        if service_name not in self.usage_data:
            return False
        
        usage = self.usage_data[service_name]
        
        # 서비스가 비활성화되어 있으면 사용 불가
        if not usage.is_active:
            return False
        
        # 사용량 한도 확인
        if usage.characters_used + text_length > usage.characters_limit:
            return False
        
        return True
    
    def record_usage(self, service_name: str, text_length: int):
        """사용량 기록"""
        if service_name not in self.usage_data:
            return
        
        usage = self.usage_data[service_name]
        usage.characters_used += text_length
        usage.last_used = datetime.now().isoformat()
        
        # 한도에 도달하면 서비스 비활성화
        if usage.characters_used >= usage.characters_limit:
            usage.is_active = False
            logging.warning(f"{service_name} 무료 한도 도달! 서비스 비활성화됨")
        
        self._save_usage_data()
    
    def get_available_services(self, text_length: int) -> List[str]:
        """사용 가능한 서비스 목록 반환"""
        available = []
        
        for service_name, usage in self.usage_data.items():
            if self.can_use_service(service_name, text_length):
                available.append(service_name)
        
        return available
    
    def get_service_status(self, service_name: str) -> Optional[Dict]:
        """서비스 상태 정보 반환"""
        if service_name not in self.usage_data:
            return None
        
        usage = self.usage_data[service_name]
        remaining = usage.characters_limit - usage.characters_used
        
        return {
            "service_name": service_name,
            "characters_used": usage.characters_used,
            "characters_limit": usage.characters_limit,
            "characters_remaining": remaining,
            "reset_date": usage.reset_date,
            "last_used": usage.last_used,
            "is_active": usage.is_active,
            "usage_percentage": (usage.characters_used / usage.characters_limit) * 100
        }
    
    def get_all_services_status(self) -> Dict[str, Dict]:
        """모든 서비스 상태 정보 반환"""
        return {name: self.get_service_status(name) for name in self.usage_data.keys()}
    
    def reset_service_usage(self, service_name: str):
        """특정 서비스 사용량 수동 리셋"""
        if service_name in self.usage_data:
            usage = self.usage_data[service_name]
            usage.characters_used = 0
            usage.is_active = True
            usage.reset_date = date.today().isoformat()
            self._save_usage_data()
            logging.info(f"{service_name} 사용량 수동 리셋됨")
    
    def add_service(self, service_name: str, characters_limit: int):
        """새로운 서비스 추가"""
        today = date.today().isoformat()
        
        self.usage_data[service_name] = TTSUsage(
            service_name=service_name,
            characters_used=0,
            characters_limit=characters_limit,
            reset_date=today,
            last_used=today,
            is_active=True
        )
        
        self._save_usage_data()
        logging.info(f"새로운 서비스 추가됨: {service_name} (한도: {characters_limit}자)")

# 전역 인스턴스
_usage_tracker = None

def get_usage_tracker() -> TTSUsageTracker:
    """전역 TTSUsageTracker 인스턴스 반환"""
    global _usage_tracker
    if _usage_tracker is None:
        _usage_tracker = TTSUsageTracker()
    return _usage_tracker
