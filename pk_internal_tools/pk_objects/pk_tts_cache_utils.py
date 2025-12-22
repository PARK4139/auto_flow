
import re
from pathlib import Path
import logging

from pk_internal_tools.pk_objects.pk_directories import D_TTS_CACHE


def sanitize_text_for_file_name(text: str, max_length: int = 50) -> str:
    sanitized = re.sub(r'[^a-zA-Z0-9가-힣\s]', '', text).strip()
    sanitized = sanitized.replace(' ', '_')
    return sanitized[:max_length]

# This function can be used by the backends to know where to save files
def get_cache_path_for_backend(text: str, voice_config, backend_name: str) -> Path:
    cache_dir = D_TTS_CACHE
    sanitized_text = sanitize_text_for_file_name(text)
    
    if backend_name == 'gtts':
        file_name = f"gtts_{sanitized_text}_{voice_config.language}.mp3"
    elif backend_name == 'elevenlabs':
        file_name = f"elevenlabs_{sanitized_text}.mp3"
    else:
        raise ValueError(f"Unknown backend: {backend_name}")
        
    return cache_dir / file_name

# This function can be used by the client to find a file without knowing the backend
def find_existing_cache_path(text: str, language: str = "ko") -> str | None:
    cache_dir = D_TTS_CACHE
    sanitized_text = sanitize_text_for_file_name(text)
    
    possible_file_names = [
        f"gtts_{sanitized_text}_{language}.mp3",
        f"elevenlabs_{sanitized_text}.mp3"
    ]
    
    for file_name in possible_file_names:
        potential_path = cache_dir / file_name
        if potential_path.exists() and potential_path.stat().st_size > 0:
            return str(potential_path)
    return None
