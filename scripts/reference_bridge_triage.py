#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict
import json

from rdss.triage import rdss_reference_bridge_triage


def main() -> int:
    report = rdss_reference_bridge_triage()
    payload = {
        "schema": "rdss.bridge-gap-triage/v1",
        "summary": asdict(report.summary()),
        "entries": [
            {
                "source_family": entry.source_family,
                "target_family": entry.target_family,
                "status": entry.status.value,
                "reason": entry.reason,
                "claim_ids": entry.claim_ids,
            }
            for entry in report.entries
        ],
    }
    print(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
