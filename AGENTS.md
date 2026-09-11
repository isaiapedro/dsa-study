# Mission

Maintain a small, local-first DSA study workspace.

## Rules

- Read `ROADMAP.md` and `TASKS.md` before structural changes.
- Never commit fetched LeetCode content, browser cookies, or personal solutions.
- Update `DECISIONS.md` when the external-source or storage policy changes.

## Registry update intent

Treat a user request to “update registry of this folder”, “update the DSA
registry”, or equivalent wording as a request to perform the complete local
governance update defined in [REGISTRY_UPDATE.md](REGISTRY_UPDATE.md). Do not
ask a follow-up merely to enumerate routine regulatory records; inspect the
change and update every applicable record. Ask only when a material product,
privacy, retention, or external-service decision is genuinely unspecified.

## Required records after a change

For every project change, determine and update as applicable: `manifest.yaml`
(identity, dependencies, interfaces, lifecycle); `STATE.md`; `TASKS.md`;
`ROADMAP.md`; `DECISIONS.md`; `AUDIT.md`; `TRACEABILITY.md`; and `LOGGING.md`.
Run the tests and Registry validation, record their result in `AUDIT.md`, and
rebuild the generated Registry snapshot after structural or boundary changes.
Never place fetched statements, cookies, personal solutions, or generated
catalog/site payloads in these records.
