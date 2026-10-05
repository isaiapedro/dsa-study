# Local interfaces

This project has one network interface. It is deliberately local-only and is
available only after `dsa-study build` followed by `dsa-study serve`. The
server binds to `127.0.0.1`, never to a LAN or public interface.

## CLI

| Command | Input | Output / effect | Boundary |
| --- | --- | --- | --- |
| `dsa-study sync [--resume]` | Public LeetCode GraphQL responses | Ignored `data/catalog.json` and sync checkpoint | External content; never commit it. |
| `dsa-study build` | Tracked course modules and interactive examples; optional ignored catalog | Ignored `site/` contents, course pages, and problem pages | Works without a catalog; never includes private progress. |
| `dsa-study audit` | Ignored local catalog | Coverage and local-runner compatibility counts | Prints aggregates only; never copies catalog text. |
| `dsa-study repair-examples` | Existing ignored statement markup | Re-extracted ignored example fields | Local-only repair; makes no provider request. |
| `dsa-study serve [--port N]` | Existing generated `site/` | Loopback static viewer and `POST /api/run` | Runs code only on the local machine. |
| `dsa-study new-solution ID` | Catalog problem ID | Ignored local solution scaffold | Personal work; never commit it. |
| `dsa-study progress …` / `review` | Local study event | Ignored `.dsa-study/progress.json` / derived queue | Personal state; never render or log it. |

## `POST /api/run`

**Address:** `http://127.0.0.1:8765/api/run` by default. The port may be
changed with `dsa-study serve --port N`.

This endpoint invokes a fresh Python `Solution` instance for each supplied
case. It is a small local study harness, not a security sandbox and not a
LeetCode submission client. Use it only with code you trust on your own
machine. It has a three-second wall-time limit per request and accepts at most
100 cases.

### Request

```json
{
  "code": "class Solution:\n    def add(self, left, right):\n        return left + right\n",
  "method": "add",
  "params": [{"type": "int"}, {"type": "int"}],
  "cases": [{"args": [2, 3], "expected": 5}]
}
```

- `code` is required Python source defining `class Solution`.
- `method` is a required valid Python identifier found on `Solution`.
- `cases` is a required, non-empty list of `{ "args": [...], "expected": … }`.
- `params` is optional metadata. Use `ListNode` or `TreeNode` in `type` when
  an array-shaped input should be converted to that helper type.

### Responses

Successful requests return HTTP `200` and one of these `status` values:

| Status | Meaning |
| --- | --- |
| `accepted` | Every supplied case matched. |
| `wrong_answer` | A case did not match; `results` contains actual and expected values. |
| `compile_error` | `Solution` or its named method could not be used. |
| `runtime_error` | The submitted code raised an error. |
| `time_limit_exceeded` | The local wall-time limit elapsed. |

Malformed bodies return HTTP `400` with `invalid_request`. There are no
authentication, account, persistence, analytics, or remote-submission
endpoints. The server intentionally suppresses API request logs because code
and test data may be Personal local material.
