import os
from git_commands import run_git_command
from .model import Scenario

def generate_scenario(repo_path):
    os.chdir(repo_path)

    run_git_command(["checkout", "-b", "main"])

    # Create an initial commit
    with open('README.md', 'w') as f:
        f.write("# Git Learning Repository\n\nThis repository is for learning Git commands.\n")
    run_git_command(["add", "README.md"])
    run_git_command(["commit", "-m", "Initial commit"])

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
    hint="Use 'git reset HEAD^' to undo the last commit but keep the changes, then stage and commit each file separately.",
    generate_func=generate_scenario,
    check_func=check_scenario
)
