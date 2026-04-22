import requests
import common.constants as constants
import services.capture_service as capture_service
import services.render_service as render_service
import services.cleanup_service as cleanup_service
from datetime import datetime

_armed = False
_current_state = None
_capture_timer = None
_session_started = False
CAPTURE_INTERVAL = 30.0


def _log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [STATE] {message}", flush=True)


def arm():
    global _armed, _current_state, _session_started
    _log("armed")
    _armed = True
    _current_state = None
    _session_started = False


def is_armed():
    return _armed


def _capture_tick():
    _log(f"capture tick (armed={_armed}, state={_current_state})")
    global _capture_timer
    if _armed and _current_state == "printing":
        capture_service.capture_new_frame()
        _capture_timer = __import__("threading").Timer(CAPTURE_INTERVAL, _capture_tick)
        _capture_timer.daemon = True
        _capture_timer.start()


def _start_capture_timer():
    _log("start capture timer requested")
    global _capture_timer
    if _capture_timer is None or not _capture_timer.is_alive():
        _log("starting capture timer immediately")
        _capture_timer = __import__("threading").Timer(0.0, _capture_tick)
        _capture_timer.daemon = True
        _capture_timer.start()


def _stop_capture_timer():
    _log("stop capture timer requested")
    global _capture_timer
    if _capture_timer is not None:
        _capture_timer.cancel()
    _capture_timer = None


def _finalize_session():
    _log("finalizing session")
    global _armed, _session_started
    _stop_capture_timer()
    render_service.render_frames()
    cleanup_service.cleanup_job()
    _armed = False
    _session_started = False


def check_printer_state():
    global _current_state, _armed, _session_started
    if not _armed:
        _log("poll skipped (not armed)")
        return
    try:
        response = requests.get(
            constants.BASE_URL + ":7125/printer/objects/query?webhooks&print_stats",
            timeout=3,
        )
        data = response.json()
        state = data["result"]["status"]["print_stats"]["state"]
        _log(f"polled state={state}")
    except Exception as error:
        _log(f"poll error: {error}")
        return

    prev_state = _current_state
    _log(f"previous state={prev_state}")

    if state != prev_state:
        _log(f"state change: {prev_state} -> {state}")
        if state == "printing":
            _session_started = True
            _log("session started")
        if state == "printing":
            _start_capture_timer()
        elif state == "paused":
            _stop_capture_timer()
        elif state in ["complete", "cancelled", "error"]:
            if _session_started:
                _finalize_session()
            else:
                _log("ignoring terminal state before session start")

    _current_state = state
