# v3.1 Capability And Provenance

Report capability separately from intent:

* Verified: a deterministic check or adapter ran and returned evidence.
* Documented: the interface and downgrade path exist, but this run did not
  execute it.
* Conceptual: required infrastructure, credentials, data, or connector is absent.

Every optional provider, parser, model adapter, or imported skill must declare its
source URL, immutable commit/version, license, capabilities, credential needs,
status, and last-tested date. Do not vendor third-party skill text or code into
the writing core. Network, shell, file-write, and model execution are separate
capabilities.
