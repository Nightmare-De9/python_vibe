# ⚡ python_vibe

<div align="center">

```
asci--
```

**make your boring python scripts look like a fucking movie** 🎬

[![PyPI version](https://img.shields.io/pypi/v/pyvibe?color=ff6b6b&style=flat-square)](https://pypi.org/project/pyvibe)
[![Python](https://img.shields.io/pypi/pyversions/pyvibe?color=ffd93d&style=flat-square)](https://pypi.org/project/pyvibe)
[![License: MIT](https://img.shields.io/badge/License-MIT-00b4d8?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/yourname/pyvibe?color=ff9f43&style=flat-square)](https://github.com/yourname/pyvibe/stargazers)
[![Downloads](https://img.shields.io/pypi/dm/pyvibe?color=a29bfe&style=flat-square)](https://pypi.org/project/pyvibe)

</div>

---

## 🤔 what is this

you write python. your terminal output looks like dogwater.  
**pyvibe fixes that. with zero effort.**

two lines. that's it.

```python
import pyvibe
pyvibe.enable()
```

now every print, every loop, every error, every table — automatic cinema.  
no rewrites. no boilerplate. your existing code just... glows up.

---

## 📦 install

```bash
pip install pyvibe
```

want the full dashboard mode (textual TUI)?

```bash
pip install pyvibe[full]
```

---

## 🚀 quick start

### before pyvibe 😭

```python
data = {"name": "rahul", "score": 99, "city": "bhopal"}
print(data)
# {'name': 'rahul', 'score': 99, 'city': 'bhopal'}

for i in range(100):
    process(i)
# [nothing. just cursor blinking. you questioning your life choices.]
```

### after pyvibe 🔥

```python
import pyvibe
pyvibe.enable()

data = {"name": "rahul", "score": 99, "city": "bhopal"}
print(data)
# ┌─────────────────────────────────┐
# │  name   │  score  │    city    │
# ├─────────┼─────────┼────────────┤
# │  rahul  │   99    │  bhopal    │
# └─────────────────────────────────┘

for i in pyvibe.track(range(100)):
    process(i)
# ⠿ Processing  ████████████░░░░  73%  [0:00:02] item 73/100
```

---

## 🎬 demo

> 📸 **[GIF PLACEHOLDER]** — imagine a dark terminal with neon green animations, animated progress bars, beautiful tables, glowing error panels. that's what this looks like. gif coming soon, too busy shipping.

---

## 📋 table of contents

- [install](#-install)
- [quick start](#-quick-start)
- [themes](#-theme-gallery)  
- [features](#-features)
- [api reference](#-api-reference)
- [why it slaps](#-why-it-slaps)
- [examples](#-examples)
- [contributing](#-contributing)

---

## 🎨 theme gallery

pyvibe ships with 10 handcrafted themes. pick your vibe.

| theme | description | feel |
|-------|-------------|------|
| `cyber` | neon blue + electric green, dark bg | hacker movie protagonist |
| `masala` | warm oranges, saffron, deep reds | chai, spice, chaos. very desi. |
| `chai_mode` | earthy browns, cream, soft gold | 2am chai and chill |
| `neon` | full rgb overload, dark void bg | synthwave fever dream |
| `retro` | amber/green monochrome CRT vibes | your grandpa's terminal (cool version) |
| `dracula` | purple, pink, clean. the classic | every dev's comfort food |
| `ocean` | cool blues, teals, calm whites | productive, clean, focused |
| `desi_chaos` | random colour per run. pure anarchy | for when you've stopped caring |
| `minimal` | no colors. just clean structure | presentation mode, boss walked in |
| `midnight` | deep navy + soft lavender | 3am grind, lofi beats, shipping |

```python
pyvibe.set_theme("masala")  # ☕ desi mode activated
pyvibe.set_theme("cyber")   # 🔵 go full hackerman
pyvibe.set_theme("chai_mode")  # works best with actual chai
```

---

## ✨ features

- 🖨️ **auto-pretty print** — dicts, lists, dataframes → instant tables. no code changes.
- 📊 **smart progress** — `pyvibe.track(iterable)` wraps any loop with a live bar
- 💥 **cinematic errors** — exceptions get formatted with context, suggestions, syntax highlighted
- 🎨 **10 themes** — swap vibes with one line
- 📋 **auto tables** — any list-of-dicts becomes a rich table automatically
- 🧰 **log takeover** — your `logging` module output gets beautified too
- ⏱️ **@vibe decorator** — time + log any function with one decorator
- 🖥️ **live dashboard** — optional TUI dashboard for long-running scripts (needs `[full]`)
- 🏥 **error doctor** — smart error explanations with hints (stub, improving)
- ☕ **masala mode** — chai emoji on success, because we're from bhopal and we can

---

## 📖 api reference

```python
import pyvibe

# core
pyvibe.enable()                    # turn on the magic
pyvibe.disable()                   # back to boring (why tho)
pyvibe.set_theme("cyber")         # change theme anytime

# progress
for item in pyvibe.track(data, desc="crunching"):
    process(item)

# decorators
@pyvibe.vibe
def my_function():
    ...
# auto logs timing, args, return val with style

# manual stuff
pyvibe.log("something happened")  # styled info log
pyvibe.success("it worked!")      # ✅ green + celebratory
pyvibe.warn("hmm")                # ⚠️  warning panel
pyvibe.error("oh no")             # 💥 error panel

# tables
pyvibe.table(list_of_dicts)       # render a table directly
pyvibe.inspect(any_object)        # pretty inspect any object

# dashboard (needs pyvibe[full])
pyvibe.start_dashboard()
```

---

## 🔥 why it slaps

**rich is great.** but you have to rewrite your whole print logic.  
**loguru is cool.** but it's just logging.  
**textual is amazing.** but it's a whole framework.

pyvibe is different. it wraps everything **automatically**.  
your existing code. zero changes. maximum vibe.

it's the library you install at 2am and forget to remove because why would you.

---

## 📁 examples

check the `examples/` folder:

- `simple_script.py` — basic before/after demo  
- `data_pipeline.py` — pandas pipeline with auto-table  
- `training_loop.py` — fake ML training loop, looks real  
- `fastapi_demo.py` — middleware for request logging

```bash
cd examples
python training_loop.py  # run this one first. trust me.
```

---

## 🤝 contributing

PRs welcome. issues welcome. vibes mandatory.

```bash
git clone https://github.com/yourname/pyvibe
cd pyvibe
pip install -e ".[dev]"
pytest tests/
```

ideas for contribution:
- new themes (especially regional/cultural ones)
- better error suggestions
- jupyter notebook support
- more auto-detect patterns

if you add a theme, name it something fun. no `theme_blue_v2` garbage.

---

## 📜 license

MIT. do whatever. just don't remove the chai emoji.

---

<div align="center">

**if this made your terminal less ugly, smash that ⭐**  
*built with ☕ chai and mild sleep deprivation in bhopal, india*

</div>
