import os
from git_commands import run_git_command
from .model import Scenario

def generate_scenario(repo_path):
    os.chdir(repo_path)

    # Create a large commit with changes to multiple files
    for i in range(3):
        with open(f'feature{i}.py', 'w') as f:
            f.write(f"def feature{i}():\n    print('This is feature {i}')\n")
    
    run_git_command(["add", "."])
    run_git_command(["commit", "-m", "Implement multiple features"])

def check_scenario(repo_path):
    os.chdir(repo_path)
    commit_messages = run_git_command(["log", "--format=%s", "main"]).split("\n")
    return len(commit_messages) == 4 and sum("feature" in msg for msg in commit_messages) == 3

scenario = Scenario(
    title="Split a Large Commit",
    difficulty="Hard",
    description="You've made a large commit that includes changes to multiple unrelated features.",
    task="Split the 'Implement multiple features' commit into three separate commits, one for each feature file.",
    hints=[
        "The 'git reset' command can move the HEAD and branch pointer, potentially unstaging changes or even discarding commits.",
        "Interactive staging with 'git add -p' allows you to selectively stage parts of a file, useful for creating more focused commits.",
        "The 'git commit --amend' command can modify the most recent commit, either changing its message or adding more changes.",
        "Git's 'cherry-pick' can apply the changes from a specific commit to your current branch, which can be useful in reorganizing commits.",
    ],
    generate_func=generate_scenario,
    check_func=check_scenario
)
