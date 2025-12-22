from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class SwitchControlRequest(BaseModel):
    action: str  # "on", "off", or "toggle"
    entity_id: Optional[str] = None  # None인 경우 기본 entity 사용


class TvControlRequest(BaseModel):
    action: str  # "on", "off", or "toggle"
    entity_id: Optional[str] = None  # None인 경우 기본 entity 사용


class EntityStateResponse(BaseModel):
    entity_id: str
    state: str
    friendly_name: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None


class EntityListResponse(BaseModel):
    entities: List[EntityStateResponse]