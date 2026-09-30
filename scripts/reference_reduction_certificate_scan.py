#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict
import json

from rdss.certificate_scan import (
    scan_reference_reduction_certificates,
)


def main() -> int:
    scan = scan_reference_reduction_certificates()

    payload = {
        "schema": "rdss.reduction-certificate-scan/v1",
        "summary": asdict(scan.summary),
        "items": [
            asdict(item)
            for item in scan.items
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

    if scan.summary.verified != scan.summary.records:
        return 31
    if scan.summary.global_canonical_true != 0:
        return 32
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
