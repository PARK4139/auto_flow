import logging
import sqlite3
import traceback
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept  # Import ensure_slept for delays
from pk_internal_tools.pk_functions.get_page_number_last_of_nyaa_si_page import get_page_number_last_of_nyaa_si_page
from pk_internal_tools.pk_functions.get_selenium_driver import get_selenium_driver
from pk_internal_tools.pk_objects.pk_files import F_NYAA_ANIMATION_TITLES_SQLITE
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def get_animation_titles_from_nyaa_si(db_path: Path = F_NYAA_ANIMATION_TITLES_SQLITE, max_pages: int | None = None, collection_mode: bool = True, nyaa_si_supplier=None):
    """
    Scrapes animation titles from nyaa.si and stores them in a SQLite database,
    or retrieves them from the database.

    Args:
        nyaa_si_supplier:
        db_path (Path): The path to the SQLite database file.
        max_pages (int | None): The maximum number of pages to scrape. If None, it will be determined dynamically.
        collection_mode (bool): If True, scrapes from the website. If False, retrieves from the database.

    Returns:
        list[str]: A list of animation titles.
    """
    import logging
    import traceback
    import random  # For random sleep

    from bs4 import BeautifulSoup

    logging.debug(f"collection_mode received: {collection_mode}") # Add this line for debugging

    if not collection_mode:
        logging.info("Collection mode is False. Retrieving titles from the database.")
        return _get_all_titles_from_db(db_path)

    logging.info(f"Starting to scrape animation titles from nyaa.si.")
    conn = _init_db(db_path)
    if not conn:
        return []

    base_url = "https://nyaa.si/"
    all_titles = []
    driver = None
    try:
        headless_mode = None
        if QC_MODE:
            headless_mode = False
        driver = get_selenium_driver(headless_mode=headless_mode)

        if nyaa_si_supplier is None:
            nyaa_si_supplier = "SubsPlease"
        search_query_params = {
            "f": 0,
            "c": "1_2",  # Anime - English-translated
            "q": f"{nyaa_si_supplier} 1080p",
        }
        # Construct the base URL with search parameters for page count determination
        initial_url_for_pages = f"{base_url}?" + "&".join([f"{k}={v}" for k, v in search_query_params.items()])

        if max_pages is None:
            logging.info("Determining max_pages dynamically...")
            # get_page_number_last_of_nyaa_si_page expects base_url and driver
            # The base_url should not include 'p=' here, as the function adds it.
            # However, the current implementation of get_page_number_last_of_nyaa_si_page
            # re-constructs the URL with 'p=' so we need to pass the query string correctly.
            # Let's refine the initial_url_for_pages to match expectation of get_page_number_last_of_nyaa_si_page (just base without page param)

            # Reconstruct base_url for get_page_number_last_of_nyaa_si_page to avoid double 'p='
            # The function expects a URL without a page number in it.
            temp_base_url_for_page_count = f"{base_url}?" + "&".join([f"{k}={v}" for k, v in search_query_params.items() if k != "p"])

            determined_max_pages = get_page_number_last_of_nyaa_si_page(temp_base_url_for_page_count, driver)
            if determined_max_pages:
                max_pages = determined_max_pages
                logging.info(f"Dynamically determined max_pages: {max_pages}")
            else:
                logging.warning("Could not dynamically determine max_pages. Falling back to default 10 pages.")
                max_pages = 10  # Fallback if dynamic determination fails
        else:
            logging.info(f"max_pages is set to: {max_pages}")

        for page in range(1, max_pages + 1):
            try:
                # Construct the full URL with page number for scraping
                full_scrape_url = f"{initial_url_for_pages}&p={page}"
                logging.debug(f"Scraping URL: {full_scrape_url}")

                driver.get(full_scrape_url)
                ensure_slept(milliseconds=random.randint(1000, 2000))  # Random sleep to avoid being blocked

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                torrent_rows = soup.select('tr.default, tr.success')
                page_titles = []

                if not torrent_rows:
                    logging.info(f"No more torrents found on page {page}. Stopping.")
                    break

                for row in torrent_rows:
                    columns = row.find_all('td')
                    if len(columns) > 1:
                        name_column = columns[1]
                        link = name_column.find('a')
                        full_name = ""
                        if link:
                            if link.has_attr('title'):
                                full_name = link['title']
                            else:
                                full_name = link.get_text(strip=True)

                        if full_name:
                            logging.debug(f"Found raw entry: {full_name}")
                            title = _extract_title(full_name)
                            if title:
                                page_titles.append(title)
                                logging.debug(f"Extracted title: '{title}'")
                            else:
                                logging.warning(f"Could not extract title from: {full_name}")

                if page_titles:
                    _save_titles_batch(conn, page_titles)
                    all_titles.extend(page_titles)
                else:
                    logging.info(f"No titles found on page {page}.")

            except Exception as e:
                logging.error(f"An error occurred while processing page {page}: {e}")
                ensure_debugged_verbose(traceback=traceback, e=e)
                break
    except Exception as e:
        logging.error(f"An error occurred during scraping initialization or main loop: {e}")
        ensure_debugged_verbose(traceback=traceback, e=e)
    finally:
        if driver:
            driver.quit()
            logging.debug("Selenium driver quit.")

    if conn:
        conn.close()
        logging.debug("Database connection closed.")

    logging.info(f"Scraping finished. Found {len(all_titles)} new unique titles in total.")
    return all_titles


def _get_all_titles_from_db(db_path: Path) -> list[str]:
    """Retrieves all unique animation titles from the database."""
    if not db_path.exists():
        logging.warning(f"Database file not found at {db_path}. Returning empty list.")
        return []

    conn = None
    try:
        conn = sqlite3.connect(db_path, timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM animation_titles ORDER BY title ASC")
        titles = [row[0] for row in cursor.fetchall()]
        logging.info(f"Successfully retrieved {len(titles)} titles from the database.")
        return titles
    except sqlite3.Error as e:
        logging.error(f"Database error while fetching titles: {e}")
        ensure_debugged_verbose(traceback=traceback, e=e)
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching titles: {e}")
        ensure_debugged_verbose(traceback=traceback, e=e)
        return []
    finally:
        if conn:
            conn.close()


def _init_db(db_path: Path) -> sqlite3.Connection | None:
    """Initializes the database and creates the table if it doesn't exist."""
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(db_path, timeout=10)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS animation_titles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        logging.info(f"Database initialized successfully at {db_path}")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database error during initialization: {e}")
        ensure_debugged_verbose(traceback=traceback, e=e)
        return None
    except Exception as e:
        logging.error(f"Failed to initialize database at {db_path}: {e}")
        ensure_debugged_verbose(traceback=traceback, e=e)
        return None


def _extract_title(full_name: str) -> str | None:
    """Extracts the animation title from the full torrent name in a generic way."""
    try:
        # Find the first closing bracket ']' and get the content that follows.
        # e.g., from "[Group] Title - 01.mkv", it gets " Title - 01.mkv"
        start_index = full_name.find(']')
        if start_index == -1:
            return None

        # Part after the first ']'
        main_part = full_name[start_index + 1:].strip()

        # Split from the right by ' - ' to separate title from metadata.
        # This correctly handles titles that contain ' - '.
        # e.g., "Gintama - 3-nen Z-gumi Ginpachi-sensei - 11 (1080p)..."
        # -> ["Gintama - 3-nen Z-gumi Ginpachi-sensei", "11 (1080p)..."]
        title_part, metadata_part = main_part.rsplit(' - ', 1)

        # A simple check to see if the metadata part likely contains an episode number.
        first_word_of_metadata = metadata_part.split(' ')[0]
        if first_word_of_metadata and (
                first_word_of_metadata.isdigit() or  # e.g., "11"
                (first_word_of_metadata.count('.') == 1 and first_word_of_metadata.replace('.', '', 1).isdigit()) or  # e.g., "11.5"
                (first_word_of_metadata.lower().startswith('s') and first_word_of_metadata[1:].isdigit()) or  # e.g., "S2"
                'v' in first_word_of_metadata  # e.g., "07v2"
        ):
            return title_part.strip()

        # If the check fails, it might be a "Batch" release or something unusual.
        # We'll log it but won't return a title to avoid incorrect data.
        logging.warning(f"Could not reliably determine episode number in metadata: '{metadata_part}'. Skipping.")
        return None

    except ValueError:
        # rsplit will raise a ValueError if ' - ' is not found.
        logging.debug(f"Could not rsplit '{full_name}' by ' - ', likely not a standard episode file.")
        return None
    except Exception as e:
        logging.error(f"Error extracting title from '{full_name}': {e}")
        ensure_debugged_verbose(traceback=traceback, e=e)
        return None


def _save_titles_batch(conn: sqlite3.Connection, titles: list[str]):
    """Saves a batch of titles to the database, ignoring duplicates."""
    if not titles:
        return

    try:
        cursor = conn.cursor()
        # Use INSERT OR IGNORE to prevent duplicates based on the UNIQUE constraint on the title
        data_to_insert = [(title,) for title in titles]
        cursor.executemany("INSERT OR IGNORE INTO animation_titles (title) VALUES (?)", data_to_insert)
        conn.commit()
        # The number of newly inserted rows
        new_rows = cursor.rowcount
        if new_rows > 0:
            logging.info(f"Successfully saved {new_rows} new titles to the database.")
        else:
            logging.info("No new unique titles to add in this batch.")
    except sqlite3.Error as e:
        logging.error(f"Database error while saving titles: {e}")
        ensure_debugged_verbose(traceback=traceback, e=e)
