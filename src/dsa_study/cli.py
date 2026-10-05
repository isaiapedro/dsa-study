from __future__ import annotations

import argparse
from pathlib import Path

from dsa_study.catalog import audit_catalog, repair_examples, sync
from dsa_study.client import LeetCodeClient
from dsa_study.progress import build_review_queue, record_progress
from dsa_study.render import render_site
from dsa_study.scaffold import create_solution
from dsa_study.server import serve
from dsa_study.storage import catalog_path, project_root, read_json, write_json


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="dsa-study", description="Local DSA study catalog")
    commands = parser.add_subparsers(dest="command", required=True)
    sync_parser = commands.add_parser("sync", help="Fetch public catalog and readable details")
    sync_parser.add_argument("--resume", action="store_true", help="Reuse prior detail records and checkpoint")
    sync_parser.add_argument("--page-size", type=int, default=100)
    commands.add_parser("build", help="Render the local static study site")
    commands.add_parser("audit", help="Report local catalog coverage and runner compatibility")
    commands.add_parser("repair-examples", help="Repair local extracted examples without contacting LeetCode")
    serve_parser = commands.add_parser("serve", help="Serve the local viewer and loopback-only code runner")
    serve_parser.add_argument("--port", type=int, default=8765)
    solution_parser = commands.add_parser("new-solution", help="Create a local Python solution skeleton")
    solution_parser.add_argument("problem_id")
    progress_parser = commands.add_parser("progress", help="Record private local learning progress")
    progress_parser.add_argument("problem_id")
    progress_parser.add_argument("--status", choices=["attempted", "solved", "reviewed"], required=True)
    progress_parser.add_argument("--confidence", type=int, choices=range(1, 6), metavar="1-5")
    progress_parser.add_argument("--note", help="Private note stored only in .dsa-study/progress.json")
    review_parser = commands.add_parser("review", help="Show a private review queue from local progress")
    review_parser.add_argument("--all", action="store_true", help="Include not-yet-due reviews")
    review_parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args(argv)
    root = project_root()
    if args.command == "sync":
        document = sync(root, LeetCodeClient(), resume=args.resume, page_size=args.page_size)
        print(f"Synced {len(document['problems'])} problems and {len(document['topics'])} topics.")
    elif args.command == "build":
        document = read_json(catalog_path(root), {"topics": [], "problems": []})
        destination = root / "site"
        render_site(document, destination)
        print(f"Rendered {destination / 'index.html'}")
    elif args.command == "audit":
        document = read_json(catalog_path(root), None)
        if not document:
            raise SystemExit("No local catalog found. Run `dsa-study sync` first.")
        for key, value in audit_catalog(document).items():
            print(f"{key}: {value}")
    elif args.command == "repair-examples":
        document = read_json(catalog_path(root), None)
        if not document:
            raise SystemExit("No local catalog found. Run `dsa-study sync` first.")
        repaired = repair_examples(document)
        write_json(catalog_path(root), document)
        print(f"Repaired examples for {repaired} local catalog records.")
    elif args.command == "new-solution":
        target = create_solution(root, args.problem_id)
        print(f"Created {target}")
    elif args.command == "serve":
        if not 1 <= args.port <= 65535:
            raise SystemExit("--port must be between 1 and 65535.")
        serve(root / "site", port=args.port)
    elif args.command == "progress":
        event = record_progress(root, args.problem_id, args.status, confidence=args.confidence, note=args.note)
        print(f"Recorded private {event['status']} progress for problem {event['problem_id']}.")
    else:
        queue = build_review_queue(root, read_json(catalog_path(root), {}))
        if not args.all:
            queue = [item for item in queue if item["due"]]
        for item in queue[:max(args.limit, 0)]:
            title = f". {item['title']}" if item["title"] else ""
            print(f"{item['problem_id']}{title} — due {item['due_at'][:10]} (confidence {item['confidence']}, {item['last_status']})")
        if not queue:
            print("No private reviews are due.")
