"""
training_loop.py — fake ML training. looks extremely legit.
run this one when you want to impress someone
"""

import python_vibe
python_vibe.set_theme("cyber")
python_vibe.enable()

import time
import math
import random


python_vibe.log("initializing model...")
time.sleep(0.4)

# fake model config
cfg = {
    "model": "TransformerMini",
    "layers": 6,
    "heads": 8,
    "hidden_dim": 256,
    "lr": 3e-4,
    "batch_size": 32,
    "epochs": 5,
    "dataset": "vibedata-v2",
    "device": "cpu (no gpu? sadge)",
}

print("training config:")
print(cfg)

time.sleep(0.3)

# training loop
total_epochs = 5
steps_per_epoch = 40

history = []

for epoch in range(1, total_epochs + 1):
    python_vibe.log(f"epoch {epoch}/{total_epochs}")

    epoch_loss = 0.0
    epoch_acc = 0.0

    for step in python_vibe.track(range(steps_per_epoch), desc=f"epoch {epoch}"):
        time.sleep(0.04)
        # fake loss that actually goes down (nice)
        progress = (epoch - 1) * steps_per_epoch + step
        total_steps = total_epochs * steps_per_epoch
        loss = 2.3 * math.exp(-0.8 * progress / total_steps) + random.gauss(0, 0.05)
        acc = 1.0 - math.exp(-1.2 * progress / total_steps) + random.gauss(0, 0.02)
        epoch_loss += loss
        epoch_acc += max(0, min(1, acc))

    avg_loss = epoch_loss / steps_per_epoch
    avg_acc = epoch_acc / steps_per_epoch

    metrics = {
        "epoch": epoch,
        "loss": round(avg_loss, 4),
        "accuracy": f"{avg_acc * 100:.2f}%",
        "lr": cfg["lr"],
    }
    print(metrics)
    history.append(metrics)

print("\ntraining history:")
print(history)

python_vibe.success(f"training complete! final accuracy: {history[-1]['accuracy']} ⚡")



