# DSA Study logging contract

## Logging boundary

Log only operational metadata needed to diagnose a sync or build: command,
timestamp, public endpoint/query class, pagination/checkpoint position, record
counts, retry/error class, output path, and tool version. Do not log cookies,
authorization headers, fetched statement bodies, personal solution content, or
browser/session data.

Keep ephemeral command output local. Record durable verification summaries in
`AUDIT.md`; record source or storage-policy changes in `DECISIONS.md`.
