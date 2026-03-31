---
name: Stale python3 processes overwrite fb0
description: Old background python3 processes keep writing to fb0 and mask test results — always killall first
type: feedback
---

When display output looks wrong (rectangles, old content, unexpected colors), old `nohup python3` background processes are often still alive and actively overwriting `/dev/fb0`.

**Why:** During debugging, scripts were launched with `nohup ... &` and not always cleanly killed. Multiple python3 processes competed to write fb0, making test results unpredictable and masking the actual script's output.

**How to apply:** Before running any test script on the Pi, always run `sudo killall -9 python3` first to ensure a clean slate. This applies during development/testing; the systemd service handles it in production.
