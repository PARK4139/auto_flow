import re


def analyze_titles(log_file="losslesscut_titles.log"):
    with open(log_file, encoding="utf-8") as f:
        lines = f.readlines()
    states = {"editing": [], "exporting": [], "loading": [], "playing": [], "other": []}
    for line in lines:
        title = line.strip().split("|", 1)[-1].strip()
        if "출력" in title or "Export" in title:
            states["exporting"].append(title)
        elif "편집" in title or "Edit" in title:
            states["editing"].append(title)
        elif "불러오는 중" in title or "Loading" in title:
            states["loading"].append(title)
        elif re.search(r"\.mp4|\.mkv|\.avi", title, re.I):
            states["playing"].append(title)
        else:
            states["other"].append(title)
    for k, v in states.items():
        print(f"\n[{k.upper()}] ({len(v)})")
        for t in set(v):
            print("", t)
    return states

# example
# analyze_titles()
