#!/usr/bin/env python3
"""Explicit editorial re-enrolment of public bytes; never semantic proof."""

import json

import check

if __name__ == "__main__":
    data = {
        "schema_version": 1,
        "scope": "public_editorial_inventory_only",
        "documents": check.inventory(check.ROOT),
    }
    (check.ROOT / "worlds/coverage.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    print(
        "Updated public byte/heading inventory. Review mapping and diff; assurance did not increase."
    )
