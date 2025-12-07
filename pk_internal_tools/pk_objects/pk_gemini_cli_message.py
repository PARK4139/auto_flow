from dataclasses import dataclass, field
import json
from dataclasses_json import dataclass_json
from typing import Optional

@dataclass_json
@dataclass
class GeminiCliMessage:
    """
    Represents a message for headless communication with the Gemini CLI.
    """
    prompt: Optional[str] = None
    response: Optional[str] = None
    status: str = "pending"  # e.g., "pending", "success", "error"
    error_message: Optional[str] = None

    def to_json(self) -> str:
        """
        Serializes the object to a JSON string.
        
        Returns:
            str: The JSON string representation of the object.
        """
        return self.to_json(indent=4, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_string: str) -> 'GeminiCliMessage':
        """
        Deserializes a JSON string to a GeminiCliMessage object.

        Args:
            json_string (str): The JSON string to deserialize.

        Returns:
            GeminiCliMessage: The deserialized GeminiCliMessage object.
        """
        return cls.from_dict(json.loads(json_string))
