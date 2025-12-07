from typing import Optional, Callable, List, Tuple


def _get_all_magnets_from_db() -> list[tuple[str, str, str]]:  # Changed return type
    import logging
    import sqlite3
    from pathlib import Path

    from pk_internal_tools.pk_objects.pk_files import F_NYAA_MAGNETS_SQLITE

    db_path = Path(F_NYAA_MAGNETS_SQLITE)
    if not db_path.exists():
        logging.warning("Magnet database not found. Please collect magnets first.")
        return []

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT title, magnet, registration_date FROM nyaa_magnets ORDER BY title ASC")  # Added registration_date
        all_magnets_from_db = cur.fetchall()
        conn.close()
        return all_magnets_from_db
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return []


def _filter_magnets_with_fzf_syntax(query: str, all_magnets: List[Tuple[str, str, str]]) -> List[str]:
    """
    Filters magnets based on fzf-like syntax.
    Supports:
    - Simple substring: term
    - Exact phrase: "phrase" or 'phrase'
    - Negation: !term
    - Start of string: ^term
    - End of string: term$
    - AND condition: space-separated terms
    """
    if not query:
        return [magnet for _, magnet in all_magnets]  # Return all magnets if query is empty

    # Tokenize the query, handling quoted phrases (both single and double quotes)
    tokens = []
    in_double_quote = False
    in_single_quote = False
    current_token = []
    for char in query:
        if char == '"':
            if in_single_quote:  # If inside single quote, treat " as literal
                current_token.append(char)
            elif in_double_quote:  # End double quote
                tokens.append("".join(current_token))
                current_token = []
                in_double_quote = False
            else:  # Start double quote
                if current_token:  # Add previous token if any
                    tokens.append("".join(current_token))
                    current_token = []
                in_double_quote = True
        elif char == "'":
            if in_double_quote:  # If inside double quote, treat ' as literal
                current_token.append(char)
            elif in_single_quote:  # End single quote
                tokens.append("".join(current_token))
                current_token = []
                in_single_quote = False
            else:  # Start single quote
                if current_token:  # Add previous token if any
                    tokens.append("".join(current_token))
                    current_token = []
                in_single_quote = True
        elif char == ' ' and not in_double_quote and not in_single_quote:
            if current_token:
                tokens.append("".join(current_token))
                current_token = []
        else:
            current_token.append(char)
    if current_token:
        tokens.append("".join(current_token))

    # Build a list of filter functions
    filter_funcs: List[Callable[[str], bool]] = []

    for token in tokens:
        token_lower = token.lower()

        # Check for quoted phrases (single or double)
        is_double_quoted = token_lower.startswith('"') and token_lower.endswith('"')
        is_single_quoted = token_lower.startswith("'") and token_lower.endswith("'")

        if token_lower.startswith('^'):
            term = token[1:].lower()
            filter_funcs.append(lambda title, t=term: title.lower().startswith(t))
        elif token_lower.endswith('$'):
            term = token[:-1].lower()
            filter_funcs.append(lambda title, t=term: title.lower().endswith(t))
        elif token_lower.startswith('!'):
            term = token[1:].lower()
            filter_funcs.append(lambda title, t=term: t not in title.lower())
        elif is_double_quoted or is_single_quoted:  # Exact phrase (after tokenization, quotes are removed)
            term = token[1:-1].lower()  # Remove quotes
            filter_funcs.append(lambda title, t=term: t in title.lower())  # Simple substring for now, can be improved for exact word word match
        else:  # Simple substring
            filter_funcs.append(lambda title, t=token_lower: t in title.lower())

    filtered_magnets = []
    for title, magnet in all_magnets:
        # All filter functions must return True (AND logic)
        if all(f(title) for f in filter_funcs):
            filtered_magnets.append(magnet)

    return filtered_magnets


def get_magnets_from_db_with_fzf(initial_query: Optional[str] = None) -> tuple[list[str], Optional[str]]:
    import logging
    import subprocess

    from pk_internal_tools.pk_functions.get_fzf_command import get_fzf_command

    all_magnets_from_db = _get_all_magnets_from_db()
    if not all_magnets_from_db:
        return [], initial_query

    # --- Interactive fzf mode (initial_query is None) ---
    fzf_executable_path = get_fzf_command()
    if not fzf_executable_path:
        logging.error("fzf command not found. Please install fzf.")
        return [], initial_query  # initial_query is None here

    title_to_magnet_map = {title: magnet for title, magnet, _ in all_magnets_from_db}
    fzf_formatted_lines = [title for title, magnet, _ in all_magnets_from_db]
    fzf_input = "\n".join(fzf_formatted_lines).encode('utf-8')

    fzf_command = [
        str(fzf_executable_path),
        "--no-mouse",
        "--multi",  # Keep multi-select
        "--ansi",  # Add ANSI color support
        "--no-sort",  # Add no-sort if input is already sorted
        "--layout", "reverse",
        "--info", "inline",
        "--prompt", "마그넷 링크 검색어=",
        "--header", "마그넷 링크 선택",
        "--footer", "Alt+A: 전체선택 | Tab: 선택/해제 | Enter: 확인 | Ctrl+Y: 복사",
        "--color=prompt:#ffffff,pointer:#4da6ff,hl:#3399ff,hl+:#3399ff,fg+:#3399ff",
        "--bind", "alt-a:select-all",
        "--bind", "ctrl-a:ignore",
        "--bind", "ctrl-y:execute-silent(echo {} | clip.exe)",  # Copy to clipboard
        "--print-query"  # Print the query string as the first line of output
    ]
    # No --query option if initial_query is None (which it is in this branch)

    try:
        process = subprocess.Popen(fzf_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=fzf_input)

        if process.returncode != 0:
            logging.error(f"fzf exited with error code {process.returncode}: {stderr.decode('utf-8')}")
            return [], initial_query  # initial_query is None here

        output_lines = stdout.decode('utf-8').strip().split('\n')

        final_query = output_lines[0] if output_lines else ""
        selected_titles = output_lines[1:] if len(output_lines) > 1 else []

        selected_magnets = [title_to_magnet_map[title] for title in selected_titles if title in title_to_magnet_map]
        return selected_magnets, final_query

    except Exception as e:
        logging.error(f"An error occurred while running fzf: {e}")
        return [], initial_query  # initial_query is None here


def _process_and_load_magnets(selected_magnets_from_fzf: list[str], load_last_only: bool = False) -> bool:
    import logging
    import webbrowser
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
    from pk_internal_tools.pk_functions.get_list_from_set import get_list_from_set
    from pk_internal_tools.pk_functions.get_list_interested_from_list import get_list_interested_from_list
    from pk_internal_tools.pk_objects.pk_directories import D_USERPROFILE
    from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import ensure_env_var_completed_2025_11_24
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    d_bittorrent_appdata = Path(D_USERPROFILE) / 'AppData' / 'Roaming' / 'bittorrent'
    d_bittorrent_appdata_as_list = [str(d_bittorrent_appdata)]

    exclusions = [
        '.dat', '.dll', '.exe', '.dmp', '.lng', '.zip',
        '$RECYCLE.BIN', 'System Volume Information',
        'deprecated', 'archived', '.git', '.idea', 'venv', 'node_modules',
    ]

    existing_torrent_files = get_list_calculated(origin_list=d_bittorrent_appdata_as_list, minus_list=exclusions)
    existing_torrent_files = get_list_interested_from_list(working_list=existing_torrent_files, ext_list_include=[".torrent"])

    existing_torrent_names = {Path(f).stem for f in existing_torrent_files}

    new_magnets_to_load_set = {magnet for magnet in selected_magnets_from_fzf if not any(name in magnet for name in existing_torrent_names)}

    final_magnets_to_load = get_list_from_set(new_magnets_to_load_set)
    final_magnets_to_load = sorted(final_magnets_to_load, key=lambda magnet: magnet.split("&dn=")[1] if "&dn=" in magnet else "")

    if load_last_only and final_magnets_to_load:
        logging.info(f"Loading only the last magnet due to 'load_last_only' flag.")
        final_magnets_to_load = [final_magnets_to_load[-1]]

    if not final_magnets_to_load:
        logging.info("All selected magnets are already present in the client.")
        return True  # Indicate that no new magnets were loaded, but it's not an error

    logging.info(f"{len(final_magnets_to_load)} out of {len(selected_magnets_from_fzf)} selected magnets will be loaded.")

    if QC_MODE:
        load_interval_milliseconds = 500
    else:
        load_interval_milliseconds = int(ensure_env_var_completed_2025_11_24(key_name='load_interval_milliseconds', options=['1000', '500', '2000']))

    for magnet in final_magnets_to_load:
        if not magnet.strip():
            continue

        logging.debug(f'Loading magnet: {magnet}')
        webbrowser.open(magnet)
        ensure_slept(milliseconds=load_interval_milliseconds)
    return False  # Indicate that new magnets were loaded


def ensure_magnets_loaded_to_bittorrent(initial_filter_query: Optional[str] = None, load_last_only: bool = False):
    import logging
    from typing import Optional

    # We need to ensure is_internet_connected_2025_10_21 is imported here.
    from pk_internal_tools.pk_functions.is_internet_connected_2025_10_21 import is_internet_connected_2025_10_21

    if not is_internet_connected_2025_10_21():
        logging.error("Internet connection is required.")
        return

    # If an initial_filter_query is provided, we run non-interactive mode once.
    if initial_filter_query is not None:
        logging.debug(f"Running in non-interactive mode with query: '{initial_filter_query}'")
        selected_magnets_from_fzf, _ = get_magnets_from_db_with_fzf(initial_query=initial_filter_query)

        if not selected_magnets_from_fzf:
            logging.info(f"No magnets found for non-interactive query '{initial_filter_query}'.")
            return

        _process_and_load_magnets(selected_magnets_from_fzf, load_last_only=load_last_only)
        return  # Exit after processing the non-interactive query

    # --- Interactive loop (if initial_filter_query is None) ---
    last_query_from_fzf: Optional[str] = None  # Start with None to trigger interactive fzf
    while True:
        logging.debug(f"Loop start. Passing to fzf, initial_query: '{last_query_from_fzf}'")
        selected_magnets_from_fzf, last_query_from_fzf = get_magnets_from_db_with_fzf(initial_query=last_query_from_fzf)
        logging.debug(f"Returned from fzf. last_query is now: '{last_query_from_fzf}'")

        if not selected_magnets_from_fzf and last_query_from_fzf is None:  # Break if no selection AND query is None (user hit ESC/Ctrl+C)
            logging.info("No magnets selected and no query entered. Exiting loop.")
            break
        elif not selected_magnets_from_fzf and last_query_from_fzf is not None:  # If query exists but no selection, re-enter with query
            logging.info(f"No magnets selected for query '{last_query_from_fzf}'. Re-entering fzf selection.")
            continue

        # Process and load magnets
        all_present = _process_and_load_magnets(selected_magnets_from_fzf, load_last_only=load_last_only)
        if all_present:  # If all selected magnets were already present, re-enter fzf
            logging.info("All selected magnets were already present in the client. Re-entering fzf selection.")
            continue


def ensure_magnets_loaded_to_bittorrent_advanced(initial_filter_query: Optional[str] = None, load_last_only: bool = False, use_advanced_syntax: bool = False, load_days_from_today: Optional[int] = None):
    import logging
    import datetime  # Added import for date filtering
    from typing import Optional, List, Tuple  # Added Tuple for all_magnets_from_db type hint

    from pk_internal_tools.pk_functions.is_internet_connected_2025_10_21 import is_internet_connected_2025_10_21

    if not is_internet_connected_2025_10_21():
        logging.error("Internet connection is required.")
        return

    # --- Interactive Mode (initial_filter_query is None) ---
    if initial_filter_query is None:
        last_query_from_fzf: Optional[str] = None
        while True:
            logging.debug(f"Loop start. Passing to fzf, initial_query: '{last_query_from_fzf}'")
            selected_magnets_from_fzf, last_query_from_fzf = get_magnets_from_db_with_fzf(initial_query=last_query_from_fzf)
            logging.debug(f"Returned from fzf. last_query is now: '{last_query_from_fzf}'")

            if not selected_magnets_from_fzf and last_query_from_fzf is None:
                logging.info("No magnets selected and no query entered. Exiting loop.")
                break
            elif not selected_magnets_from_fzf and last_query_from_fzf is not None:
                logging.info(f"No magnets selected for query '{last_query_from_fzf}'. Re-entering fzf selection.")
                continue

            all_present = _process_and_load_magnets(selected_magnets_from_fzf, load_last_only=load_last_only)
            if all_present:
                logging.info("All selected magnets were already present in the client. Re-entering fzf selection.")
                continue
        return  # Exit after interactive loop

    # --- Non-Interactive Mode (initial_filter_query is a string) ---
    else:  # initial_filter_query is a string
        logging.debug(f"Running in non-interactive mode with query: '{initial_filter_query}'")

        all_magnets_from_db_with_date: List[Tuple[str, str, str]] = _get_all_magnets_from_db()
        if not all_magnets_from_db_with_date:
            logging.info("No magnets found in the database.")
            return

        # --- Apply date filtering if load_days_from_today is set ---
        filtered_by_date_magnets: List[Tuple[str, str, str]] = []
        if load_days_from_today is not None and load_days_from_today > 0:
            logging.debug(f"Filtering magnets registered within {load_days_from_today} days from today.")
            today = datetime.date.today()
            cutoff_date = today - datetime.timedelta(days=load_days_from_today)

            for title, magnet, reg_date_str in all_magnets_from_db_with_date:
                try:
                    reg_date = datetime.date.fromisoformat(reg_date_str)
                    if reg_date >= cutoff_date:
                        filtered_by_date_magnets.append((title, magnet, reg_date_str))
                except (ValueError, TypeError):
                    logging.warning(f"Invalid registration_date format for magnet '{title}': '{reg_date_str}'. Skipping date filter for this entry.")
                    # Optionally include if date is invalid, or skip. Skipping for now.

            if not filtered_by_date_magnets:
                logging.info(f"No magnets found registered within {load_days_from_today} days matching date filter.")
                return
        else:
            filtered_by_date_magnets = all_magnets_from_db_with_date  # No date filter, use all

        # --- Apply initial_filter_query filtering ---
        selected_magnets_from_fzf_list: List[str] = []

        if use_advanced_syntax:
            logging.debug(f"Using advanced fzf syntax parsing for query: '{initial_filter_query}'")
            selected_magnets_from_fzf_list = _filter_magnets_with_fzf_syntax(initial_filter_query, filtered_by_date_magnets)
        else:
            logging.debug(f"Using simple substring matching for query: '{initial_filter_query}'")
            # Implement simple filtering logic
            for title, magnet, _ in filtered_by_date_magnets:  # Iterate over date-filtered list
                if initial_filter_query.lower() in title.lower():
                    selected_magnets_from_fzf_list.append(magnet)

        if not selected_magnets_from_fzf_list:
            logging.info(f"No magnets found matching query '{initial_filter_query}'.")
            return

        _process_and_load_magnets(selected_magnets_from_fzf_list, load_last_only=load_last_only)
        return  # Exit after non-interactive processing
