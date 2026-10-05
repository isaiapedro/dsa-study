# Local runner validation

## Purpose and boundary

This record contains project-authored methodology, aggregate results, and
link-only public references. It does not retain fetched statements, external
solution text, submitted code, full test arguments, expected values, or
browser output.

## Catalog integrity check — 2026-09-11

The local audit found 4,042 records: 3,260 readable public details, 2,998
runner-compatible records, 782 paid or unavailable records, 94 readable
records without an extracted example, and 161 without a Python starter.

The example extractor had allowed a subsequent numbered-example heading into a
prior output field. A deterministic parser test was added, then
`dsa-study repair-examples` re-extracted examples only from existing ignored
local statement markup. It repaired 427 records; a post-repair local scan
found no remaining output field with a subsequent example heading. No provider
request was made and no catalog payload was added to tracked files.

## Representative runner check — 2026-09-11

Original one-pass dictionary and nested-loop implementations were checked
against the three local examples for catalog record `1`; the one-pass approach
passed all three. A separate original 7,000-element worst-case-style input was
sampled five times through the same `judge_submission()` path used by
`POST /api/run`.

| Approach | Median aggregate call time | Complexity claim |
| --- | ---: | --- |
| One-pass dictionary lookup | 1.962 ms | Expected O(n) time, O(n) space |
| Nested loops | 1,599.286 ms | O(n²) time, O(1) auxiliary space |

The local median ratio was about 815×. This is a local relative comparison,
not a LeetCode runtime, time-limit, memory, or percentile claim: hidden cases,
executor, limits, and runtime distribution are unavailable to this workspace.

## Public comparison references

- [LeetCode Discuss: one-pass hash-map explanation](https://leetcode.com/discuss/post/7042575/struggling-to-explain-why-hashmap-works-0mrbw/)
- [LeetCode Discuss: nested-loop approach](https://leetcode.com/discuss/post/4506136/Two-Sum-oror-Java-or-Easy-Solution-or-Beginner/)
- [LeetCode Discuss: repeated-runtime variance](https://leetcode.com/discuss/post/566030/large-variance-in-runtime-performance-for-repeated-tests-of-same-answer/)

These sources were consulted for comparison only. Their code and prose are not
copied, adapted, or used as catalog fixtures.

## Manual public GraphQL provider-compatibility procedure

This is a manual, on-demand operational check, not part of the deterministic
test suite. Run it only against the public provider when its response shape is
in doubt or immediately before an operational sync that depends on a changed
shape. Do not run it with a logged-in browser, cookies, authorization headers,
or Personal state.

1. Start from a clean local working tree for ignored catalog data, or use an
   isolated temporary catalog location. Confirm that any existing fetched
   catalog remains ignored by Git.
2. Run the documented public catalog synchronization command once. Do not
   enable verbose HTTP/body logging and do not copy terminal payload output
   into any tracked record.
3. Run `dsa-study audit` against the resulting local ignored catalog.
4. Compare only the expected structural contract: the sync completed without
   a schema/key error; the top-level catalog collection is present; each
   catalog record has its expected identifier/slug/topic metadata fields when
   applicable; and the aggregate audit counts are internally consistent.
   Treat absent paid-only details as an expected availability state, not a
   compatibility failure.
5. If the check succeeds, record the date, provider/query class, success,
   field-presence result, and aggregate counts below or in `AUDIT.md`. If it
   fails, record only the error class and missing/changed field names, then
   stop automated sync use until the client and deterministic fixtures are
   reviewed.
6. Do not commit the downloaded catalog, HTML, checkpoints, command output,
   request/response bodies, titles, slugs, statements, headers, cookies, or
   Personal data. Remove or retain ignored local data according to the local
   storage policy only.

### Compatibility record template

| Date | Provider/query class | Shape result | Aggregate counts | Error class / follow-up |
| --- | --- | --- | --- | --- |
| _YYYY-MM-DD_ | _public catalog metadata; unauthenticated_ | _pass/fail; collection and expected fields present/absent_ | _catalog/readable/runner-compatible/unavailable totals only_ | _none or structural error class and owner action_ |

No completed public provider check is asserted by this template. The catalog
counts above are historical local-audit results, not a claim about the current
provider response.

## Verification status

The extractor-specific suite passed 3 tests. The runner accepted the
representative three-case check, and Registry validation reported 41 valid
components. The historical `question_provenance` block-data failure is resolved.
The six additional authored blocks now have their required fixed
catalog-practice contracts, and the fresh build passes. `tests/test_runner.py`
also covers original list, tree, compact graph, and explicit cyclic-graph
fixtures; graph output is canonicalized before comparison. Current project-wide
verification evidence is maintained in `AUDIT.md`.
