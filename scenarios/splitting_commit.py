import os
from git_commands import run_git_command
from .model import Scenario

def generate_scenario(repo_path):
    os.chdir(repo_path)

    run_git_command(["checkout", "-b", "main"])

    # Create a large commit with changes to multiple files
    for i in range(3):
        with open(f'feature{i}.py', 'w') as f:
            f.write(f"def feature{i}():\n    print('This is feature {i}')\n")
    
    run_git_command(["add", "."])
    run_git_command(["commit", "-m", "Implement multiple features"])

def check_scenario(repo_path):
    os.chdir(repo_path)
    commit_messages = run_git_command(["log", "--format=%s", "main"]).split("\n")
    return len(commit_messages) == 3 and all("feature" in msg for msg in commit_messages)

scenario = Scenario(
    title="Split a Large Commit",
    difficulty="Hard",
    description="You've made a large commit that includes changes to multiple unrelated features.",
    task="Use interactive rebase to split this commit into three separate commits, one for each feature file.",
    hint="Use 'git rebase -i', mark the commit to edit, then use 'git reset HEAD^' and create new commits for each change.",
    generate_func=generate_scenario,
    check_func=check_scenario
)
