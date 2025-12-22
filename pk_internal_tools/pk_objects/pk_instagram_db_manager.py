import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import yt_dlp

from pk_internal_tools.pk_objects.pk_directories import D_INSTAGRAM_DOWNLOADS_CACHE
from pk_internal_tools.pk_objects.pk_files import F_INSTAGRAM_URLS_TO_DOWNLOAD_TXT
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3


class PkInstagramDB:
    def __init__(self):
        d_instagram_downloads_cache = D_INSTAGRAM_DOWNLOADS_CACHE
        d_instagram_downloads_cache.mkdir(parents=True, exist_ok=True)
        f_instagram_db = d_instagram_downloads_cache / "pk_instagram_downloads.sqlite"
        self.pk_db = PkSqlite3(db_path=f_instagram_db)
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        self.pk_db.ensure_table_exists("instagram_urls", {
            "id": "INTEGER PRIMARY KEY",
            "video_id": "TEXT UNIQUE",
            "raw_url": "TEXT",
            "download_status": "TEXT",
            "error_message": "TEXT",
            "created_at": "TEXT",
            "updated_at": "TEXT",
            "channel_name": "TEXT"  # New column
        })

    @staticmethod
    def get_instagram_shortcode(url: str) -> Optional[str]:
        if not url: return None
        match = re.search(r"/(p|reel|reels)/([A-Za-z0-9-_]+)", url)
        return match.group(2) if match else None

    def add_urls_to_db(self, urls: list[str], cookie_opts: dict, channel_name: Optional[str] = None): # channel_name 인자 추가
        validation_opts = {'quiet': True, 'no_warnings': True, 'extract_flat': 'in_playlist'}
        validation_opts.update(cookie_opts)
        cur = self.pk_db.pk_db_connection.cursor()

        cur.execute("PRAGMA table_info(instagram_urls)")
        columns = [info[1] for info in cur.fetchall()]
        if 'video_id' not in columns:
            logging.info("기존 테이블에 'video_id' 컬럼이 없어 추가합니다.")
            cur.execute("ALTER TABLE instagram_urls ADD COLUMN video_id TEXT")
            self.pk_db.pk_db_connection.commit()
        if 'channel_name' not in columns: # Add column if not exists
            logging.info("기존 테이블에 'channel_name' 컬럼이 없어 추가합니다.")
            cur.execute("ALTER TABLE instagram_urls ADD COLUMN channel_name TEXT")
            self.pk_db.pk_db_connection.commit()

        with yt_dlp.YoutubeDL(validation_opts) as ydl:
            for raw_url in urls:
                video_id = self.get_instagram_shortcode(raw_url)
                if not video_id:
                    logging.warning(f"유효하지 않은 URL 형식입니다. 건너뜁니다: {raw_url}")
                    continue

                cur.execute("SELECT download_status FROM instagram_urls WHERE video_id = ?", (video_id,))
                result = cur.fetchone()
                if result:
                    if result[0] == "COMPLETED":
                        logging.debug(f"이미 완료된 ID입니다: {video_id}")
                        self._comment_out_url_in_txt_file(video_id)
                    else:
                        cur.execute("UPDATE instagram_urls SET download_status = ?, updated_at = ? WHERE video_id = ?",
                                    ("PENDING", datetime.now().isoformat(), video_id))
                else:
                    # Update INSERT query to include channel_name
                    cur.execute(
                        "INSERT INTO instagram_urls (raw_url, video_id, download_status, created_at, updated_at, channel_name) VALUES (?, ?, ?, ?, ?, ?)",
                        (raw_url, video_id, "PENDING", datetime.now().isoformat(), datetime.now().isoformat(), channel_name))
        self.pk_db.pk_db_connection.commit()

    def get_pending_urls(self) -> list[str]:
        cur = self.pk_db.pk_db_connection.cursor()
        cur.execute("SELECT raw_url FROM instagram_urls WHERE download_status = 'PENDING'")
        return [row[0] for row in cur.fetchall()]

    def update_download_status(self, video_id: str, status: str, error_message: Optional[str] = None):
        now = datetime.now().isoformat()
        cur = self.pk_db.pk_db_connection.cursor()
        if status == "FAILED":
            sql = "UPDATE instagram_urls SET download_status = ?, error_message = ?, updated_at = ? WHERE video_id = ?"
            params = (status, error_message, now, video_id)
        else:
            sql = "UPDATE instagram_urls SET download_status = ?, error_message = NULL, updated_at = ? WHERE video_id = ?"
            params = (status, now, video_id)
        cur.execute(sql, params)
        self.pk_db.pk_db_connection.commit()
        if status == "COMPLETED":
            self._comment_out_url_in_txt_file(video_id)

    def _comment_out_url_in_txt_file(self, completed_video_id: str):
        try:
            file_path = Path(F_INSTAGRAM_URLS_TO_DOWNLOAD_TXT)
            if not file_path.exists(): return
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            new_lines = []
            changed = False
            for line in lines:
                stripped_line = line.strip()
                if not stripped_line or stripped_line.startswith('#'):
                    new_lines.append(line)
                    continue

                line_video_id = self.get_instagram_shortcode(stripped_line)
                if line_video_id == completed_video_id:
                    new_lines.append(f"# {line}")
                    changed = True
                else:
                    new_lines.append(line)
            if changed:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
        except Exception as e:
            logging.error(f"URL 주석 처리 중 오류 발생: {e}")
