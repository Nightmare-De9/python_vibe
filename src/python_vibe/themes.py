from dataclasses import dataclass, field
from typing import Dict, Optional
import random


@dataclass
class Theme:
    name: str
    primary: str
    secondary: str
    accent: str
    success: str
    warn: str
    error: str
    bg: Optional[str]
    border_style: str
    panel_style: str
    emoji_ok: str
    emoji_err: str
    emoji_warn: str
    emoji_run: str
    header_gradient: list = field(default_factory=list)


# theme defs — dont touch monkey patch
THEMES: Dict[str, Theme] = {
    "cyber": Theme(
        name="cyber",
        primary="bright_cyan",
        secondary="bright_green",
        accent="bright_blue",
        success="bright_green",
        warn="bright_yellow",
        error="bright_red",
        bg=None,
        border_style="bright_cyan",
        panel_style="bright_cyan on grey11",
        emoji_ok="⚡",
        emoji_err="💀",
        emoji_warn="⚠️",
        emoji_run="🔵",
        header_gradient=["bright_cyan", "bright_blue", "bright_green"],
    ),
    "masala": Theme(
        name="masala",
        primary="dark_orange",
        secondary="gold1",
        accent="orange_red1",
        success="chartreuse2",
        warn="yellow",
        error="red1",
        bg=None,
        border_style="dark_orange",
        panel_style="dark_orange on grey15",
        emoji_ok="☕",
        emoji_err="🌶️",
        emoji_warn="🍋",
        emoji_run="🫚",
        header_gradient=["dark_orange", "gold1", "orange_red1"],
    ),
    "chai_mode": Theme(
        name="chai_mode",
        primary="tan",
        secondary="wheat1",
        accent="gold3",
        success="pale_green3",
        warn="khaki1",
        error="light_coral",
        bg=None,
        border_style="tan",
        panel_style="tan on grey7",
        emoji_ok="☕",
        emoji_err="😬",
        emoji_warn="🤔",
        emoji_run="🫖",
        header_gradient=["tan", "wheat1", "gold3"],
    ),
    "neon": Theme(
        name="neon",
        primary="bright_magenta",
        secondary="bright_cyan",
        accent="bright_yellow",
        success="bright_green",
        warn="bright_yellow",
        error="bright_red",
        bg=None,
        border_style="bright_magenta",
        panel_style="bright_magenta on grey3",
        emoji_ok="✨",
        emoji_err="🔴",
        emoji_warn="🟡",
        emoji_run="🟣",
        header_gradient=["bright_magenta", "bright_cyan", "bright_yellow"],
    ),
    "retro": Theme(
        name="retro",
        primary="green3",
        secondary="dark_green",
        accent="green_yellow",
        success="green3",
        warn="yellow3",
        error="red3",
        bg=None,
        border_style="green3",
        panel_style="green3 on grey3",
        emoji_ok="►",
        emoji_err="✗",
        emoji_warn="!",
        emoji_run="▶",
        header_gradient=["green3", "dark_green"],
    ),
    "dracula": Theme(
        name="dracula",
        primary="medium_purple",
        secondary="hot_pink",
        accent="plum1",
        success="chartreuse2",
        warn="orange1",
        error="red1",
        bg=None,
        border_style="medium_purple",
        panel_style="medium_purple on grey11",
        emoji_ok="🧛",
        emoji_err="🩸",
        emoji_warn="🌙",
        emoji_run="💜",
        header_gradient=["medium_purple", "hot_pink", "plum1"],
    ),
    "ocean": Theme(
        name="ocean",
        primary="steel_blue1",
        secondary="deep_sky_blue1",
        accent="turquoise2",
        success="aquamarine1",
        warn="light_yellow3",
        error="light_salmon1",
        bg=None,
        border_style="steel_blue1",
        panel_style="steel_blue1 on grey15",
        emoji_ok="🌊",
        emoji_err="🔴",
        emoji_warn="⚡",
        emoji_run="💧",
        header_gradient=["steel_blue1", "deep_sky_blue1", "turquoise2"],
    ),
    "desi_chaos": Theme(  # this shit works lol
        name="desi_chaos",
        primary=random.choice(["bright_red", "bright_green", "bright_cyan", "bright_magenta", "bright_yellow"]),
        secondary=random.choice(["bright_blue", "bright_white", "gold1", "dark_orange"]),
        accent=random.choice(["hot_pink", "chartreuse2", "orange_red1"]),
        success="bright_green",
        warn="bright_yellow",
        error="bright_red",
        bg=None,
        border_style=random.choice(["bright_red", "bright_cyan", "bright_magenta"]),
        panel_style="bright_white on grey7",
        emoji_ok="🎉",
        emoji_err="😤",
        emoji_warn="🙃",
        emoji_run="🎲",
        header_gradient=["bright_red", "bright_yellow", "bright_green", "bright_cyan", "bright_magenta"],
    ),
    "minimal": Theme(
        name="minimal",
        primary="white",
        secondary="bright_white",
        accent="grey74",
        success="white",
        warn="grey74",
        error="white",
        bg=None,
        border_style="grey74",
        panel_style="white on grey3",
        emoji_ok="✓",
        emoji_err="✗",
        emoji_warn="·",
        emoji_run="→",
        header_gradient=["white", "grey74"],
    ),
    "midnight": Theme(
        name="midnight",
        primary="medium_slate_blue",
        secondary="light_slate_blue",
        accent="plum2",
        success="pale_turquoise1",
        warn="light_goldenrod2",
        error="light_pink1",
        bg=None,
        border_style="medium_slate_blue",
        panel_style="medium_slate_blue on grey7",
        emoji_ok="🌙",
        emoji_err="💫",
        emoji_warn="⭐",
        emoji_run="🌌",
        header_gradient=["medium_slate_blue", "light_slate_blue", "plum2"],
    ),
}

DEFAULT_THEME = "cyber"


class ThemeManager:
    def __init__(self):
        self._current = THEMES[DEFAULT_THEME]
        self._name = DEFAULT_THEME

    @property
    def current(self) -> Theme:
        return self._current

    @property
    def name(self) -> str:
        return self._name

    def set(self, name: str):
        if name not in THEMES:
            avail = ", ".join(THEMES.keys())
            raise ValueError(f"unknown theme '{name}'. available: {avail}")
        # re-instantiate desi_chaos each time for fresh randomness
        if name == "desi_chaos":
            THEMES["desi_chaos"] = Theme(
                name="desi_chaos",
                primary=random.choice(["bright_red", "bright_green", "bright_cyan", "bright_magenta", "bright_yellow"]),
                secondary=random.choice(["bright_blue", "bright_white", "gold1", "dark_orange"]),
                accent=random.choice(["hot_pink", "chartreuse2", "orange_red1"]),
                success="bright_green",
                warn="bright_yellow",
                error="bright_red",
                bg=None,
                border_style=random.choice(["bright_red", "bright_cyan", "bright_magenta"]),
                panel_style="bright_white on grey7",
                emoji_ok="🎉",
                emoji_err="😤",
                emoji_warn="🙃",
                emoji_run="🎲",
                header_gradient=["bright_red", "bright_yellow", "bright_green", "bright_cyan", "bright_magenta"],
            )
        self._current = THEMES[name]
        self._name = name

    def list_themes(self):
        return list(THEMES.keys())


# singleton
_mgr = ThemeManager()


def get_theme() -> Theme:
    return _mgr.current


def set_theme(name: str):
    _mgr.set(name)


def get_manager() -> ThemeManager:
    return _mgr
