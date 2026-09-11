# DSA Study Registry update procedure

## Update registry of this folder

Interpret this request as a complete situational-governance update, not merely
a manifest edit. Inspect the changed work and update every applicable item:

1. `manifest.yaml`: identity, owner, lifecycle, dependencies, interfaces, and
   data/boundary declarations.
2. `STATE.md`: implemented capabilities, current stage, and blockers.
3. `TASKS.md` and `ROADMAP.md`: work status, next actions, and milestones.
4. `DECISIONS.md`: durable architectural, source, storage, privacy, or
   repository decisions.
5. `TRACEABILITY.md` and `LOGGING.md`: provenance, authoritative sources,
   operational logging, and exclusions.
6. `registry/repositories.yaml`: repository identity, source/secret/generated
   paths, and commit boundary; replace an unmanaged scope when applicable.
7. `AUDIT.md`: verification scope and results.
8. `TESTING.md`: execute the required checks, then rebuild Registry state.

Do not copy fetched problems, personal solutions, browser state, credentials,
or generated payloads into Registry records.

## Completion gate

The update is complete only when the applicable records above are consistent,
the project tests pass, `registry validate` passes, the Registry snapshot is
rebuilt after a structural change, and `AUDIT.md` names the verification result.
