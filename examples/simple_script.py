"""
simple_script.py — before/after demo
run this first to see what python_vibe actually does
"""

# ---- comment these 2 lines to see the "before" version ----
import python_vibe
python_vibe.enable()
# -----------------------------------------------------------

import time
import logging

log = logging.getLogger(__name__)

# --- boring data
user = {"name": "rahul verma", "city": "bhopal", "score": 9001, "active": True, "balance": 1337.42}
friends = [
    {"name": "priya", "city": "indore", "score": 8800},
    {"name": "karan", "city": "pune", "score": 7200},
    {"name": "disha", "city": "bhopal", "score": 9500},
]
tags = ["python", "bhopal", "chai", "open-source", "vibe"]


print("=== user info ===")
print(user)

print("\n=== friends ===")
print(friends)

print("\n=== tags ===")
print(tags)

print("\n=== logging test ===")
log.debug("debug message — usually ignored but python_vibe shows it")
log.info("this is an info log")
log.warning("careful bhai")
log.error("something broke (fake error for demo)")

print("\n=== progress ===")
for _ in python_vibe.track(range(50), desc="doing stuff"):
    time.sleep(0.03)

python_vibe.success("all done! ☕")



