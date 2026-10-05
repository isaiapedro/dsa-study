from __future__ import annotations

import json
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from dsa_study.server import _ViewerHandler


def _runner_request() -> bytes:
    return json.dumps({
        "code": "class Solution:\n    def add(self, left, right):\n        return left + right\n",
        "method": "add",
        "cases": [{"args": [2, 3], "expected": 5}],
    }).encode("utf-8")


def test_loopback_run_endpoint_accepts_valid_and_rejects_invalid_requests(tmp_path: Path):
    (tmp_path / "index.html").write_text("viewer", encoding="utf-8")
    handler = lambda *args, **kwargs: _ViewerHandler(*args, directory=str(tmp_path), **kwargs)
    try:
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    except PermissionError:
        pytest.skip("this sandbox does not permit loopback socket binding")
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        address = f"http://127.0.0.1:{server.server_port}/api/run"
        valid = Request(address, data=_runner_request(), headers={"Content-Type": "application/json"}, method="POST")
        with urlopen(valid, timeout=3) as response:
            assert response.status == 200
            assert json.loads(response.read())["status"] == "accepted"

        invalid = Request(address, data=b"{}", headers={"Content-Type": "application/json"}, method="POST")
        try:
            urlopen(invalid, timeout=3)
        except HTTPError as error:
            assert error.code == 400
            assert json.loads(error.read())["status"] == "invalid_request"
        else:
            raise AssertionError("expected malformed API request to be rejected")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
