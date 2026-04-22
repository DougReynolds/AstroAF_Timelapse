from pathlib import Path
from urllib.request import urlopen
from datetime import datetime
import common.constants as constants


constants.TIMELAPSE_DEST_DIR.mkdir(parents=True, exist_ok=True)


def _log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [CAPTURE] {message}", flush=True)


def capture_new_frame():
    try:
        _log("capture requested")
        timestamp = datetime.now()
        filename = timestamp.strftime("%Y%m%d_%H%M%S.jpg")
        filepath = constants.TIMELAPSE_DEST_DIR / filename

        with urlopen(
            constants.BASE_URL + ":8080/?action=snapshot", timeout=3
        ) as response:
            data = response.read()
            _log(f"snapshot received ({len(data)} bytes)")

        with open(filepath, "wb") as file_handle:
            file_handle.write(data)
            _log(f"saved {filename}")

        return {
            "code": constants.HTTP_OK,
            "payload": {
                "ok": constants.OK_TRUE,
                "file": filename,
                "timestamp": timestamp.isoformat(),
            },
        }
    except Exception as error:
        _log(f"error: {error}")
        return {
            "code": constants.HTTP_ERROR,
            "payload": {
                "ok": constants.OK_FALSE,
                "error": str(error),
            },
        }
