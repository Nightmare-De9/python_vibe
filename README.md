# ⚡ PYTHON_VIBE

<div align="center">

```
██████╗░██╗░░░██╗████████╗██╗░░██╗░█████╗░███╗░░██╗  ██╗░░░██╗██╗██████╗░███████╗
██╔══██╗╚██╗░██╔╝╚══██╔══╝██║░░██║██╔══██╗████╗░██║  ██║░░░██║██║██╔══██╗██╔════╝
██████╔╝░╚████╔╝░░░░██║░░░███████║██║░░██║██╔██╗██║  ╚██╗░██╔╝██║██████╦╝█████╗░░
██╔═══╝░░░╚██╔╝░░░░░██║░░░██╔══██║██║░░██║██║╚████║  ░╚████╔╝░██║██╔══██╗██╔══╝░░
██║░░░░░░░░██║░░░░░░██║░░░██║░░██║╚█████╔╝██║░╚███║  ░░╚██╔╝░░██║██████╦╝███████╗
╚═╝░░░░░░░░╚═╝░░░░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝  ░░░╚═╝░░░╚═╝╚═════╝░╚══════╝
```


**Make your boring Python scripts look like a fucking movie** 🎬

[![PyPI version](https://img.shields.io/pypi/v/python-vibe?color=ff6b6b\&style=flat-square)](https://pypi.org/project/python-vibe)
[![Python](https://img.shields.io/pypi/pyversions/python-vibe?color=ffd93d\&style=flat-square)](https://pypi.org/project/python-vibe)
[![License: MIT](https://img.shields.io/badge/License-MIT-00b4d8?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Nightmare-De9/python_vibe?color=ff9f43\&style=flat-square)](https://github.com/Nightmare-De9/python_vibe/stargazers)
[![Downloads](https://img.shields.io/pypi/dm/python-vibe?color=a29bfe\&style=flat-square)](https://pypi.org/project/python-vibe)

</div>

---

## 🤔 WHAT IS THIS

You write Python. Your terminal output looks like dogwater.
**python_vibe fixes that. With zero effort.**

Two lines. That’s it.

```python
import python_vibe
python_vibe.enable()
```

Now every print, every loop, every error, every table — automatic cinema.
No rewrites. No boilerplate. Your existing code just... glows up.

---

## 📦 INSTALL

```bash
pip install python-vibe
```

---

## 🚀 QUICK START

### BEFORE python_vibe 😭

```python
data = {"name": "rahul", "score": 99, "city": "bhopal"}
print(data)
# {'name': 'rahul', 'score': 99, 'city': 'bhopal'}

for i in range(100):
    process(i)
# [nothing. just cursor blinking. you questioning your life choices.]
```

---

### AFTER python_vibe 🔥

```python
import python_vibe
python_vibe.enable()

data = {"name": "rahul", "score": 99, "city": "bhopal"}
print(data)
# ┌─────────────────────────────────┐
# │  name   │  score  │    city    │
# ├─────────┼─────────┼────────────┤
# │  rahul  │   99    │  bhopal    │
# └─────────────────────────────────┘

for i in python_vibe.track(range(100)):
    process(i)
# ⠿ Processing  ████████████░░░░  73%  [0:00:02] item 73/100
```

---

## 📋 TABLE OF CONTENTS

* Install
* Quick Start
* Theme Gallery
* Features
* API Reference
* Why It Slaps
* Examples
* Contributing

---

## 🎨 THEME GALLERY

python_vibe ships with 10 handcrafted themes. pick your vibe.

| theme        | description                 | feel                     |
| ------------ | --------------------------- | ------------------------ |
| `cyber`      | neon blue + electric green  | hacker movie protagonist |
| `masala`     | warm oranges, saffron, reds | chai, spice, chaos       |
| `chai_mode`  | earthy browns, soft gold    | 2am chai and chill       |
| `neon`       | rgb overload                | synthwave fever dream    |
| `retro`      | amber/green CRT vibes       | old-school cool          |
| `dracula`    | purple + pink               | dev classic              |
| `ocean`      | cool blues                  | clean + focused          |
| `desi_chaos` | random colours              | pure anarchy             |
| `minimal`    | no colors                   | boss walked in           |
| `midnight`   | navy + lavender             | 3am grind                |

```python
python_vibe.set_theme("masala")
python_vibe.set_theme("cyber")
python_vibe.set_theme("chai_mode")
```

---

## ✨ FEATURES

* 🖨️ **Auto pretty print** — dicts, lists, dataframes → instant tables
* 📊 **Smart progress** — wrap any loop with `track()`
* 💥 **Cinematic errors** — styled exceptions with context
* 🎨 **10 themes** — swap instantly
* 📋 **Auto tables** — list-of-dicts → table
* 🧰 **Logging takeover** — beautifies `logging` output
* ⏱️ **@vibe decorator** — timing + logs
* 🖥️ **Live dashboard** — optional TUI (`[full]`)
* 🏥 **Error doctor** — smart hints (WIP)
* ☕ **Masala mode** — because bhopal

---

## 📖 API REFERENCE

```python
import python_vibe

# core
python_vibe.enable()
python_vibe.disable()
python_vibe.set_theme("cyber")

# progress
for item in python_vibe.track(data, desc="crunching"):
    process(item)

# decorators
@python_vibe.vibe
def my_function():
    ...

# logs
python_vibe.log("something happened")
python_vibe.success("it worked!")
python_vibe.warn("hmm")
python_vibe.error("oh no")

# tables
python_vibe.table(list_of_dicts)
python_vibe.inspect(obj)

# dashboard
python_vibe.start_dashboard()
```

---

## 📁 EXAMPLES

check the `examples/` folder:

* simple_script.py
* data_pipeline.py
* training_loop.py
* fastapi_demo.py

```bash
cd examples
python training_loop.py
```

---

## 🤝 CONTRIBUTING

PRs welcome. issues welcome. vibes mandatory.

```bash
git clone https://github.com/Nightmare-De9/python_vibe
cd python_vibe
pip install -e ".[dev]"
pytest tests/
```

ideas:

* new themes
* better error suggestions
* jupyter support
* smarter detection

---

## 📜 LICENSE

MIT — do whatever. just don’t remove the chai ☕

---

<div align="center">

**If this made your terminal less ugly, smash that ⭐**
Built with ☕ chai and sleep deprivation in Bhopal

</div>

