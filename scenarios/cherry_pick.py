import os
from git_commands import run_git_command
from .model import Scenario

def generate_scenario(repo_path):
    os.chdir(repo_path)

    # Create some commits
    for i in range(3):
        with open(f'file{i}.txt', 'w') as f:
            f.write(f"Content {i}")
        run_git_command(["add", f'file{i}.txt'])
        run_git_command(["commit", "-m", f"Add file{i}.txt"])

    # Create feature branch
    run_git_command(["checkout", "-b", "feature-branch"])

    # Make some changes in feature branch
    for i in range(3, 6):
        with open(f'file{i}.txt', 'w') as f:
            f.write(f"Feature content {i}")
        run_git_command(["add", f'file{i}.txt'])
        run_git_command(["commit", "-m", f"Add feature file{i}.txt"])

    # Add a bug fix commit
    with open('bug_fix.txt', 'w') as f:
        f.write("This is an important bug fix")
    run_git_command(["add", "bug_fix.txt"])
    bug_fix_commit = run_git_command(["commit", "-m", "Fix critical bug"])

    # Switch back to main
    run_git_command(["checkout", "main"])

def check_scenario(repo_path):
    os.chdir(repo_path)
    main_files = run_git_command(["ls-tree", "-r", "main", "--name-only"]).split("\n")
    return "bug_fix.txt" in main_files

scenario = Scenario(
    title="Cherry-pick a Commit",
    difficulty="Medium",
    description="A critical bug fix was made in the 'feature-branch', but it's needed in the 'main' branch immediately.",
    task="Cherry-pick the bug fix commit from 'feature-branch' into 'main'. Then, delete the commit from 'feature-branch'.",
    hints=[
        "The 'git cherry-pick <commit>' command applies the changes from a specific commit to the current branch.",
        "Use 'git log <branch>' to view commit hashes and messages on a specific branch.",
        "The 'git checkout <branch>' command switches to a different branch.",
        "Interactive rebase with 'git rebase -i HEAD~n' allows editing of the last n commits.",
        "During interactive rebase, changing 'pick' to 'drop' for a commit removes it from history.",
        "The 'git push --force' command updates a remote branch, overwriting its history.",
    ],
    generate_func=generate_scenario,
    check_func=check_scenario
)
