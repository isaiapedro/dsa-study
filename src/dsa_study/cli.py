from __future__ import annotations

import argparse
from pathlib import Path

from dsa_study.catalog import sync
from dsa_study.client import LeetCodeClient
from dsa_study.render import render_site
from dsa_study.scaffold import create_solution
from dsa_study.storage import catalog_path, project_root, read_json


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="dsa-study", description="Local DSA study catalog")
    commands = parser.add_subparsers(dest="command", required=True)
    sync_parser = commands.add_parser("sync", help="Fetch public catalog and readable details")
    sync_parser.add_argument("--resume", action="store_true", help="Reuse prior detail records and checkpoint")
    sync_parser.add_argument("--page-size", type=int, default=100)
    commands.add_parser("build", help="Render the local static study site")
    solution_parser = commands.add_parser("new-solution", help="Create a local Python solution skeleton")
    solution_parser.add_argument("problem_id")
    args = parser.parse_args(argv)
    root = project_root()
    if args.command == "sync":
        document = sync(root, LeetCodeClient(), resume=args.resume, page_size=args.page_size)
        print(f"Synced {len(document['problems'])} problems and {len(document['topics'])} topics.")
    elif args.command == "build":
        document = read_json(catalog_path(root), None)
        if not document:
            raise SystemExit("No local catalog found. Run `dsa-study sync` first.")
        destination = root / "site"
        render_site(document, destination)
        print(f"Rendered {destination / 'index.html'}")
    else:
        target = create_solution(root, args.problem_id)
        print(f"Created {target}")
