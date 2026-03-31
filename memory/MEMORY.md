# Memory Index

- [ADS-B Pi TFT Display Setup](project_adsb_pi.md) — Pi host, ILI9486/tft35a hardware, fb0/SDL1/dummy quirks, RGB565 byte order
- [Pi Deploy Method](feedback_deploy.md) — paramiko SFTP only; no sshpass, no heredocs for Python files
- [pygame Font Rendering on Pi](feedback_pygame_font.md) — must use DejaVuSans path, antialias=False, explicit bg color or you get solid rectangles
- [TFT Orientation — Software Flip Only](feedback_tft_orientation.md) — screen is upside-down; fix with np.rot90(arr,2), never change dtoverlay rotate param
- [Stale python3 Processes Overwrite fb0](feedback_fb0_stale_processes.md) — always killall -9 python3 before testing to avoid stale nohup processes masking output
