import logging
import os
import traceback
import urllib.parse
import webbrowser

from pk_internal_tools.pk_functions.ensure_magnets_loaded_to_bittorrent import ensure_magnets_loaded_to_bittorrent
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.ensure_values_completed_2025_10_23 import ensure_values_completed_2025_10_23
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_functions.get_magnets_set_from_torrentqq import get_magnets_set_from_torrentqq
from pk_internal_tools.pk_objects.pk_directories import d_pk_root, d_pk_cache, d_pk_root_hidden
    
MAGNET_STORAGE_FILE = os.path.join(d_pk_root_hidden, "pk_magnets.txt")

def open_magnet_link(magnet_link: str):
    """Opens a magnet link in the default torrent client."""
    try:
        logging.info(f"Opening magnet: {magnet_link[:70]}...")
        if os.name == 'nt':
            os.startfile(magnet_link)
        else:
            webbrowser.open(magnet_link)
    except Exception as e:
        logging.error(f"Failed to open magnet link {magnet_link}: {e}")


def get_display_name_from_magnet(magnet: str) -> str:
    """Parses and decodes the display name (&dn=) from a magnet link."""
    try:
        name_part = magnet.split("&dn=")[1]
        name = name_part.split("&tr=")[0]
        return urllib.parse.unquote(name)
    except Exception:
        return magnet[:100] + "..."


if __name__ == "__main__":
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        writable_dir = os.path.join(d_pk_cache, "pk_sb_workspace")
        os.makedirs(writable_dir, exist_ok=True)
        os.chdir(writable_dir)
        logging.info(f"CWD set to {writable_dir} to prevent permission errors.")

        func_n = get_caller_name()
        while 1:
            magnets_to_show = set()

            mode = ensure_value_completed_2025_10_13_0000(
                key_name="mode_select",
                func_n=func_n,
                options=["Collect New", "Show Existing"],
                guide_text="Select operation mode"
            )

            if not mode:
                logging.info("No mode selected. Exiting.")
                break

            if os.path.exists(MAGNET_STORAGE_FILE):
                with open(MAGNET_STORAGE_FILE, 'r', encoding='utf-8') as f:
                    existing_magnets = set(line.strip() for line in f if line.strip())
            else:
                existing_magnets = set()

            if mode == "Collect New":
                search_keyword = ensure_value_completed_2025_10_13_0000(
                    key_name='torrent_keyword',
                    func_n=func_n,
                    options=[],
                    guide_text="Enter a keyword to search for torrents. (Press ESC to exit)"
                )
                if not search_keyword:
                    logging.info("No keyword entered. Returning to mode selection.")
                    continue

                existing_titles = {get_display_name_from_magnet(m) for m in existing_magnets}
                logging.info(f"Checking against {len(existing_titles)} already collected titles.")

                logging.info(f"Searching for: {search_keyword}")
                # Corrected function call to the core scraper
                newly_collected_magnets = get_magnets_set_from_torrentqq(
                    search_keyword=search_keyword,
                    existing_titles=existing_titles
                )

                if not newly_collected_magnets:
                    logging.warning(f"No new magnets found for '{search_keyword}'. Using existing collection.")
                    magnets_to_show = existing_magnets
                else:
                    magnets_to_show = existing_magnets.union(newly_collected_magnets)
                    with open(MAGNET_STORAGE_FILE, 'w', encoding='utf-8') as f:
                        for magnet in sorted(list(magnets_to_show), reverse=True):
                            f.write(magnet + '\n')
                    logging.info(f"{len(newly_collected_magnets)} new magnets found and saved.")

            elif mode == "Show Existing":
                magnets_to_show = existing_magnets
                logging.info(f"Loaded {len(magnets_to_show)} magnets from storage.")

            if not magnets_to_show:
                logging.info("No magnets to display.")
                continue

            name_to_magnet_map = {get_display_name_from_magnet(m): m for m in magnets_to_show}
            display_names = sorted(list(name_to_magnet_map.keys()), reverse=True)

            selected_display_names = ensure_values_completed_2025_10_23(
                key_name="select_magnets",
                options=display_names,
                multi_select=True
            )

            if not selected_display_names:
                logging.info("No magnets selected.")
                continue

            for name in selected_display_names:
                open_magnet_link(name_to_magnet_map[name])

            logging.info(f"{len(selected_display_names)} magnet(s) sent to torrent client.")
            ensure_magnets_loaded_to_bittorrent()

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
