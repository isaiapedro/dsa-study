# Purpose

This project synchronizes public LeetCode study metadata into a local catalog,
renders an offline browser, provides Python-first solution scaffolds, and can
serve that generated browser with a loopback-only local execution harness.

The harness compares supplied JSON outputs exactly and reports aggregate local
call time across fresh `Solution` instances. It supports relative local
comparison only; it does not reproduce LeetCode hidden tests, infrastructure,
limits, memory accounting, or percentiles. Local examples can be repaired from
already ignored statement markup without a provider call.

Its authored learning layer is a separate, validated source path. It renders
45-minute concept blocks with controlled state traces, curriculum context, a
four-lens pre-code checkpoint, five review-required authored prompts, and
optional advanced bridge cards. Those controls are local browser interactions;
they do not create learner analytics, a recommendation system, or a mastery
claim.

It does not submit solutions, store credentials, bypass paid-only access, or
expose a network listener beyond `127.0.0.1`. The local runner is a study aid,
not a security sandbox.
