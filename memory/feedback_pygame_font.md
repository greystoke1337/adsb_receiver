---
name: pygame font rendering on Pi
description: How to render text correctly with pygame 1.9.6 on the Pi — font path, antialias, and background color requirements
type: feedback
---

For pygame text on the Pi TFT, three things are required or you get a solid white/colored rectangle instead of text:

1. **Use explicit TTF path** — `pygame.font.Font('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)`. Both `SysFont(None, ...)` and `Font(None, ...)` fail because `freesansbold.ttf` (pygame's built-in default) does not exist on Raspbian Bullseye.

2. **antialias must be False** — `font.render('text', False, fg_color, bg_color)`. With `antialias=True`, pygame blends text into a transparent background; surfarray then sees the alpha-blended result as a solid filled rectangle.

3. **Explicit background color required** — Pass the background color as the 4th argument to `font.render()`. Without it, the surface has transparency that surfarray reads as a solid block.

**Why:** Spent multiple sessions chasing a "solid white rectangle" bug that turned out to be these three font issues stacked together. Each one alone can cause the rectangle symptom.

**How to apply:** Whenever writing any pygame text for the Pi display, use the DejaVuSans path, antialias=False, and explicit bg color. Don't use SysFont or Font(None) on the Pi.
