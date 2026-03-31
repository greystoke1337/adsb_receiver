---
name: Pi Deploy Method
description: How to get files onto the Pi — paramiko SFTP only, no heredocs, no sshpass
type: feedback
---

Use Python paramiko for all SSH and file transfer to the Pi. sshpass is not installed and there is no key-based auth configured.

**Why:** sshpass unavailable on the Windows dev machine; password auth only on the Pi side.

**How to apply:** When deploying updated scripts:
1. Write the file locally in the repo (`tft_display.py`)
2. Upload via `paramiko.SFTPClient` to `/home/pi/tft_display.py`
3. Run restart command via `paramiko.SSHClient.exec_command`

Never use bash heredocs to write Python files on the Pi — single quotes inside the Python source break the shell quoting. Always SFTP the file directly.
