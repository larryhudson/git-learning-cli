import os
from git_commands import run_git_command
from .model import Scenario

def generate_scenario(repo_path):
    os.chdir(repo_path)

    run_git_command(["checkout", "main"])

    # Create a feature branch with many small commits
    run_git_command(["checkout", "-b", "feature-branch"])

    for i in range(10):
        with open(f'file{i}.txt', 'w') as f:
            f.write(f"Content {i}")
        run_git_command(["add", f'file{i}.txt'])
        run_git_command(["commit", "-m", f"Add file{i}.txt"])

def check_scenario(repo_path):
    os.chdir(repo_path)
    commit_messages = run_git_command(["log", "--format=%s", "feature-branch"]).split("\n")
    return (len(commit_messages) == 2 and
            commit_messages[0] == "Implement new feature" and
            commit_messages[1] == "Initial commit")

scenario = Scenario(
    title="Squash Commits",
    difficulty="Medium",
    description="Your 'feature-branch' has 10 small commits that need to be consolidated before merging into 'main'.",
    task="Use interactive rebase to squash these 10 commits into a single commit with the message 'Implement new feature'.",
    hint="Use 'git rebase -i HEAD~10' and change 'pick' to 'squash' for the commits you want to combine.",
    generate_func=generate_scenario,
    check_func=check_scenario
)
