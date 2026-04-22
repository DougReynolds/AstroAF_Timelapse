import subprocess
from datetime import datetime
import tempfile
import common.constants as constants
from pathlib import Path

ACTION_RENDER = "render"
STATUS_FINISHED = "finished"
STATUS_ERROR = "error"
FRAME_PATTERN = "%Y%m%d_%H%M%S.jpg"
FPS = "30"


def render_frames():
    try:
        frame_count = len(list(constants.TIMELAPSE_DEST_DIR.glob("*.jpg")))
        if frame_count == 0:
            return {
                "code": constants.HTTP_ERROR,
                "payload": {
                    "action": ACTION_RENDER,
                    "status": STATUS_ERROR,
                    "error": "no frames found",
                },
            }

        output_dir = constants.ARCHIVE_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = datetime.now().strftime("%Y%m%d_%H%M%S_timelapse.mp4")
        output_path = output_dir / output_file

        frame_files = sorted(constants.TIMELAPSE_DEST_DIR.glob("*.jpg"))

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as manifest:
            manifest_path = Path(manifest.name)
            for frame in frame_files:
                manifest.write(f"file '{frame}'\n")

        command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(manifest_path),
            "-r",
            FPS,
            "-c:v",
            "h264_v4l2m2m",
            "-b:v",
            "4M",
            "-g",
            "1",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output_path),
        ]

        result = subprocess.run(command, check=True, capture_output=True, text=True)

        if not output_path.exists() or output_path.stat().st_size == 0:
            raise Exception("render produced empty output")

        manifest_path.unlink(missing_ok=True)

        return {
            "code": constants.HTTP_OK,
            "payload": {
                "action": ACTION_RENDER,
                "status": STATUS_FINISHED,
                "framecount": frame_count,
                "file": output_file,
                "path": str(output_path),
            },
        }
    except Exception as error:
        try:
            manifest_path.unlink(missing_ok=True)
        except Exception:
            pass
        return {
            "code": constants.HTTP_ERROR,
            "payload": {
                "action": ACTION_RENDER,
                "status": STATUS_ERROR,
                "error": str(error),
            },
        }
