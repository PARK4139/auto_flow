
import hashlib
import logging

def get_hashed_items(items: list[str], hash_length: int = 6) -> list[str]:
    """
    주어진 문자열 목록의 각 항목에 짧은 해시를 접두사로 추가하여 반환합니다.

    Args:
        items (list[str]): 해시를 추가할 문자열 항목 목록.
        hash_length (int): 생성할 해시 접두사의 길이. 기본값은 6입니다.

    Returns:
        list[str]: 각 항목에 "[hash] original_item" 형식으로 해시가 추가된 새 목록.
    """
    hashed_list = []
    for item in items:
        # SHA256 해시를 생성하고 처음 hash_length 문자만 사용합니다.
        full_hash = hashlib.sha256(str(item).encode('utf-8')).hexdigest()
        short_hash = full_hash[:hash_length]
        hashed_list.append(f"[{short_hash}] {item}")
    logging.debug(f"get_hashed_items: {len(items)} items hashed.")
    return hashed_list

