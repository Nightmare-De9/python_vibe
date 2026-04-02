"""
core vibe engine — dont touch monkey patch
patches builtins.print and logging to make everything pretty
"""
import builtins
import logging
import sys
import functools
import traceback
from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich.traceback import Traceback
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn, TaskProgressColumn
from rich.table import Table
from rich import box

from .themes import get_theme
from .utils import make_table, try_df_to_table, fmt_exc, get_err_hint, should_tablify, Timer, is_df


_con = Console(highlight=False)
_err_con = Console(stderr=True, highlight=False)
_active = False
_orig_print = builtins.print
_orig_excepthook = sys.excepthook
_vibe_logger_handler: Optional[logging.Handler] = None


class VibeHandler(logging.Handler):
    """logging handler — replaces ugly default logs"""

    LEVEL_STYLES = {
        logging.DEBUG: ("dim", "🔍"),
        logging.INFO: ("bright_white", "ℹ️"),
        logging.WARNING: ("yellow", "⚠️"),
        logging.ERROR: ("red", "❌"),
        logging.CRITICAL: ("bold red", "💥"),
    }

    def emit(self, record: logging.LogRecord):
        if not _active:
            return
        thm = get_theme()
        style, emoji = self.LEVEL_STYLES.get(record.levelno, ("white", "•"))
        lvl_name = record.levelname.lower()
        msg = self.format(record)
        name_part = f"[dim]{record.name}[/dim]" if record.name != "root" else ""

        _con.print(
            f"[{thm.accent}]{emoji}[/{thm.accent}] [{style}]{lvl_name}[/{style}] {name_part} {msg}"
        )


def _vibe_print(*args, sep=" ", end="\n", file=None, flush=False):
    """the main print override — this is where the magic happens"""
    if not _active or file not in (None, sys.stdout):
        _orig_print(*args, sep=sep, end=end, file=file, flush=flush)
        return

    thm = get_theme()

    # single arg that can be tablified
    if len(args) == 1:
        obj = args[0]
        tbl = None

        if is_df(obj):
            tbl = try_df_to_table(obj)
        elif should_tablify(obj):
            tbl = make_table(obj)

        if tbl is not None:
            _con.print(tbl)
            return

    # fallback to rich print (handles markup, syntax highlighting for code strings, etc)
    out = sep.join(str(a) for a in args)
    _con.print(out, end=end, highlight=True)


def _vibe_excepthook(exc_type, exc_val, exc_tb):
    """pretty exceptions"""
    if not _active:
        _orig_excepthook(exc_type, exc_val, exc_tb)
        return

    thm = get_theme()
    hint = get_err_hint(exc_val)

    _err_con.print()
    _err_con.print(
        Panel(
            Traceback.from_exception(exc_type, exc_val, exc_tb, show_locals=False, max_frames=8),
            title=f"[bold {thm.error}]{thm.emoji_err}  {exc_type.__name__}[/bold {thm.error}]",
            border_style=thm.error,
            expand=False,
        )
    )
    if hint:
        _err_con.print(
            Panel(
                f"[{thm.accent}]{hint}[/{thm.accent}]",
                title=f"[{thm.warn}]💡 hint[/{thm.warn}]",
                border_style=thm.warn,
                expand=False,
            )
        )


def enable():
    """turn on python_vibe. call this at top of script."""
    global _active, _vibe_logger_handler

    if _active:
        return  # already on, skip

    _active = True
    builtins.print = _vibe_print
    sys.excepthook = _vibe_excepthook

    # attach log handler to root logger
    _vibe_logger_handler = VibeHandler()
    _vibe_logger_handler.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(message)s")  # we handle formatting ourselves
    _vibe_logger_handler.setFormatter(fmt)

    root_log = logging.getLogger()
    # remove existing stream handlers so we dont double print
    root_log.handlers = [h for h in root_log.handlers if not isinstance(h, logging.StreamHandler)]
    root_log.addHandler(_vibe_logger_handler)
    if root_log.level == logging.WARNING or root_log.level == 0:
        root_log.setLevel(logging.DEBUG)

    thm = get_theme()
    _con.print(
        f"[{thm.primary}]⚡ python_vibe enabled[/{thm.primary}] [{thm.accent}]theme: {thm.name}[/{thm.accent}] [{thm.secondary}]{thm.emoji_run}[/{thm.secondary}]"
    )


def disable():
    """turn off vibe. go back to ugly."""
    global _active

    if not _active:
        return

    _active = False
    builtins.print = _orig_print
    sys.excepthook = _orig_excepthook

    if _vibe_logger_handler:
        logging.getLogger().removeHandler(_vibe_logger_handler)

    _orig_print("python_vibe disabled.")


def log(msg: str, level: str = "info"):
    """manual styled log output"""
    thm = get_theme()
    level = level.lower()
    style_map = {
        "debug": ("dim", "🔍"),
        "info": (thm.primary, thm.emoji_run),
        "warn": (thm.warn, thm.emoji_warn),
        "warning": (thm.warn, thm.emoji_warn),
        "error": (thm.error, thm.emoji_err),
    }
    style, emoji = style_map.get(level, (thm.primary, "•"))
    _con.print(f"[{style}]{emoji} {msg}[/{style}]")


def success(msg: str):
    thm = get_theme()
    _con.print(Panel(f"[bold {thm.success}]{thm.emoji_ok}  {msg}[/bold {thm.success}]", border_style=thm.success, expand=False))


def warn(msg: str):
    thm = get_theme()
    _con.print(Panel(f"[{thm.warn}]{thm.emoji_warn}  {msg}[/{thm.warn}]", border_style=thm.warn, expand=False))


def error(msg: str):
    thm = get_theme()
    _err_con.print(Panel(f"[bold {thm.error}]{thm.emoji_err}  {msg}[/bold {thm.error}]", border_style=thm.error, expand=False))


def track(iterable, desc: str = "working", total: int = None):
    """wrap any iterable with a progress bar"""
    thm = get_theme()
    prog = Progress(
        SpinnerColumn(style=thm.primary),
        TextColumn(f"[{thm.secondary}]{desc}[/{thm.secondary}]"),
        BarColumn(bar_width=None, style=thm.accent, complete_style=thm.primary),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=_con,
        transient=False,
    )
    try:
        _total = total if total is not None else (len(iterable) if hasattr(iterable, "__len__") else None)
        with prog:
            task = prog.add_task(desc, total=_total)
            for item in iterable:
                yield item
                prog.advance(task)
    except KeyboardInterrupt:
        _con.print(f"\n[{thm.warn}]interrupted[/{thm.warn}]")
        raise


def table(data: Any, title: str = ""):
    """manually render a table"""
    thm = get_theme()
    if is_df(data):
        tbl = try_df_to_table(data, title=title)
    else:
        tbl = make_table(data, title=title)
    if tbl:
        _con.print(tbl)
    else:
        _con.print(f"[dim]cant tablify this: {type(data).__name__}[/dim]")


def inspect(obj: Any, title: str = ""):
    """pretty inspect any object"""
    from rich import inspect as rich_inspect
    rich_inspect(obj, title=title or None, console=_con)


def vibe(_func=None, *, time_it=True, show_args=False, show_ret=False):
    """decorator: times + logs function calls with style"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            thm = get_theme()
            fname = func.__name__
            tmr = Timer().start()

            if _active and show_args:
                _con.print(f"[{thm.accent}]→ {fname}[/{thm.accent}] args={args} kwargs={kwargs}")
            elif _active:
                _con.print(f"[{thm.accent}]→ {fname}[/{thm.accent}]")

            try:
                result = func(*args, **kwargs)
                tmr.stop()
                if _active:
                    msg = f"[{thm.success}]{thm.emoji_ok} {fname}[/{thm.success}] [{thm.secondary}]{tmr.fmt()}[/{thm.secondary}]"
                    if show_ret:
                        msg += f" → {result!r}"
                    _con.print(msg)
                return result
            except Exception as e:
                tmr.stop()
                if _active:
                    _con.print(f"[{thm.error}]{thm.emoji_err} {fname} failed ({tmr.fmt()}): {e}[/{thm.error}]")
                raise
        return wrapper

    if _func is not None:
        return decorator(_func)
    return decorator


def is_active() -> bool:
    return _active
