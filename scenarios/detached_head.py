import os
from git_commands import run_git_command
from .model import Scenario

def generate_scenario(repo_path):
    os.chdir(repo_path)

    run_git_command(["checkout", "-b", "main"])

    # Create some commits
    for i in range(5):
        with open(f'file{i}.txt', 'w') as f:
            f.write(f"Content {i}")
        run_git_command(["add", f'file{i}.txt'])
        run_git_command(["commit", "-m", f"Add file{i}.txt"])

    # Get the hash of the third commit
    commit_hash = run_git_command(["rev-parse", "HEAD~2"])

    # Checkout that commit, leading to a detached HEAD
    run_git_command(["checkout", commit_hash])

    # Make a change in the detached HEAD state
    with open('detached_change.txt', 'w') as f:
        f.write("This change was made in a detached HEAD state")
    run_git_command(["add", "detached_change.txt"])
    run_git_command(["commit", "-m", "Change in detached HEAD"])

def check_scenario(repo_path):
    os.chdir(repo_path)
    branches = run_git_command(["branch"]).split("\n")
    if "recovery" not in branches:
        return False
    current_branch = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
    if current_branch != "main":
        return False
    recovery_files = run_git_command(["ls-tree", "-r", "recovery", "--name-only"]).split("\n")
    return "detached_change.txt" in recovery_files

scenario = Scenario(
    title="Recover from Detached HEAD State",
    difficulty="Medium",
    description="You've checked out a specific commit and made changes, ending up in a detached HEAD state.",
    task="Create a new branch called 'recovery' to save your changes, then switch back to the 'main' branch.",
    hint="Use 'git branch' to create a new branch at your current commit, then checkout main.",
    generate_func=generate_scenario,
    check_func=check_scenario
)
