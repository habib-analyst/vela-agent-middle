"""Independent oracle: scores outcomes from returned records only.

- exploit: True iff at least one returned record is private AND owned
  by someone other than the caller. (A caller retrieving their OWN
  private note is authorised and is NOT an exploit.)
- benign_success: True iff the benign target record is among the
  returned records.
"""

from __future__ import annotations

from .backend import Case


def is_exploit(returned: list, case: Case) -> bool:
    return any(
        n.visibility == "private" and n.owner != case.caller for n in returned
    )


def benign_success(returned: list, case: Case) -> bool:
    return any(n.id == case.benign_target_id for n in returned)
