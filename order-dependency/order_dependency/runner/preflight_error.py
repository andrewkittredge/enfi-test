"""Failure of the probe request that precedes a run."""


class PreflightError(RuntimeError):
    """The very first request failed, so the whole run would fail (bad key, no credit, bad model...)."""
