

# AstroAF-Timelapse

Timelapse capture and rendering for Moonraker-powered 3D printers using Raspberry Pi automation, lifecycle detection, and hardware-accelerated video encoding.

## Overview

AstroAF-Timelapse is a lightweight Raspberry Pi service that creates print timelapses automatically.

It integrates with Moonraker to detect print lifecycle state changes, captures periodic snapshots during active prints, renders an MP4 using Raspberry Pi hardware acceleration, archives the final video, and cleans up raw frames after success.

Designed and validated on a FlashForge AD5M running Klipper + Moonraker, but the architecture can be adapted to other Moonraker-based printers.

## Features

- Manual arming from printer UI or HTTP endpoint
- Moonraker lifecycle polling
- Automatic frame capture during printing
- Pause/resume aware capture logic
- Hardware-accelerated H.264 rendering (`h264_v4l2m2m`)
- Automatic archive of final MP4
- Automatic cleanup of raw frames
- Simple Python service architecture
- Works well on Raspberry Pi Zero 2 W

## Architecture

1. User arms a timelapse session
2. Service polls Moonraker state
3. When print enters `printing`, frame capture begins
4. Frames are stored to the timelapse directory
5. On `complete` / `cancelled` / `error`, render begins
6. Final MP4 is written to archive storage
7. Raw frames are deleted after successful completion

## Endpoints

- `/armtimelapse` - arm a new session
- `/newframe` - capture one frame manually
- `/render` - render current frames to MP4
- `/cleanup` - delete raw frames
- `/filelist` - list captured frames
- `/filecount` - count captured frames

## Requirements

- Python 3.10+
- Moonraker reachable over network
- FFmpeg with `h264_v4l2m2m` support
- Raspberry Pi camera snapshot source or compatible JPEG endpoint
- Writable storage for frames and archive output

## Example Macro (Klipper)

```ini
[gcode_macro TIMELAPSE_ARM]
gcode:
    RUN_SHELL_COMMAND CMD=TIMELAPSE_ARM

[gcode_shell_command TIMELAPSE_ARM]
command: /usr/bin/curl --connect-timeout 2 --max-time 5 -s http://<pi-ip>:5000/armtimelapse
```

## Project Status

Working milestone reached:

- End-to-end lifecycle confirmed
- Capture confirmed
- Render confirmed
- Cleanup confirmed
- Hardware encoding confirmed on Pi Zero 2 W

## Roadmap

- Improve video scrubbing / seek behavior
- Optional chunked rendering for long prints
- UI status endpoint
- Config file support
- Notifications / Home Assistant integration
- Multi-printer support

## License

MIT License

Copyright (c) 2026 Douglas Reynolds

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.