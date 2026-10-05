# DSA Study logging contract

## Logging boundary

Log only operational metadata needed to diagnose a sync or build: command,
timestamp, public endpoint/query class, pagination/checkpoint position, record
counts, retry/error class, output path, and tool version. Do not log cookies,
authorization headers, fetched statement bodies, personal solution content, or
browser/session data.

Keep ephemeral command output local. Record durable verification summaries in
`AUDIT.md`; record source or storage-policy changes in `DECISIONS.md`.

For the learning-block renderer, log only aggregate build diagnostics such as
block identifier, renderer version, generated output path, control-validation
result, and error class. Do not log prompt answers, free-text attempts,
completion, confidence, interaction sequences, or client identifiers. Browser
console diagnostics remain local and must be treated as potentially Personal
when they include learner input.

This includes the four pre-code checkpoint fields and any bridge-card response:
they are instructional interactions, not analytics or evidence of mastery.

For the loopback runner, do not log request bodies, submitted code, test
arguments, expected values, actual values, output, or stack traces. A durable
audit may report only that deterministic endpoint tests passed.

For catalog repair and runner comparison, record only repair counts, test
status, aggregate timing summaries, and algorithm class. Do not log catalog
examples, synthetic inputs, solution source, per-run timing sequences, or code.

For a manual public GraphQL provider-compatibility check, retain only the
provider/query class, timestamp, field-presence pass/fail, aggregate counts,
and structural error class. Never retain request or response bodies, titles,
slugs, statements, headers, cookies, checkpoint contents, terminal output, or
any account/browser state. The reproducible procedure and record template are
in `TESTING.md` and `RUNNER_VALIDATION.md`.

Interactive-learning evaluation records only source titles/URLs, renderer
capabilities, non-sensitive test outcomes, and backlog decisions in the
project documentation. Do not log motion-preference settings, responses,
interaction sequences, accessibility-assistive-technology use, transfer-task
answers, or evaluation outcomes; each can be Personal study data.

Research synthesis, curriculum-graph, and rubric records are authored design
documents. They may cite local Knowledge paths and public URLs, but may not
contain rubric attempts, feedback, outcomes, or review-queue events.
