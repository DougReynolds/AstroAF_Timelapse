import os
import shutil
import common.constants as constants

ACTION_CLEANUP = "cleanup"
STATUS_FINISHED = "finished"
STATUS_ERROR = "error"


def cleanup_job():
    try:
        for item_path in constants.TIMELAPSE_DEST_DIR.iterdir():
            if item_path.is_file():
                os.remove(item_path)
            elif item_path.is_dir():
                shutil.rmtree(item_path)

        return {
            "code": constants.HTTP_OK,
            "payload": {
                "action": ACTION_CLEANUP,
                "status": STATUS_FINISHED,
            },
        }
    except Exception as error:
        return {
            "code": constants.HTTP_ERROR,
            "payload": {
                "action": ACTION_CLEANUP,
                "status": STATUS_ERROR,
                "error": str(error),
            },
        }
