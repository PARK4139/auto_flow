import time
from pk_internal_tools.pk_functions.get_window_titles import get_window_titles

def collect_losslesscut_titles(output_file="losslesscut_titles.log", interval=1.0):
    seen = set()
    with open(output_file, "a", encoding="utf-8") as f:
        while True:
            titles = get_window_titles()
            for title in titles:
                if get_idle_title_of_losslesscut() in title and title not in seen:
                    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {title}\n")
                    f.flush()
                    print(title)
                    seen.add(title)
            time.sleep(interval)

# example
# collect_losslesscut_titles() 