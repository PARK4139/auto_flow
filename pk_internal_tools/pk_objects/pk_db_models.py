import json
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import TypeDecorator
from datetime import datetime

# This custom type allows storing JSON data in a TEXT column,
# ensuring data is serialized/deserialized automatically.
class Json(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None

# Base class for declarative class definitions
Base = declarative_base()

class PkGenericState(Base):
    """
    A generic table to store key-value state information, where the value is a JSON object.
    """
    __tablename__ = "pk_generic_states"

    state_key = Column(String, primary_key=True, index=True)
    state_value = Column(Json)

    def __repr__(self):
        return f"<PkGenericState(state_key='{self.state_key}')>"


class PkMediaFileState(Base):
    """
    A table to store the state of individual media files (e.g., in LosslessCut).
    Tracks whether a file is idle, loaded, or played.
    """
    __tablename__ = "pk_media_file_states"

    file_path = Column(String, primary_key=True, index=True)
    status = Column(String, default="idle") # e.g., "idle", "loaded", "played"
    window_title = Column(String, nullable=True) # Actual window title when loaded/playing
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<PkMediaFileState(file_path='{self.file_path}', status='{self.status}')>"

    def to_dict(self):
        return {
            "file_path": self.file_path,
            "status": self.status,
            "window_title": self.window_title,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }

