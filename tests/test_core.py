"""
basic tests — nothing fancy, just making sure things dont explode
"""

import pytest
import builtins
import sys


def test_import():
    import python_vibe
    assert hasattr(python_vibe, "enable")
    assert hasattr(python_vibe, "disable")
    assert hasattr(python_vibe, "track")
    assert hasattr(python_vibe, "vibe")


def test_enable_disable():
    import python_vibe
    orig_print = builtins.print
    python_vibe.enable()
    assert python_vibe.is_active()
    assert builtins.print is not orig_print
    python_vibe.disable()
    assert not python_vibe.is_active()
    assert builtins.print is orig_print


def test_set_theme():
    import python_vibe
    python_vibe.set_theme("masala")
    thm = python_vibe.get_theme()
    assert thm.name == "masala"
    python_vibe.set_theme("cyber")
    assert python_vibe.get_theme().name == "cyber"


def test_bad_theme():
    import python_vibe
    with pytest.raises(ValueError):
        python_vibe.set_theme("doesnt_exist_lol")


def test_list_themes():
    import python_vibe
    themes = python_vibe.list_themes()
    assert isinstance(themes, list)
    assert "cyber" in themes
    assert "masala" in themes
    assert "chai_mode" in themes
    assert len(themes) >= 8


def test_vibe_decorator():
    import python_vibe
    python_vibe.enable()

    @python_vibe.vibe
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5
    python_vibe.disable()


def test_vibe_decorator_exception():
    import python_vibe
    python_vibe.enable()

    @python_vibe.vibe
    def broken():
        raise ValueError("intentional test error")

    with pytest.raises(ValueError):
        broken()

    python_vibe.disable()


def test_track_basic():
    import python_vibe
    python_vibe.enable()
    result = list(python_vibe.track(range(5), desc="testing"))
    assert result == [0, 1, 2, 3, 4]
    python_vibe.disable()


def test_utils_make_table():
    from python_vibe.utils import make_table
    tbl = make_table({"key": "val", "num": 42})
    assert tbl is not None

    tbl2 = make_table([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
    assert tbl2 is not None

    tbl3 = make_table([1, 2, 3])
    assert tbl3 is not None


def test_utils_should_tablify():
    from python_vibe.utils import should_tablify
    assert should_tablify({"a": 1})
    assert should_tablify([{"a": 1}])
    assert not should_tablify("hello")
    assert not should_tablify(42)
    assert not should_tablify([1, 2, 3])  # plain list = no table


def test_timer():
    from python_vibe.utils import Timer
    import time
    t = Timer()
    with t:
        time.sleep(0.05)
    assert t.elapsed >= 0.05
    assert "ms" in t.fmt() or "s" in t.fmt()


def test_err_hint():
    from python_vibe.utils import get_err_hint
    exc = ModuleNotFoundError("No module named 'panda'")
    hint = get_err_hint(exc)
    assert hint is not None
    assert "pip" in hint

    exc2 = KeyError("missing_key")
    assert get_err_hint(exc2) is not None

    exc3 = ZeroDivisionError("division by zero")
    assert get_err_hint(exc3) is not None
