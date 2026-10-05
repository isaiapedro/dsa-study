from dsa_study.runner import judge_submission


def test_runner_accepts_solution_and_reports_aggregate_time():
    report = judge_submission({
        "code": "class Solution:\n    def add(self, left, right):\n        return left + right\n",
        "method": "add", "params": [],
        "cases": [{"args": [2, 3], "expected": 5}, {"args": [-1, 1], "expected": 0}],
    })
    assert report["status"] == "accepted"
    assert report["cases_passed"] == 2
    assert report["runtime_ns"] >= 0


def test_runner_reports_first_wrong_answer():
    report = judge_submission({
        "code": "class Solution:\n    def identity(self, value):\n        return value\n",
        "method": "identity", "params": [],
        "cases": [{"args": [3], "expected": 4}],
    })
    assert report["status"] == "wrong_answer"
    assert report["cases_passed"] == 0
    assert report["results"][0]["actual"] == 3


def test_runner_converts_linked_list_arguments_and_results():
    report = judge_submission({
        "code": "class Solution:\n    def reverseList(self, head):\n        previous = None\n        while head:\n            head.next, previous, head = previous, head, head.next\n        return previous\n",
        "method": "reverseList", "params": [{"name": "head", "type": "ListNode"}],
        "cases": [{"args": [[1, 2, 3]], "expected": [3, 2, 1]}],
    })
    assert report["status"] == "accepted"


def test_runner_converts_tree_arguments_and_results():
    report = judge_submission({
        "code": "class Solution:\n    def invertTree(self, root):\n        if root:\n            root.left, root.right = root.right, root.left\n            self.invertTree(root.left)\n            self.invertTree(root.right)\n        return root\n",
        "method": "invertTree", "params": [{"name": "root", "type": "TreeNode"}],
        "cases": [{"args": [[4, 2, 7, 1, 3, 6, 9]], "expected": [4, 7, 2, 9, 6, 3, 1]}],
    })
    assert report["status"] == "accepted"


def test_runner_converts_adjacency_list_graph_and_canonicalizes_result():
    report = judge_submission({
        "code": "class Solution:\n    def cloneGraph(self, node):\n        if not node:\n            return None\n        copies = {node: GraphNode(node.val)}\n        stack = [node]\n        while stack:\n            current = stack.pop()\n            for neighbor in current.neighbors:\n                if neighbor not in copies:\n                    copies[neighbor] = GraphNode(neighbor.val)\n                    stack.append(neighbor)\n                copies[current].neighbors.append(copies[neighbor])\n        return copies[node]\n",
        "method": "cloneGraph", "params": [{"name": "node", "type": "GraphNode"}],
        "cases": [{
            "args": [[[2, 4], [1, 3], [2, 4], [1, 3]]],
            "expected": {"root": 1, "nodes": [
                {"id": 1, "val": 1, "neighbors": [2, 3]},
                {"id": 2, "val": 2, "neighbors": [1, 4]},
                {"id": 3, "val": 4, "neighbors": [1, 4]},
                {"id": 4, "val": 3, "neighbors": [2, 3]},
            ]},
        }],
    })
    assert report["status"] == "accepted"


def test_runner_accepts_explicit_graph_json_with_non_sequential_values():
    report = judge_submission({
        "code": "class Solution:\n    def identity(self, root):\n        return root\n",
        "method": "identity", "params": [{"name": "root", "type": "GraphNode"}],
        "cases": [{
            "args": [{"root": "start", "nodes": [
                {"id": "finish", "val": 99, "neighbors": ["start"]},
                {"id": "start", "val": 10, "neighbors": ["finish"]},
            ]}],
            "expected": {"root": 1, "nodes": [
                {"id": 1, "val": 10, "neighbors": [2]},
                {"id": 2, "val": 99, "neighbors": [1]},
            ]},
        }],
    })
    assert report["status"] == "accepted"


def test_runner_rejects_an_incomplete_request():
    try:
        judge_submission({"code": "class Solution: pass", "method": "run", "cases": []})
    except ValueError as error:
        assert "at least one test case" in str(error)
    else:
        raise AssertionError("expected invalid local-runner request to be rejected")
