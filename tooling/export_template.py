"""Create a self-contained project repository, including pinned tooling and schemas."""
import argparse,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('destination',type=Path);args=p.parse_args();root=Path(__file__).resolve().parents[1]
if args.destination.exists():raise SystemExit('Destination already exists')
shutil.copytree(root/'templates/project',args.destination)
shutil.copytree(root/'schemas',args.destination/'schemas')
shutil.copytree(root/'tooling',args.destination/'tooling',ignore=shutil.ignore_patterns('__pycache__','tests'))
print(args.destination)
