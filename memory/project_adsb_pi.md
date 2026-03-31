---
name: ADS-B Pi TFT Display Setup
description: Pi host details, framebuffer quirks, SDL version, display hardware (ILI9486), deploy workflow for the airplanes.live Pi
type: project
---

Raspberry Pi 3B+ running airplanes.live image (Raspbian Bullseye) with a generic lcdwiki 3.5" SPI TFT (ILI9486 controller, XPT2046 touch), 480×320.

- **Host**: airplanes.local (192.168.86.24), SSH: pi/checkmate1989
- **Location**: Russell Lea, Sydney (-33.855130, 151.141500)
- **Display hardware**: Generic lcdwiki 3.5" (NOT Adafruit HX8357D) — ILI9486 controller, XPT2046 touch
- **dtoverlay**: `tft35a:rotate=90` from goodtft/LCD-show repo (dtbo at `/boot/overlays/tft35a.dtbo`)
- **GPIO**: DC=GPIO24, RST=GPIO25 (active low)
- **Framebuffer**: `/dev/fb0` — fb_ili9486 claims fb0; vc4-kms-v3d uses DRM/KMS
- **Display script**: `/home/pi/hello_world.py` (sanity check); full ADS-B UI not yet built
- **Service**: `tft-display.service` (not yet deployed for new display)
- **Data source**: `/run/readsb/aircraft.json`, `/run/readsb/stats.json`, `/run/readsb/receiver.json`
- **Repo file**: `hello_world.py` in the adsb_receiver repo (tft_display.py not yet created)

**Why: SDL_VIDEODRIVER=dummy** — Pi has pygame 1.9.6 (SDL1) which doesn't support `offscreen` driver (SDL2 only). Use `dummy` instead, flush via surfarray → RGB565 → fb0 write.

**Why: little-endian RGB565** — framebuffer requires `rgb565.astype('<u2').tobytes()`. Native `.tobytes()` produces wrong byte order → white screen.

**Why: ILI9486 not HX8357D** — Initial assumption was wrong. Confirmed via: XPT2046 touch chip (not STMPE610 which Adafruit uses), stmpe probe failure in dmesg, and user-provided lcdwiki product URL.

**How to apply:** Always use `dummy`, always write to `/dev/fb0`, always use `<u2` byte order. tft35a overlay is the correct one for this board.
