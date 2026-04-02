"""
live dashboard — needs python_vibe[full] (textual + psutil)
usage: python_vibe.start_dashboard() from your script
"""

_TEXTUAL_AVAIL = False
try:
    from textual.app import App, ComposeResult
    from textual.widgets import Header, Footer, Static, DataTable, Log
    from textual.containers import Container, Horizontal, Vertical
    from textual.reactive import reactive
    from textual import work
    _TEXTUAL_AVAIL = True
except ImportError:
    pass

_PSUTIL_AVAIL = False
try:
    import psutil
    _PSUTIL_AVAIL = True
except ImportError:
    pass

import time
import threading
from typing import List, Tuple, Optional
from collections import deque


# shared state between main script and dashboard
# hacky but it works lol
_dash_state = {
    "logs": deque(maxlen=200),
    "metrics": {},
    "progress": {},
    "running": False,
    "start_time": None,
}


def _get_cpu_mem() -> Tuple[float, float]:
    if not _PSUTIL_AVAIL:
        return 0.0, 0.0
    return psutil.cpu_percent(interval=None), psutil.virtual_memory().percent


def push_log(msg: str):
    """push a log line to dashboard"""
    _dash_state["logs"].append((time.time(), msg))


def push_metric(key: str, val):
    """update a metric in dashboard"""
    _dash_state["metrics"][key] = val


def update_progress(task: str, current: int, total: int):
    """update progress for a named task"""
    _dash_state["progress"][task] = (current, total)


if _TEXTUAL_AVAIL:

    class SysStats(Static):
        """live cpu + mem widget"""

        cpu = reactive(0.0)
        mem = reactive(0.0)

        def on_mount(self):
            self.update_timer = self.set_interval(1.0, self._refresh_stats)

        def _refresh_stats(self):
            c, m = _get_cpu_mem()
            self.cpu = c
            self.mem = m

        def render(self):
            from .themes import get_theme
            thm = get_theme()
            uptime = ""
            if _dash_state["start_time"]:
                elapsed = int(time.time() - _dash_state["start_time"])
                uptime = f"  ⏱ {elapsed//60}m{elapsed%60:02d}s"
            return f"[{thm.primary}]cpu[/{thm.primary}] {self.cpu:.1f}%  [{thm.secondary}]mem[/{thm.secondary}] {self.mem:.1f}%{uptime}"

    class MetricsWidget(Static):
        """renders _dash_state metrics as a lil table"""

        def on_mount(self):
            self.set_interval(0.5, self.refresh)

        def render(self):
            from .themes import get_theme
            thm = get_theme()
            if not _dash_state["metrics"]:
                return "[dim]no metrics yet — use python_vibe.push_metric(k, v)[/dim]"
            lines = []
            for k, v in _dash_state["metrics"].items():
                lines.append(f"[{thm.accent}]{k}[/{thm.accent}]: [{thm.primary}]{v}[/{thm.primary}]")
            return "\n".join(lines)

    class LogWidget(Log):
        """auto-updating log panel"""

        _last_len = 0

        def on_mount(self):
            self.set_interval(0.3, self._sync_logs)

        def _sync_logs(self):
            curr_len = len(_dash_state["logs"])
            if curr_len > self._last_len:
                new_entries = list(_dash_state["logs"])[self._last_len:]
                for ts, msg in new_entries:
                    t = time.strftime("%H:%M:%S", time.localtime(ts))
                    self.write_line(f"[{t}] {msg}")
                self._last_len = curr_len

    class VibeDashboard(App):
        """the main dashboard app"""

        CSS = """
        Screen {
            layout: vertical;
        }
        #top-bar {
            height: 3;
            layout: horizontal;
            background: $surface;
            border: solid $primary;
            padding: 0 1;
        }
        #sys-stats {
            width: 1fr;
            content-align: left middle;
        }
        #metrics-panel {
            height: 10;
            border: solid $primary;
            padding: 1;
            margin: 0 0 1 0;
        }
        #log-panel {
            height: 1fr;
            border: solid $accent;
        }
        """

        BINDINGS = [("q", "quit", "quit")]
        TITLE = "⚡ python_vibe dashboard"

        def compose(self) -> ComposeResult:
            yield Header()
            with Container(id="top-bar"):
                yield SysStats(id="sys-stats")
            yield Static("[bold]metrics[/bold]", classes="section-header")
            yield MetricsWidget(id="metrics-panel")
            yield Static("[bold]logs[/bold]", classes="section-header")
            yield LogWidget(id="log-panel", highlight=True)
            yield Footer()

else:
    VibeDashboard = None  # type: ignore


def start_dashboard(block: bool = True):
    """launch the TUI dashboard. block=False runs in background thread (experimental)"""
    if not _TEXTUAL_AVAIL:
        print("python_vibe dashboard needs textual: pip install python_vibe[full]")
        return

    _dash_state["running"] = True
    _dash_state["start_time"] = time.time()

    app = VibeDashboard()

    if block:
        app.run()
    else:
        # run in thread — kinda janky but works for demos
        t = threading.Thread(target=app.run, daemon=True)
        t.start()
        return t



