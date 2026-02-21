#!/usr/bin/env python3
import argparse
import csv
import json
import re
from pathlib import Path

FIELDNAMES = [
    "county",
    "office",
    "district",
    "candidate",
    "incumbent",
    "party",
    "votes",
    "pct",
]


def normalize_party(party: str) -> str:
    party = (party or "").strip().upper()
    if party == "W":
        return "WI"
    return party


def clean_candidate_name(name: str) -> tuple[str, str]:
    name = (name or "").strip()
    incumbent = "TRUE" if "(I)" in name else "FALSE"
    cleaned = re.sub(r"\s*\(I\)\s*", "", name).strip()
    return cleaned, incumbent


def normalize_office_and_district(office_raw: str) -> tuple[str, str]:
    office = re.sub(r"\s+", " ", (office_raw or "").strip())
    district = ""

    patterns = [
        r"^(.*?),\s*DISTRICT\s+([0-9A-Z-]+)$",
        r"^(.*?)\s+DISTRICT\s+([0-9A-Z-]+)$",
    ]

    for pattern in patterns:
        match = re.match(pattern, office, flags=re.IGNORECASE)
        if match:
            office = match.group(1).strip().rstrip(",")
            district = match.group(2).strip()
            break

    return office, district


def convert(input_path: Path, output_path: Path, include_totals: bool) -> int:
    with input_path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    rows = []
    for county_obj in payload.values():
        county_name = (county_obj.get("N") or "").strip().upper()
        races = county_obj.get("Races", {})

        for race_obj in races.values():
            office, district = normalize_office_and_district(race_obj.get("ON", ""))
            candidates = race_obj.get("C", {})

            for candidate_obj in candidates.values():
                candidate_name, incumbent = clean_candidate_name(candidate_obj.get("N", ""))
                votes = int(candidate_obj.get("V", 0) or 0)
                pct = candidate_obj.get("PE", "")
                if pct is None:
                    pct = ""
                rows.append(
                    {
                        "county": county_name,
                        "office": office,
                        "district": district,
                        "candidate": candidate_name,
                        "incumbent": incumbent,
                        "party": normalize_party(candidate_obj.get("P", "")),
                        "votes": votes,
                        "pct": pct,
                    }
                )

            if include_totals:
                rows.append(
                    {
                        "county": county_name,
                        "office": office,
                        "district": district,
                        "candidate": "Total",
                        "incumbent": "",
                        "party": "",
                        "votes": int(race_obj.get("T", 0) or 0),
                        "pct": "",
                    }
                )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Clarity County.json to OpenElections-style county CSV.")
    parser.add_argument("--input", required=True, help="Path to input County.json")
    parser.add_argument("--output", required=True, help="Output CSV path")
    parser.add_argument("--no-totals", action="store_true", help="Exclude 'Total' rows")
    args = parser.parse_args()

    row_count = convert(Path(args.input), Path(args.output), include_totals=not args.no_totals)
    print(f"Wrote {row_count} rows to {args.output}")


if __name__ == "__main__":
    main()
