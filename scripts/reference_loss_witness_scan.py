#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict
import json

from rdss.loss_witness import (
    rdss_forgetful_loss_witnesses,
    summarize_forgetful_loss_witnesses,
)


def main() -> int:
    witnesses = rdss_forgetful_loss_witnesses()
    summary = summarize_forgetful_loss_witnesses()

    payload = {
        "schema": "rdss.loss-witness-scan/v1",
        "summary": asdict(summary),
        "items": [
            {
                "rule_name": witness.rule_name,
                "source_family": witness.source_family,
                "target_family": witness.target_family,
                "sources_distinct": witness.sources_distinct,
                "targets_equal": witness.targets_equal,
                "verified": witness.verified,
                "left_verified_invariants": (
                    witness.left_step.verified_invariants
                ),
                "right_verified_invariants": (
                    witness.right_step.verified_invariants
                ),
                "claim_ids": witness.claim_ids,
            }
            for witness in witnesses
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

    if summary.verified != summary.witnesses:
        return 41
    if summary.distinct_source_pairs != summary.witnesses:
        return 42
    if summary.collapsed_target_pairs != summary.witnesses:
        return 43
    if summary.irreducible_targets != summary.witnesses:
        return 44
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
