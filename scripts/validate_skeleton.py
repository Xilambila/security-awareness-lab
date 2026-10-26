"""Validate the static scaffold and synthetic fixtures without network access."""

import csv
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "README.md", "SECURITY.md", ".gitignore", "config/lab.example.json",
    "docs/architecture.md", "docs/campaign-runbook.md", "docs/privacy-and-metrics.md",
    "cloudflared/README.md", "nginx/README.md", "landing/index.html",
    "templates/email.example.html", "data/participants.example.csv",
    "examples/aggregate-metrics.json", "scripts/validate_skeleton.py",
}


class StaticHTMLCheck(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag.lower() in {"form", "input", "script", "iframe", "img", "object", "embed"}:
            raise ValueError("Active or collecting content.")
        for name, _ in attrs:
            if name.lower().startswith("on") or name.lower() in {"src", "href", "action"}:
                raise ValueError("External or active reference.")

    handle_startendtag = handle_starttag


def validate():
    files = {
        p.relative_to(ROOT).as_posix(): p
        for p in ROOT.rglob("*")
        if p.is_file() and not any(
            part in {".git", "__pycache__", ".venv"}
            for part in p.relative_to(ROOT).parts
        )
    }
    if set(files) != EXPECTED:
        raise ValueError("Unexpected or missing scaffold file; review the allowlist.")

    config = json.loads(files["config/lab.example.json"].read_text(encoding="utf-8"))
    if config.get("mode") != "documentation-only" or config.get("sample_data_only") is not True:
        raise ValueError("Scaffold must remain documentation-only and synthetic.")
    for key in (
        "outbound_delivery_enabled", "visitor_tracking_enabled",
        "credential_collection_enabled", "public_exposure_enabled",
    ):
        if config.get(key) is not False:
            raise ValueError("An operational capability was enabled.")

    with files["data/participants.example.csv"].open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    expected = {
        "participant_id": "LAB-P001", "display_name": "Synthetic Participant",
        "email": "participant@example.invalid", "cohort": "synthetic-lab",
    }
    if rows != [expected]:
        raise ValueError("Participant fixture must be the single synthetic example.")

    metrics = json.loads(files["examples/aggregate-metrics.json"].read_text(encoding="utf-8"))
    if metrics.get("data_classification") != "synthetic-example":
        raise ValueError("Metrics must be labeled synthetic.")
    if metrics["reporting_rate_percent"] != 100 * metrics["reported"] / metrics["delivered"]:
        raise ValueError("Example arithmetic mismatch.")

    for relative, path in files.items():
        content = path.read_text(encoding="utf-8")
        if re.search(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|(?:AKIA|ASIA)[A-Z0-9]{16})\b", content):
            raise ValueError("Possible credential pattern.")
        if relative.endswith(".html"):
            StaticHTMLCheck().feed(content)
    return len(files)


if __name__ == "__main__":
    try:
        total = validate()
    except (ValueError, KeyError, ZeroDivisionError, OSError, csv.Error) as error:
        print(f"Validation failed: {type(error).__name__}. Review files privately.", file=sys.stderr)
        sys.exit(1)
    print(f"Validated {total} files: static content and synthetic fixtures passed.")
    print("Targeted checks only; manual confidentiality review remains necessary.")
