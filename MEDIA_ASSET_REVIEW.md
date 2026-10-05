# External visual-source review

## Scope

This review evaluates OpenDSA as a reference only. No OpenDSA asset, code,
text, iframe, script, account, analytics integration, or runtime dependency is
approved or included in DSA Study.

## Review — 2026-09-11

| Dimension | Finding | Decision |
| --- | --- | --- |
| License | OpenDSA publishes an MIT license. | License is not an authorization to copy material into this project; preserve link-only review. |
| Accessibility | Its interactive assets require asset-by-asset review. | Do not infer keyboard, no-motion, or semantic-equivalent compliance from source availability. |
| External runtime | The project uses a separate interactive platform and services. | No embed or remote script; DSA Study stays dependency-free and local-first. |
| Privacy and retention | A remote exercise environment can have its own account and tracking behavior. | Do not send learner input, identifiers, completion, or analytics to it. |

## Outcome

OpenDSA remains a link-only comparison source. DSA Study implements original
semantic HTML/text media primitives instead. A future proposal to copy or embed
any external visual needs a separate asset-level license, accessibility,
runtime, privacy, retention, and Registry decision.

## Sources

- [OpenDSA license](https://opendsa.org/home/license)
- [OpenDSA project source](https://github.com/OpenDSA/OpenDSA)
