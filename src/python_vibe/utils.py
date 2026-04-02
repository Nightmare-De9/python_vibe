import time
import traceback
from typing import Any, List, Dict, Optional
from rich.table import Table
from rich.console import Console
from rich import box


_con = Console()


def make_table(data: Any, title: str = "", thm=None) -> Optional[Table]:
    """turns lists/dicts into rich tables. returns None if cant."""
    from .themes import get_theme
    t = thm or get_theme()

    if isinstance(data, dict):
        # single dict -> 2col table
        tbl = Table(
            title=title or None,
            box=box.ROUNDED,
            border_style=t.border_style,
            header_style=f"bold {t.primary}",
            show_header=True,
        )
        tbl.add_column("key", style=t.secondary, min_width=12)
        tbl.add_column("value", style="bright_white", min_width=20)
        for k, v in data.items():
            tbl.add_row(str(k), _fmt_val(v))
        return tbl

    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], dict):
            return _list_of_dicts_table(data, title, t)
        # plain list
        tbl = Table(
            title=title or None,
            box=box.SIMPLE_HEAD,
            border_style=t.border_style,
            header_style=f"bold {t.primary}",
        )
        tbl.add_column("idx", style=t.accent, width=6)
        tbl.add_column("value", style="bright_white")
        for i, v in enumerate(data):
            tbl.add_row(str(i), _fmt_val(v))
        return tbl

    return None


def _list_of_dicts_table(data: List[Dict], title: str, t) -> Table:
    cols = list(data[0].keys())
    tbl = Table(
        title=title or None,
        box=box.ROUNDED,
        border_style=t.border_style,
        header_style=f"bold {t.primary}",
        row_styles=["", f"on grey7"],
        expand=False,
    )
    for c in cols:
        tbl.add_column(str(c), style="bright_white", overflow="fold")
    for row in data:
        tbl.add_row(*[_fmt_val(row.get(c, "")) for c in cols])
    return tbl


def _fmt_val(v: Any) -> str:
    if v is None:
        return "[dim]None[/dim]"
    if isinstance(v, bool):
        return "[green]True[/green]" if v else "[red]False[/red]"
    if isinstance(v, float):
        return f"{v:.4f}" if abs(v) < 1e6 else f"{v:.2e}"
    return str(v)


def try_df_to_table(obj: Any, title: str = "", thm=None) -> Optional[Table]:
    """pandas df -> table. optional dep so wrapped in try"""
    try:
        import pandas as pd
        if not isinstance(obj, pd.DataFrame):
            return None
        from .themes import get_theme
        t = thm or get_theme()
        tbl = Table(
            title=title or "DataFrame",
            box=box.ROUNDED,
            border_style=t.border_style,
            header_style=f"bold {t.primary}",
            row_styles=["", "on grey7"],
        )
        tbl.add_column("#", style=t.accent, width=5)
        for col in obj.columns:
            tbl.add_column(str(col), style="bright_white", overflow="fold")
        for idx, row in obj.head(50).iterrows():  # fixme later: add pagination
            tbl.add_row(str(idx), *[_fmt_val(v) for v in row])
        if len(obj) > 50:
            tbl.caption = f"[dim]showing 50/{len(obj)} rows[/dim]"
        return tbl
    except ImportError:
        return None
    except Exception:
        return None


def fmt_exc(exc: BaseException) -> str:
    """makes exceptions slightly less ugly. stub rn, will improve"""
    tb = traceback.format_exception(type(exc), exc, exc.__traceback__)
    lines = []
    for line in tb:
        lines.append(line.rstrip())
    return "\n".join(lines)


def get_err_hint(exc: BaseException) -> Optional[str]:
    """dumb error hint lookup. not smart yet but better than nothing"""
    msg = str(exc).lower()
    etype = type(exc).__name__

    hints = {
        "ModuleNotFoundError": "run `pip install {mod}` maybe?",
        "KeyError": "key doesn't exist in dict — check spelling or use .get()",
        "IndexError": "list index out of range — check len() before indexing",
        "AttributeError": "object doesn't have that attr — check type or spelling",
        "TypeError": "wrong type passed somewhere — check your function args",
        "ValueError": "bad value — check what you're passing in",
        "FileNotFoundError": "file not found — check path and cwd",
        "ConnectionError": "network issue — check internet/server",
        "PermissionError": "no permission — try sudo or check file perms",
        "RecursionError": "infinite recursion — add a base case bro",
        "MemoryError": "ran out of memory — process smaller chunks",
        "ZeroDivisionError": "dividing by zero — add a zero check",
    }

    hint = hints.get(etype)
    if hint and "{mod}" in hint and "'" in msg:
        # extract module name from "No module named 'xyz'"
        try:
            mod_name = msg.split("'")[1]
            hint = hint.format(mod=mod_name)
        except Exception:
            hint = hint.format(mod="<module>")
    return hint


class Timer:
    """dead simple timer"""
    def __init__(self):
        self._start = None
        self._end = None

    def start(self):
        self._start = time.perf_counter()
        return self

    def stop(self):
        self._end = time.perf_counter()
        return self

    @property
    def elapsed(self) -> float:
        if self._start is None:
            return 0.0
        end = self._end or time.perf_counter()
        return end - self._start

    def fmt(self) -> str:
        e = self.elapsed
        if e < 1:
            return f"{e*1000:.1f}ms"
        if e < 60:
            return f"{e:.2f}s"
        return f"{int(e//60)}m {e%60:.1f}s"

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *_):
        self.stop()


def is_df(obj: Any) -> bool:
    """check if pandas df without importing pandas if not installed"""
    return type(obj).__name__ == "DataFrame" and hasattr(obj, "columns") and hasattr(obj, "iterrows")


def should_tablify(obj: Any) -> bool:
    """decide if obj should be auto-converted to table"""
    if is_df(obj):
        return True
    if isinstance(obj, dict) and len(obj) > 0:
        return True
    if isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], dict):
        return True
    return False
