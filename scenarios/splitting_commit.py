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
        "Start by using 'git reset HEAD^' to undo the commit. This will unstage all changes.",
        "Use 'git add' to stage changes for each feature file separately.",
        "Create a new commit for each feature file using 'git commit -m \"Implement feature X\"'.",
        "Repeat the process for all three feature files."
    ],
    generate_func=generate_scenario,
    check_func=check_scenario
)
