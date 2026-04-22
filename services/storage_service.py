import common.constants as constants

ACTION_FILELIST = "filelist"
ACTION_FILECOUNT = "filecount"
STATUS_FINISHED = "finished"
STATUS_ERROR = "error"


def get_file_list():
    try:
        file_list = sorted(
            [file_path.name for file_path in constants.TIMELAPSE_DEST_DIR.glob("*.jpg")]
        )
        return {
            "code": constants.HTTP_OK,
            "payload": {
                "action": ACTION_FILELIST,
                "status": STATUS_FINISHED,
                "files": file_list,
            },
        }
    except Exception as error:
        return {
            "code": constants.HTTP_ERROR,
            "payload": {
                "action": ACTION_FILELIST,
                "status": STATUS_ERROR,
                "error": str(error),
            },
        }


def get_file_count():
    try:
        file_count = len(list(constants.TIMELAPSE_DEST_DIR.glob("*.jpg")))

        return {
            "code": constants.HTTP_OK,
            "payload": {
                "action": ACTION_FILECOUNT,
                "status": STATUS_FINISHED,
                "count": file_count,
            },
        }
    except Exception as error:
        return {
            "code": constants.HTTP_ERROR,
            "payload": {
                "action": ACTION_FILECOUNT,
                "status": STATUS_ERROR,
                "error": str(error),
            },
        }
