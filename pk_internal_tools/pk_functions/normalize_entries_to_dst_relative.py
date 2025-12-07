from pathlib import Path
from typing import Iterable, List, Union

def normalize_entries_to_dst_relative(
    entries: Iterable[Union[str, Path]],
    d_src: Union[str, Path],
    d_dst: Union[str, Path],
) -> List[Path]:
    """
    Normalize mixed-path entries to destination-relative Paths.

    Rules:
      - If entry is absolute under d_src: make it src-relative, then reuse the same relative under d_dst.
      - Else if entry is absolute under d_dst: convert to dst-relative.
      - Else (relative): treat as already dst-relative (new contract).
    This keeps wildcard suffixes (e.g., '#*.sh', '*.rdp') as-is in the last segment.

    Returns:
      List[Path] of paths relative to d_dst (Path objects may include wildcard chars in name).
    """
    src = Path(d_src).resolve(strict=False)
    dst = Path(d_dst).resolve(strict=False)

    out: List[Path] = []
    for e in entries:
        p = Path(e)
        if p.is_absolute():
            rp = p.resolve(strict=False)
            try:
                # absolute under src → src-relative
                rel = rp.relative_to(src)
                out.append(rel)  # keep relative; applies to dst
                continue
            except Exception:
                pass
            try:
                # absolute under dst → dst-relative
                rel = rp.relative_to(dst)
                out.append(rel)
                continue
            except Exception:
                pass
            # absolute but under neither src nor dst → reject (or log/skip to taste)
            raise ValueError(f"Entry is absolute but under neither src nor dst: {p}")
        else:
            # already relative → interpret as dst-relative (new style)
            out.append(p)
    return out
