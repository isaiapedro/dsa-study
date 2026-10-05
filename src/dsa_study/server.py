"""Loopback-only web server for the generated catalog and local judge API."""

from __future__ import annotations

from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from typing import Any

from dsa_study.runner import judge_submission


class _ViewerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, directory: str, **kwargs: Any) -> None:
        super().__init__(*args, directory=directory, **kwargs)

    def do_POST(self) -> None:  # noqa: N802 - standard library handler name
        if self.path != "/api/run":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 250_000:
                raise ValueError("Request must be between 1 and 250000 bytes.")
            payload = json.loads(self.rfile.read(length))
            result = judge_submission(payload)
            status = HTTPStatus.OK
        except (ValueError, json.JSONDecodeError) as error:
            result, status = {"status": "invalid_request", "message": str(error)}, HTTPStatus.BAD_REQUEST
        encoded = json.dumps(result, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: Any) -> None:
        # Browser code and results are Personal local state: never log either.
        if not args or str(args[0]).startswith("POST /api/run"):
            return
        super().log_message(format, *args)


def serve(site_directory: Path, *, port: int = 8765) -> None:
    if not site_directory.is_dir():
        raise RuntimeError("No generated site found. Run `dsa-study build` first.")
    handler = lambda *args, **kwargs: _ViewerHandler(*args, directory=str(site_directory), **kwargs)
    with ThreadingHTTPServer(("127.0.0.1", port), handler) as server:
        print(f"DSA Study viewer: http://127.0.0.1:{port}/")
        print("The local judge executes code on this machine; stop with Ctrl+C.")
        server.serve_forever()
