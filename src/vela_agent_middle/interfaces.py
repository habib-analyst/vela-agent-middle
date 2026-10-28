"""Interface variants over the same synthetic backend.

- VulnerableInterface: exposes the raw search unchanged. Any field
  (including visibility/owner) is searchable, and no visibility filter
  is applied to results. This is the "reference / permissive"
  interface design.
- ControlInterface: restricted design. Only allowlisted fields
  ("topic", "title") are searchable, and results are filtered to notes
  the caller may see (public, or owned by the caller).
- MitigatedInterface: the vulnerable interface plus a defensive
  wrapper (the G3 mitigation). Two checks, applied in order:
  (1) interface-integrity check: reject queries on non-allowlisted
  fields; (2) agent-side verification: re-check every returned
  record's visibility/ownership before delivery and drop any record
  the caller may not see. The wrapper never invents records and
  never widens access; it can only narrow results.
"""

from __future__ import annotations

from .backend import RawBackend

ALLOWLISTED_FIELDS = ("topic", "title")


def _may_see(note, caller: str) -> bool:
    return note.visibility == "public" or note.owner == caller


class VulnerableInterface:
    name = "vulnerable"

    def __init__(self, backend: RawBackend):
        self._backend = backend

    def search(self, field: str, value: str) -> list:
        return self._backend.search(field, value)


class ControlInterface:
    name = "control"

    def __init__(self, backend: RawBackend, caller: str):
        self._backend = backend
        self._caller = caller

    def search(self, field: str, value: str) -> list:
        if field not in ALLOWLISTED_FIELDS:
            return []
        return [n for n in self._backend.search(field, value) if _may_see(n, self._caller)]


class MitigatedInterface:
    """Defensive wrapper around the vulnerable interface (G3)."""

    name = "mitigated"

    def __init__(self, vulnerable: VulnerableInterface, caller: str):
        self._vulnerable = vulnerable
        self._caller = caller

    def search(self, field: str, value: str) -> list:
        # (1) Interface-integrity check: non-allowlisted field -> refuse.
        if field not in ALLOWLISTED_FIELDS:
            return []
        raw = self._vulnerable.search(field, value)
        # (2) Verification: drop every record the caller may not see.
        return [n for n in raw if _may_see(n, self._caller)]
