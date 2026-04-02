"""
python_vibe — make your boring python scripts look like a movie
two lines. that's it.
"""

from .core import (
    enable,
    disable,
    log,
    success,
    warn,
    error,
    track,
    table,
    inspect,
    vibe,
    is_active,
)
from .themes import set_theme, get_theme, get_manager as _thm_mgr

__version__ = "0.1.0"
__all__ = [
    "enable",
    "disable",
    "log",
    "success",
    "warn",
    "error",
    "track",
    "table",
    "inspect",
    "vibe",
    "set_theme",
    "get_theme",
    "is_active",
    "__version__",
]


def list_themes():
    """returns all available theme names"""
    return _thm_mgr().list_themes()
