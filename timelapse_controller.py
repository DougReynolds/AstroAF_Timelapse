# timelapse_controller.py

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen
from pathlib import Path
import json
from datetime import datetime

import services.arming_service as arming_service
import services.capture_service as capture_service
import services.storage_service as storage_service
import services.render_service as render_service
import services.cleanup_service as cleanup_service

import common.constants as constants

HOST = "0.0.0.0"
PORT = 5000


class Handler(BaseHTTPRequestHandler):
    def log_event(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}", flush=True)

    def send_json(self, result):
        body = json.dumps(result["payload"]).encode()
        self.send_response(result["code"])
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def handle_timelapse_arm(self):
        self.log_event("[HTTP] /armtimelapse")
        self.send_json(arming_service.timelapse_arm())

    def handle_newframe(self):
        self.log_event("[HTTP] /newframe")
        self.send_json(capture_service.capture_new_frame())

    def handle_filelist(self):
        self.log_event("[HTTP] /filelist")
        self.send_json(storage_service.get_file_list())

    def handle_filecount(self):
        self.log_event("[HTTP] /filecount")
        self.send_json(storage_service.get_file_count())

    def handle_render(self):
        self.log_event("[HTTP] /render")
        self.send_json(render_service.render_frames())

    def handle_cleanup(self):
        self.log_event("[HTTP] /cleanup")
        self.send_json(cleanup_service.cleanup_job())

    def handle_not_found(self):
        self.log_event(f"[HTTP] 404 {self.path}")
        self.send_json(
            {
                "code": constants.HTTP_NOT_FOUND,
                "payload": {
                    "ok": constants.OK_FALSE,
                    "error": constants.ERROR_NOT_FOUND,
                },
            }
        )

    def do_GET(self):
        if self.path == "/armtimelapse":
            self.handle_timelapse_arm()
            return
        if self.path == "/newframe":
            self.handle_newframe()
            return
        if self.path == "/filelist":
            self.handle_filelist()
            return
        if self.path == "/filecount":
            self.handle_filecount()
            return
        if self.path == "/render":
            self.handle_render()
            return
        if self.path == "/cleanup":
            self.handle_cleanup()
            return
        self.handle_not_found()


HTTPServer((HOST, PORT), Handler).serve_forever()
