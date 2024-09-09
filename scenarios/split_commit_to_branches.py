import os
from git_commands import run_git_command
from .model import Scenario

def generate_scenario(repo_path):
    os.chdir(repo_path)

    # Create multiple files with changes
    for i in range(3):
        with open(f'feature{i}.py', 'w') as f:
            f.write(f"def feature{i}():\n    print('This is feature {i}')\n")
    
    run_git_command(["add", "."])
    run_git_command(["commit", "-m", "Implement multiple features in one commit"])

def check_scenario(repo_path):
    os.chdir(repo_path)
    
    # Check if we have three branches with one commit each
    branches = run_git_command(["branch"]).split("\n")
    if len([b for b in branches if b.strip()]) != 3:
        return False
    
    for branch in branches:
        if branch.strip():
            run_git_command(["checkout", branch.strip()])
            commit_count = len(run_git_command(["log", "--oneline"]).split("\n"))
            if commit_count != 2:  # Initial commit + feature commit
                return False
    
    return True

scenario = Scenario(
    title="Split Commit to Multiple Branches",
    difficulty="Hard",
    description="You've made a large commit that includes changes to multiple unrelated features. Your company has a convention where each PR should only contain one commit.",
    task="Split the 'Implement multiple features in one commit' into three separate branches, each with one commit for a single feature.",
    hint="Use 'git cherry-pick -n <commit>' to apply changes without committing, then create new branches and commit the changes one by one.",
    generate_func=generate_scenario,
    check_func=check_scenario
)
