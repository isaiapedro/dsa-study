# DSA Study state

## Current status

The project is active, at prototype stage, and implements a local public
catalog synchronizer, topic registry, static site renderer, and Python solution
scaffolder. Its backlog remains focused on curated CS notes, local progress,
and future spaced-repetition support.

## Repository and Registry boundary

Implementation, tests, and local configuration belong to the dedicated
`dsa_study` repository. Fetched catalog data, generated site output,
checkpoints, browser state, and personal solutions are local-only and excluded
from commits and Registry payloads. The Registry owns only the manifest,
repository-boundary declaration, and generated structural state.
