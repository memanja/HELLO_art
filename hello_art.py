
#!/usr/bin/env python3

import os
import random
import subprocess
from datetime import date, datetime, timedelta

# ==========================================
# GITHUB CONFIGURATION
# ==========================================

GITHUB_USERNAME = "memanja"
GITHUB_EMAIL = "48172171+memanja@users.noreply.github.com"

REPO_URL = "https://github.com/memanja/HELLO_art.git"
BRANCH = "main"

# ==========================================
# CONTRIBUTION GRAPH CONFIGURATION
# ==========================================

WORD = "HELLO"
WEEKS_BACK = 45

# Random seed: change this to generate a different pattern
RANDOM_SEED = 20261117

# ==========================================
# FONT
# ==========================================

FONT = {
    "H": ["X...X", "X...X", "XXXXX", "X...X", "X...X"],
    "E": ["XXXXX", "X....", "XXXX.", "X....", "XXXXX"],
    "L": ["X....", "X....", "X....", "X....", "XXXXX"],
    "O": [".XXX.", "X...X", "X...X", "X...X", ".XXX."],
}

# ==========================================
# GIT HELPERS
# ==========================================

def run_git(command, env=None):
    subprocess.run(command, check=True, env=env)


def setup_git():
    if not os.path.isdir(".git"):
        run_git(["git", "init", "-b", BRANCH])

    run_git(["git", "config", "user.name", GITHUB_USERNAME])
    run_git(["git", "config", "user.email", GITHUB_EMAIL])

    remotes = subprocess.check_output(
        ["git", "remote"], text=True
    ).splitlines()

    if "origin" not in remotes:
        run_git(["git", "remote", "add", "origin", REPO_URL])


# ==========================================
# GENERATE WORD
# ==========================================

def generate_word():
    rows = ["", "", "", "", ""]

    for i, ch in enumerate(WORD.upper()):
        if ch not in FONT:
            raise ValueError(f"Unsupported character: {ch}")

        for r in range(5):
            rows[r] += FONT[ch][r]

            if i < len(WORD) - 1:
                rows[r] += "."

    return rows


# ==========================================
# CREATE COMMITS
# ==========================================

def create_commits():
    today = date.today()

    last_sunday = today - timedelta(
        days=(today.weekday() + 1) % 7
    )

    start = last_sunday - timedelta(weeks=WEEKS_BACK)

    rows = generate_word()
    rng = random.Random(RANDOM_SEED)

    total = 0
    pixel_count = 0

    print("\nGenerating HELLO pattern...\n")

    for r, line in enumerate(rows):
        for c, pixel in enumerate(line):

            if pixel != "X":
                continue

            day = start + timedelta(
                weeks=c,
                days=r + 1
            )

            if day > today:
                continue

            # Vary commit counts for testing/visualization
            commits = rng.randint(1, 25)

            stamp = datetime(
                day.year,
                day.month,
                day.day,
                12
            ).isoformat()

            env = {
                **os.environ,
                "GIT_AUTHOR_DATE": stamp,
                "GIT_COMMITTER_DATE": stamp,
            }

            print(f"{day}: {commits} commits")

            for n in range(commits):
                run_git([
                    "git",
                    "commit",
                    "--allow-empty",
                    "-m", f"{WORD} {day} #{n + 1}"
                ], env=env)

                total += 1

            pixel_count += 1

    print("\n================================")
    print("GENERATION SUMMARY")
    print("================================")
    print(f"Word             : {WORD}")
    print(f"Active pixels    : {pixel_count}")
    print(f"Total commits    : {total}")
    print(f"Average per pixel: {total / pixel_count:.2f}" if pixel_count else "No pixels")
    print("================================\n")


# ==========================================
# PUSH TO GITHUB
# ==========================================

if __name__ == "__main__":

    setup_git()

    create_commits()

    run_git([
        "git",
        "push",
        "-u",
        "origin",
        BRANCH
    ])

    print("Finished!")
