#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
import json

from rdss.corpus import scan_rdss_reference_corpus


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="return non-zero while signature coverage gaps remain",
    )
    args = parser.parse_args()

    result = scan_rdss_reference_corpus()
    graph_summary = result.equivalence_graph.summary()
    gap_report = result.bridge_gap_report

    payload = {
        "schema": "rdss.reference-corpus-scan/v1",
        "corpus_items": len(result.items),
        "supported_items": len(result.supported_items),
        "coverage_complete": result.coverage_complete,
        "coverage_gaps": [
            asdict(gap) for gap in result.coverage_gaps
        ],
        "novelty_counts": {
            kind.value: count
            for kind, count in result.novelty_counts.items()
        },
        "novelty": [
            {
                "name": item.name,
                "novelty": item.novelty.value,
                "family": item.family,
            }
            for item in result.novelty
        ],
        "catalog_summary": asdict(result.catalog_summary),
        "equivalence_graph_summary": asdict(graph_summary),
        "bridge_gap_summary": {
            "family_pairs": gap_report.family_pairs,
            "unresolved_pairs": gap_report.unresolved_pairs,
        },
        "bridge_gaps": [
            {
                "left_family": gap.left_family,
                "right_family": gap.right_family,
                "count": gap.count,
                "pairs": gap.pairs,
            }
            for gap in gap_report.gaps
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

    if args.require_complete and not result.coverage_complete:
        return 23
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
