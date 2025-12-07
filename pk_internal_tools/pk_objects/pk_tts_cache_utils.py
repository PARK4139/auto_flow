
import re
from pathlib import Path
import logging

# This should be the single source of truth for the cache directory
def get_pk_tts_cache_dir() -> Path:
    try:
        from pk_internal_tools.pk_objects.pk_directories import d_pk_logs
        if d_pk_logs is None:
            logging.error("d_pk_logs is None. Falling back to default cache path.")
            return Path("./pk_logs/pk_tts_cache") # Fallback if d_pk_logs is None
        return d_pk_logs / "pk_tts_cache"
    except ImportError as e:
        logging.error(f"get_pk_tts_cache_dir: Failed to import d_pk_logs: {e}. Falling back to default cache path.")
        return Path("./pk_logs/pk_tts_cache") # Fallback if import fails
    except Exception as e: # Catch any other potential errors during path construction
        logging.error(f"get_pk_tts_cache_dir: An unexpected error occurred: {e}. Falling back to default cache path.")
        return Path("./pk_logs/pk_tts_cache")

def sanitize_text_for_filename(text: str, max_length: int = 50) -> str:
    sanitized = re.sub(r'[^a-zA-Z0-9가-힣\s]', '', text).strip()
    sanitized = sanitized.replace(' ', '_')
    return sanitized[:max_length]

# This function can be used by the backends to know where to save files
def get_cache_path_for_backend(text: str, voice_config, backend_name: str) -> Path:
    cache_dir = get_pk_tts_cache_dir()
    sanitized_text = sanitize_text_for_filename(text)
    
    if backend_name == 'gtts':
        filename = f"gtts_{sanitized_text}_{voice_config.language}.mp3"
    elif backend_name == 'elevenlabs':
        filename = f"elevenlabs_{sanitized_text}.mp3"
    else:
        raise ValueError(f"Unknown backend: {backend_name}")
        
    return cache_dir / filename

# This function can be used by the client to find a file without knowing the backend
def find_existing_cache_path(text: str, language: str = "ko") -> str | None:
    cache_dir = get_pk_tts_cache_dir()
    sanitized_text = sanitize_text_for_filename(text)
    
    possible_filenames = [
        f"gtts_{sanitized_text}_{language}.mp3",
        f"elevenlabs_{sanitized_text}.mp3"
    ]
    
    for filename in possible_filenames:
        potential_path = cache_dir / filename
        if potential_path.exists() and potential_path.stat().st_size > 0:
            return str(potential_path)
    return None
