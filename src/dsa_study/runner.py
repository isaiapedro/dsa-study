"""Local, LeetCode-shaped execution harness used by the browser viewer.

This is deliberately a study aid, not a security sandbox and not a submission
client.  It creates a new ``Solution`` instance for every supplied case and
times the aggregate construction-and-call loop, which is the closest local
model available without LeetCode's private judge and hidden test suite.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import traceback
from typing import Any


DEFAULT_TIMEOUT_SECONDS = 3.0
MAX_CASES = 100


class ListNode:
    def __init__(self, val: Any = 0, next: "ListNode | None" = None) -> None:
        self.val, self.next = val, next


class TreeNode:
    def __init__(self, val: Any = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None) -> None:
        self.val, self.left, self.right = val, left, right


class GraphNode:
    """A graph node for original local exercises.

    Inputs use either a LeetCode-shaped adjacency list (one-based node values
    and references, rooted at node one), or the explicit object format emitted
    by ``_to_json``. Output is always the explicit breadth-first canonical
    form, keeping arbitrary node values and cyclic graphs unambiguous JSON.
    """

    def __init__(self, val: Any = 0, neighbors: "list[GraphNode] | None" = None) -> None:
        self.val, self.neighbors = val, list(neighbors or [])


def judge_submission(request: dict[str, Any], *, timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS) -> dict[str, Any]:
    """Run one local request in a separate Python process with a wall timeout."""
    _validate_request(request)
    command = [sys.executable, "-I", str(Path(__file__).resolve()), "--child"]
    environment = {"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8"}
    try:
        completed = subprocess.run(
            command, input=json.dumps(request), text=True, capture_output=True,
            timeout=timeout_seconds, env=environment, cwd=tempfile.gettempdir(), check=False,
        )
    except subprocess.TimeoutExpired:
        return {"status": "time_limit_exceeded", "message": f"Local wall-time limit exceeded ({timeout_seconds:g}s)."}
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"status": "runtime_error", "message": "The local runner did not return a valid result."}
    if completed.returncode and result.get("status") == "accepted":
        return {"status": "runtime_error", "message": "The local runner exited unexpectedly."}
    return result


def _validate_request(request: dict[str, Any]) -> None:
    if not isinstance(request.get("code"), str) or not request["code"].strip():
        raise ValueError("Python solution code is required.")
    if not isinstance(request.get("method"), str) or not request["method"].isidentifier():
        raise ValueError("A valid Solution method is required.")
    cases = request.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Provide at least one test case.")
    if len(cases) > MAX_CASES:
        raise ValueError(f"At most {MAX_CASES} cases may be run at once.")
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("args"), list) or "expected" not in case:
            raise ValueError("Each case must have JSON args and an expected output.")


def _from_json(value: Any, type_name: str) -> Any:
    if "ListNode" in type_name:
        sentinel = ListNode()
        tail = sentinel
        for item in value or []:
            tail.next = ListNode(item)
            tail = tail.next
        return sentinel.next
    if "TreeNode" in type_name:
        if not value:
            return None
        nodes = [TreeNode(item) if item is not None else None for item in value]
        children = iter(nodes[1:])
        for node in nodes:
            if node is not None:
                node.left = next(children, None)
                node.right = next(children, None)
        return nodes[0]
    if "GraphNode" in type_name:
        return _graph_from_json(value)
    return value


def _graph_from_json(value: Any) -> GraphNode | None:
    """Build a graph from compact adjacency-list or explicit JSON fixtures."""
    if value is None:
        return None
    if isinstance(value, list):
        nodes = [GraphNode(index + 1) for index in range(len(value))]
        for index, neighbors in enumerate(value):
            if not isinstance(neighbors, list):
                raise ValueError("GraphNode adjacency rows must be lists.")
            for neighbor in neighbors:
                if not isinstance(neighbor, int) or isinstance(neighbor, bool) or not 1 <= neighbor <= len(nodes):
                    raise ValueError("GraphNode adjacency references must be one-based node numbers.")
                nodes[index].neighbors.append(nodes[neighbor - 1])
        return nodes[0] if nodes else None
    if not isinstance(value, dict) or set(value) - {"root", "nodes"} or not isinstance(value.get("nodes"), list):
        raise ValueError("GraphNode must be an adjacency list or an object with root and nodes.")
    records = value["nodes"]
    by_id: dict[str, GraphNode] = {}
    neighbor_ids: dict[str, list[Any]] = {}
    for record in records:
        if not isinstance(record, dict) or set(record) - {"id", "val", "neighbors"} or "id" not in record or "neighbors" not in record:
            raise ValueError("Each GraphNode record needs only id, val, and neighbors.")
        identifier = _graph_id(record["id"])
        if identifier in by_id or not isinstance(record["neighbors"], list):
            raise ValueError("GraphNode ids must be unique and neighbors must be lists.")
        by_id[identifier] = GraphNode(record.get("val"))
        neighbor_ids[identifier] = record["neighbors"]
    if not records:
        if value.get("root") is not None:
            raise ValueError("An empty GraphNode graph must have a null root.")
        return None
    root_id = _graph_id(value.get("root"))
    if root_id not in by_id:
        raise ValueError("GraphNode root must reference a supplied node.")
    for identifier, references in neighbor_ids.items():
        for reference in references:
            neighbor_id = _graph_id(reference)
            if neighbor_id not in by_id:
                raise ValueError("GraphNode neighbors must reference supplied nodes.")
            by_id[identifier].neighbors.append(by_id[neighbor_id])
    return by_id[root_id]


def _graph_id(value: Any) -> str:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError("GraphNode ids must be strings or integers.")
    return f"{type(value).__name__}:{value}"


def _to_json(value: Any) -> Any:
    if isinstance(value, ListNode):
        result = []
        while value is not None:
            result.append(value.val)
            value = value.next
        return result
    if isinstance(value, TreeNode):
        result, queue = [], [value]
        while queue:
            node = queue.pop(0)
            result.append(None if node is None else node.val)
            if node is not None:
                queue.extend([node.left, node.right])
        while result and result[-1] is None:
            result.pop()
        return result
    if isinstance(value, GraphNode):
        nodes, ids, queue = [], {id(value): 1}, [value]
        while queue:
            node = queue.pop(0)
            node_id = ids[id(node)]
            neighbor_ids = []
            for neighbor in node.neighbors:
                if not isinstance(neighbor, GraphNode):
                    raise TypeError("GraphNode neighbors must be GraphNode instances.")
                if id(neighbor) not in ids:
                    ids[id(neighbor)] = len(ids) + 1
                    queue.append(neighbor)
                neighbor_ids.append(ids[id(neighbor)])
            nodes.append({"id": node_id, "val": _to_json(node.val), "neighbors": neighbor_ids})
        return {"root": 1, "nodes": nodes}
    if isinstance(value, tuple):
        return [_to_json(item) for item in value]
    if isinstance(value, list):
        return [_to_json(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _to_json(item) for key, item in value.items()}
    return value


def _child(request: dict[str, Any]) -> dict[str, Any]:
    _validate_request(request)
    namespace: dict[str, Any] = {"ListNode": ListNode, "TreeNode": TreeNode, "GraphNode": GraphNode, "__name__": "solution"}
    captured = io.StringIO()
    try:
        with contextlib.redirect_stdout(captured):
            exec(compile(request["code"], "solution.py", "exec"), namespace)
        solution_type = namespace.get("Solution")
        if not isinstance(solution_type, type):
            return {"status": "compile_error", "message": "Define a class named Solution."}
        parameters = request.get("params") or []
        started = time.perf_counter_ns()
        results = []
        for index, case in enumerate(request["cases"]):
            # A fresh instance per case intentionally models the observed LC judge behaviour.
            method = getattr(solution_type(), request["method"], None)
            if not callable(method):
                return {"status": "compile_error", "message": f"Solution.{request['method']} is not callable."}
            args = [_from_json(value, str(parameters[position].get("type", "")) if position < len(parameters) else "") for position, value in enumerate(case["args"])]
            actual = _to_json(method(*args))
            passed = actual == case["expected"]
            results.append({"index": index + 1, "passed": passed, "actual": actual, "expected": case["expected"]})
            if not passed:
                elapsed = time.perf_counter_ns() - started
                return {"status": "wrong_answer", "runtime_ns": elapsed, "cases_passed": index, "cases_total": len(request["cases"]), "results": results}
        elapsed = time.perf_counter_ns() - started
        return {"status": "accepted", "runtime_ns": elapsed, "cases_passed": len(results), "cases_total": len(results), "results": results}
    except Exception:
        return {"status": "runtime_error", "message": traceback.format_exc(limit=3), "stdout": captured.getvalue()[:2_000]}


def _main() -> None:
    try:
        request = json.loads(sys.stdin.read())
        result = _child(request)
    except Exception as error:
        result = {"status": "invalid_request", "message": str(error)}
    print(json.dumps(result, ensure_ascii=False, default=str))


if __name__ == "__main__":
    _main()
