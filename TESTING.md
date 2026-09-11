# DSA Study testing

## Required verification

Run the project test suite after a behavior, storage, or client change:

```bash
cd workspace/side_projects/dsa_study
.venv/bin/python -m pytest
```

Run Registry validation after a manifest, interface, repository, dependency, or
boundary change:

```bash
(cd ../../.. && python3 registry/implementation/cli.py validate)
(cd ../../.. && python3 registry/implementation/cli.py build)
```

Record the date, commands, and outcome in `AUDIT.md`. Mocked GraphQL fixtures
are required for deterministic tests; a manual public sync verifies provider
response compatibility without committing provider content.
