import datetime  # Added import
import logging
import math
import random
import sqlite3
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pk_internal_tools.pk_objects.pk_texts import PK_BLANK
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.get_selenium_driver import get_selenium_driver
from pk_internal_tools.pk_functions.get_page_number_last_of_nyaa_si_page import get_page_number_last_of_nyaa_si_page
from pk_internal_tools.pk_functions.get_str_encoded_url import get_str_encoded_url
from pk_internal_tools.pk_functions.get_total_cnt_of_f_torrent_list import get_total_cnt_of_f_torrent_list
from pk_internal_tools.pk_objects.pk_files import F_NYAA_MAGNETS_SQLITE

DB_FILE = Path(F_NYAA_MAGNETS_SQLITE)


def init_and_get_db_conn():
    """Initializes the SQLite database and table, returns a connection."""
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS nyaa_magnets
                (
                    magnet TEXT PRIMARY KEY,
                    title TEXT,
                    registration_date TEXT,
                    registration_time TEXT
                )
                """)

    # --- Migration: Add columns if they don't exist ---
    # Check if registration_date column exists
    cur.execute("PRAGMA table_info(nyaa_magnets);")
    columns = [col[1] for col in cur.fetchall()]

    if 'registration_date' not in columns:
        cur.execute("ALTER TABLE nyaa_magnets ADD COLUMN registration_date TEXT;")
        logging.info("Added 'registration_date' column to nyaa_magnets table.")

    if 'registration_time' not in columns:
        cur.execute("ALTER TABLE nyaa_magnets ADD COLUMN registration_time TEXT;")
        logging.info("Added 'registration_time' column to nyaa_magnets table.")

    # --- Migration: Update existing rows with current date/time if NULL ---
    current_date = datetime.date.today().isoformat()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    cur.execute("UPDATE nyaa_magnets SET registration_date = ?, registration_time = ? WHERE registration_date IS NULL;", (current_date, current_time))
    logging.info("Updated existing nyaa_magnets rows with current date/time where registration_date was NULL.")

    conn.commit()
    return conn


def save_magnets_batch(magnets):
    """Saves a batch of magnets to the SQLite database."""
    if not magnets:
        return
    logging.debug(f"Saving {len(magnets)} magnets to SQLite")
    conn = init_and_get_db_conn()
    cur = conn.cursor()

    current_date = datetime.date.today().isoformat()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    # magnet 링크에서 title 파싱 및 날짜/시간 추가
    data = [(m, parse_qs(urlparse(unquote(m)).query).get("dn", [""])[0], current_date, current_time) for m in magnets]
    cur.executemany(
        "INSERT OR IGNORE INTO nyaa_magnets(magnet,title,registration_date,registration_time) VALUES(?,?,?,?)", data
    )
    conn.commit()
    cur.close()
    conn.close()
    logging.debug("Batch saved")


def ensure_magnets_collected_from_nyaa_si(*, animation_title_keyword, nyaa_si_supplier, resolution_keyword, driver=None, pages=None):
    init_and_get_db_conn()  # Ensure DB and table are created before starting
    logging.debug("Starting crawl")
    driver = driver or get_selenium_driver(headless_mode=False)
    search_keyword = rf"{animation_title_keyword}{PK_BLANK}{resolution_keyword}"
    base = f"https://nyaa.si/user/{nyaa_si_supplier}?f=0&c=0_0&q={get_str_encoded_url(search_keyword)}"
    driver.get(base)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = get_total_cnt_of_f_torrent_list(soup.find("h3").text.strip())
    if pages is None:
        pages = math.ceil(total / 75) if total else get_page_number_last_of_nyaa_si_page(base, driver)
    logging.debug(f"Total pages found: {pages}")

    start = 1

    batch = []
    for p in range(start, pages + 1):
        try:
            logging.debug(f"--- Scraping Page {p}/{pages} ---")
            driver.get(f"{base}&p={p}")
            WebDriverWait(driver, 10).until(lambda d: d.find_element(By.TAG_NAME, "body"))
            found = {a["href"] for a in BeautifulSoup(driver.page_source, "html.parser").find_all("a", href=True) if
                     a["href"].startswith("magnet:")}
            logging.debug(f"Found {len(found)} magnets on page {p}.")
            batch.extend(found)
            if len(batch) >= 100:
                save_magnets_batch(batch)
                batch.clear()
            ensure_slept(milliseconds=random.randint(200, 333))
        except Exception as e:
            logging.debug(f"Error page {p}: {e}")

    if batch:
        save_magnets_batch(batch)

    logging.debug("Done collecting")
    return None
