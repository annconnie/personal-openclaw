#!/usr/bin/env python3
import datetime
import random
import subprocess
import time
from pathlib import Path


def format_timestamp(dt: datetime.datetime) -> str:
    hour = dt.hour % 12 or 12
    am_pm = "AM" if dt.hour < 12 else "PM"
    return f"{hour}:{dt.minute:02d}{am_pm} {dt.month}/{dt.day}/{dt.year}"


def run_git_command(args):
    subprocess.run(["git"] + args, check=True)


def append_readme_comment(readme_path: Path, text: str) -> None:
    content = readme_path.read_text(encoding="utf-8")
    content += f"\n{text}\n"
    readme_path.write_text(content, encoding="utf-8")


def main() -> None:
    repo_dir = Path(__file__).resolve().parent
    readme_path = repo_dir / "README.md"
    if not readme_path.exists():
        raise SystemExit("README.md not found in repository root.")

    commit_count = random.choice([1, 3, 4, 5])
    print(f"Creating {commit_count} random README commit(s)...")

    for index in range(commit_count):
        timestamp = format_timestamp(datetime.datetime.now())
        comment = f"#this is added at {timestamp}"
        append_readme_comment(readme_path, comment)

        run_git_command(["add", str(readme_path)])
        run_git_command(["commit", "-m", f"Random README update at {timestamp}"])
        print(f"Committed {index + 1}/{commit_count}: {comment}")

        run_git_command(["push", "origin", "HEAD"])
        print(f"Pushed commit {index + 1}/{commit_count} to origin.")

        if index < commit_count - 1:
            pause = random.randint(10, 60)
            print(f"Waiting {pause} second(s) before next commit...")
            time.sleep(pause)


if __name__ == "__main__":
    main()
