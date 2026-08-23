# Pure AI-Agent Benchmark Contract

Use this contract when two or more Agent-produced manuscript candidates must be
compared without a human judge in the execution loop.

## Execution boundary

1. `run_agentic_candidates.py` runs candidate writers in isolated calls. No candidate
   sees another output; each output records provider/model/request and content hashes.
2. `build_agentic_review_packet.py` creates a public blind packet and a separate private
   mapping. Never send the mapping or deterministic hard-audit results to judge Agents.
3. At least three declared judge profiles score every candidate against the same rubric
   in isolated calls. Each review binds packet, prompt, raw response, provider, model,
   request ID, attempt, and finish reason.
4. `adjudicate_agentic_benchmark.py` validates all hashes and schemas. Deterministic hard
   gates take precedence over votes. Invalid, duplicate, incomplete, or stale reviews
   fail closed.
5. A panel using only one provider/model pair is labeled
   `single-model-low-confidence`. Two or more pairs are labeled
   `cross-model-evaluated`; this is not a truth or journal-acceptance claim.
6. High-risk meaning changes always terminate as `high-risk-no-ai-authorization`, even
   after unanimous Agent consensus. A pure-Agent run may stop safely; it may not silently
   lower the risk classification.

## Adversarial regression boundary

`generate_adversarial_mutations.py` applies bounded deterministic operators to repository
fixtures. A mutation enters the suite only when an independent oracle rejects it. Current
operators cover number and citation relocation, direction and significance flips,
association-to-causal upgrades, and broken LaTeX references, packages, and environments.
Controls are copied unchanged. Generated reports contain no timestamps so identical inputs
produce identical manifests.

Default CI runs only packet construction, dry-run prompt validation, fixture adjudication,
and adversarial generation. Live model calls require an explicitly configured compatible
provider and are never part of the offline release gate.
