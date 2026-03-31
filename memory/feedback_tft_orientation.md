---
name: TFT display orientation — do not change dtoverlay rotate param
description: Screen is upside-down with tft35a:rotate=90; fix with software np.rot90 not dtoverlay parameter
type: feedback
---

The tft35a display is physically mounted upside-down when using `dtoverlay=tft35a:rotate=90`. The fix is a **software 180° flip** via `np.rot90(arr, 2)` after `transpose(1, 0, 2)`, not changing the dtoverlay rotation parameter.

**Why:** Attempting `dtoverlay=tft35a:rotate=270` (the logical inverse) broke font rendering — text appeared as rectangles again, for unclear reasons (likely scan direction mismatch + old nohup processes conflicting). User rejected further reboots and insisted on software rotation instead.

**How to apply:** Leave `dtoverlay=tft35a:rotate=90` in `/boot/config.txt` untouched. Always apply `arr = np.rot90(arr, 2)` in the framebuffer flush pipeline. Do not suggest changing dtoverlay rotation as a fix for orientation issues.
