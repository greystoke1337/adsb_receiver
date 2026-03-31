# ADS-B Receiver — Claude Context

## What this repo is
Two Python display scripts for an Adafruit PiTFT 3.5" (HX8357D, 480×320) attached to a Raspberry Pi 3B+:

| File | Purpose |
|------|---------|
| `display.py` | Original overhead tracker — fetches from `https://api.overheadtracker.com`, runs on a separate Pi with pygame 2.x / SDL2 |
| `tft_display.py` | ADS-B receiver display — reads local readsb JSON, runs on the airplanes.live Pi with pygame 1.9.6 / SDL1 |

## Target Pi (airplanes.live)
- **Host**: airplanes.local (192.168.86.24), SSH: `pi` / `checkmate1989`
- **OS**: Raspbian Bullseye, Linux 6.1.21-v7+, armv7l
- **Location**: Russell Lea, Sydney — lat -33.855130, lon 151.141500
- **Python access**: paramiko (sshpass is not installed, no key auth)
- **SFTP uploads**: write to local temp file, then upload via paramiko SFTP — never use bash heredocs (single quotes in Python source break them)

## Display hardware
- Generic 3.5" SPI TFT (lcdwiki.com/3.5inch_RPi_Display), **ILI9486** controller, XPT2046 touch, 480×320
- Device tree overlay: `dtoverlay=tft35a:rotate=90` in `/boot/config.txt`
  - Overlay file: `/boot/overlays/tft35a.dtbo` (from goodtft/LCD-show repo)
  - DC = GPIO 24, RST = GPIO 25 (active low)
- **Framebuffer**: `/dev/fb0` — fbtft (`fb_ili9486`) takes fb0; `vc4-kms-v3d` uses DRM/KMS so TFT driver claims fb0
- **fbcon**: must unbind before writing to fb0: `echo 0 > /sys/class/vtconsole/vtcon1/bind`
  - Also set in systemd service as `ExecStartPre`

## Rendering approach (do not change without good reason)
```python
os.environ['SDL_VIDEODRIVER'] = 'dummy'   # SDL1/pygame 1.9.6 — NOT 'offscreen' (SDL2 only)
os.environ['SDL_NOMOUSE']     = '1'
```

Font rendering — **antialias must be False**, explicit background color required:
```python
font = pygame.font.Font('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
text = font.render('Hello World', False, (255, 255, 255), (0, 0, 0))  # antialias=False
```

Framebuffer flush — transpose + 180° software flip (tft35a:rotate=90 is physically upside-down):
```python
arr    = pygame.surfarray.array3d(screen).transpose(1, 0, 2)
arr    = np.rot90(arr, 2)  # 180° flip to correct orientation
r      = arr[:, :, 0].astype(np.uint16)
g      = arr[:, :, 1].astype(np.uint16)
b      = arr[:, :, 2].astype(np.uint16)
rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
fb.seek(0)
fb.write(rgb565.astype('<u2').tobytes())   # little-endian — critical
fb.flush()
```

Before writing to fb0, unbind fbcon: `echo 0 > /sys/class/vtconsole/vtcon1/bind`

`display.py` uses `SDL_VIDEODRIVER=offscreen` and `/dev/fb1` — different Pi with pygame 2.x / SDL2.

## Data sources (tft_display.py)
| File | Content |
|------|---------|
| `/run/readsb/aircraft.json` | Live aircraft list, updated every ~1s by readsb |
| `/run/readsb/receiver.json` | Receiver lat/lon (auto-loads at startup) |
| `/run/readsb/stats.json` | Message counts, signal/noise, strong signal warnings |

## Systemd service
`/etc/systemd/system/tft-display.service` — `User=root`, `ExecStartPre=/bin/sleep 3`, `Restart=on-failure`

## Deploying changes
1. Edit `tft_display.py` locally in this repo
2. Upload via paramiko SFTP to `/home/pi/tft_display.py`
3. `sudo systemctl restart tft-display.service`
4. Check: `sudo journalctl -u tft-display.service -n 30`
