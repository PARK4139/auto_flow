import logging
import traceback
import re
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import urllib.parse

from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
from pk_internal_tools.pk_functions.get_selenium_driver_initialized_for_cloudflare import get_selenium_driver_initialized_for_cloudflare
from pk_internal_tools.pk_functions.ensure_driver_navigates_to_url_and_switches_to_new_tab import ensure_driver_navigates_to_url_and_switches_to_new_tab
from pk_internal_tools.pk_functions.is_all_included_in_prompt import is_all_included_in_prompt

def get_magnets_set_from_torrentqq(search_keyword, driver=None, existing_titles: set = None):
    if existing_titles is None:
        existing_titles = set()
        
    magnet_link_set = set()
    try:
        logging.info(f"Starting magnet collection for keyword: '{search_keyword}'")
        if not search_keyword:
            logging.warning("Search keyword is blank.")
            return magnet_link_set

        if driver is None:
            logging.info("No Selenium driver provided, creating a new one.")
            driver = get_selenium_driver_initialized_for_cloudflare(headless_mode=True)

        base_url = None
        start_num = 390
        max_retries = 10
        for i in range(max_retries):
            current_num = start_num + i
            current_url = f"https://torrentqq{current_num}.com"
            logging.info(f"[Attempt {i+1}/{max_retries}] Connecting to {current_url}...")
            try:
                driver.uc_open_with_reconnect(current_url, reconnect_time=5)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                logging.debug(f"--- HTML of {current_url} ---\n{soup.prettify()}\n-------------------------------------")
                body_text = soup.body.get_text(strip=True) if soup.body else ""
                if '잠시만 기다려' in body_text or not body_text:
                    logging.warning(f" -> Failed: Cloudflare or empty page at {current_url}")
                    continue
                base_url = current_url
                logging.info(f"> Success: Connected to {base_url}")
                break
            except Exception as e:
                logging.warning(f" -> Failed to connect to {current_url}. Error: {e}")
                continue

        if not base_url:
            logging.error("Could not find a working torrentqq URL. Aborting.")
            return magnet_link_set

        if not base_url:
            logging.error("Could not find a working torrentqq URL. Aborting.")
            return magnet_link_set

        successful_search_nav = False
        search_attempt_base_url = base_url  # Start with the initially found base_url
        max_search_retries = 3  # Define how many times we retry the search
        for attempt in range(max_search_retries):
            current_search_url = f'{search_attempt_base_url}/search?q={search_keyword}'
            logging.info(f"[Search Attempt {attempt + 1}/{max_search_retries}] Navigating to search results: {current_search_url}")
            ensure_driver_navigates_to_url_and_switches_to_new_tab(url=current_search_url, driver=driver,
                                                                   seconds_s=500, seconds_e=1500)

            current_url_after_nav = driver.current_url
            logging.info(f"Current URL after search navigation: {current_url_after_nav}")

            encoded_search_keyword = urllib.parse.quote_plus(search_keyword)

            # Check if the current URL is a torrentqq homepage (e.g., torrentqqXXX.com/)
            # This regex is a bit simplistic, but good enough for now
            torrentqq_homepage_redirect_match = re.match(r"https://torrentqq([0-9]+)\.com/?$", current_url_after_nav)

            if f"/search?q={encoded_search_keyword}" in current_url_after_nav:
                logging.info(f"Successfully navigated to search results page: {current_url_after_nav}")
                successful_search_nav = True
                break  # Exit retry loop if successful
            elif torrentqq_homepage_redirect_match:
                # Redirected to a torrentqq homepage. Update search_attempt_base_url and retry.
                new_domain_num = torrentqq_homepage_redirect_match.group(1)
                search_attempt_base_url = f"https://torrentqq{new_domain_num}.com"
                logging.warning(f"Redirected to a torrentqq homepage: {current_url_after_nav}. Retrying search from new base URL: {search_attempt_base_url}")
                # Continue to next iteration of search retry loop
            else:
                # Redirected to something else entirely or a non-search page.
                logging.warning(f"Redirected away from expected search page to '{current_url_after_nav}'. Aborting search retries for '{search_keyword}'.")
                return magnet_link_set  # Give up entirely

        if not successful_search_nav:
            logging.error(f"Failed to navigate to a valid search results page after {max_search_retries} attempts. Aborting.")
            return magnet_link_set

        try:
            logging.info("Waiting for search results to load...")
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "miso-post-list")))
            logging.info("Search results list has loaded.")
        except Exception as e:
            logging.error(f"Search results did not load in time: {e}")
            return magnet_link_set

        soup_search = BeautifulSoup(driver.page_source, 'html.parser')
        logging.debug(f"--- HTML of Search Results Page ---\n{soup_search.prettify()}\n-------------------------------------")

        detail_page_links = []
        for a_tag in soup_search.find_all("a"):
            title = a_tag.get('title')
            href = a_tag.get('href')
            if title and href and '/torrent/' in href and href.startswith("http"):
                logging.debug(f"  -> Found detail page link: {href}")
                detail_page_links.append((title, href))
        
        logging.info(f"Found {len(detail_page_links)} potential detail page links.")
        if not detail_page_links:
            logging.warning("No detail page links found on the search results page.")
            return magnet_link_set

        keywords_required = [k.lower() for k in search_keyword.split()]
        for title, href in detail_page_links:
            if title in existing_titles:
                logging.info(f"Skipping already collected item: {title}")
                continue

            if not is_all_included_in_prompt(prompt=title.lower(), txt_list=keywords_required):
                logging.debug(f"Skipping '{title}' as it does not match all keywords.")
                continue

            logging.info(f"Visiting detail page: {title}")
            ensure_driver_navigates_to_url_and_switches_to_new_tab(url=href, driver=driver, seconds_s=500, seconds_e=1500)
            soup_detail = BeautifulSoup(driver.page_source, 'html.parser')
            logging.debug(f"--- HTML of Detail Page: {title} ---\n{soup_detail.prettify()}\n-------------------------------------------")
            
            magnet_found_on_page = False
            if magnet_button := soup_detail.find("a", class_="btn-magnet"):
                logging.debug(f"  -> Found magnet button: {magnet_button.prettify()}")
                if onclick_attr := magnet_button.get("onclick"):
                    logging.debug(f"  -> Extracted onclick attribute: {onclick_attr}")
                    if path_match := re.search(r"window\.open\('([^']+)'", onclick_attr):
                        magnet_page_path = path_match.group(1)
                        magnet_page_url = f"{base_url}{magnet_page_path}"
                        logging.info(f"> Found magnet page link, navigating: {magnet_page_url}")
                        
                        ensure_driver_navigates_to_url_and_switches_to_new_tab(url=magnet_page_url, driver=driver, seconds_s=500, seconds_e=1500)
                        
                        if magnet_match_final := re.search(r"(magnet:\?[^'\"]+)", driver.page_source):
                            magnet_link = magnet_match_final.group(1)
                            logging.debug(f"    -> Successfully extracted magnet link: {magnet_link[:60]}...")
                            magnet_url_customed = f"{magnet_link}&dn={title}"
                            magnet_link_set.add(magnet_url_customed)
                            magnet_found_on_page = True
            
            if magnet_found_on_page:
                logging.info(f"> Success: Magnet found for '{title}'")
            else:
                logging.warning(f" -> Failure: Magnet not found for '{title}'")

        ensure_iterable_data_printed(iterable_data=magnet_link_set, iterable_data_n="Final collected magnet links")
        logging.info(f"Collection complete. Found a total of {len(magnet_link_set)} unique magnet links.")

        return magnet_link_set

    except Exception as e:
        logging.error(f"An unexpected error occurred during magnet collection: {e}")
        traceback.print_exc()
        return magnet_link_set
