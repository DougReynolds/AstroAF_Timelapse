import threading
import common.constants as constants
import services.state_service as state_service
from datetime import datetime

_poll_timer = None


def _log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [ARMING] {message}", flush=True)


def _poll_tick():
    _log("poll tick")
    global _poll_timer
    state_service.check_printer_state()
    if state_service.is_armed():
        _log("restarting poll timer (5s)")
        _poll_timer = threading.Timer(5.0, _poll_tick)
        _poll_timer.daemon = True
        _poll_timer.start()


def timelapse_arm():
    _log("arm request received")
    global _poll_timer
    state_service.arm()
    if _poll_timer is None or not _poll_timer.is_alive():
        _log("starting poll timer immediately")
        _poll_timer = threading.Timer(0.0, _poll_tick)
        _poll_timer.daemon = True
        _poll_timer.start()
    return {
        "code": constants.HTTP_OK,
        "payload": {
            "action": constants.ACTION_ARM,
            "status": constants.STATUS_FINISHED,
            "armed": True,
        },
    }
