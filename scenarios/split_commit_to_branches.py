import os
from git_commands import run_git_command
from .model import Scenario

def generate_scenario(repo_path):
    os.chdir(repo_path)

    # Create multiple files with changes and dependencies
    with open('feature1.py', 'w') as f:
        f.write("def feature1():\n    return 'Feature 1 output'\n")

    with open('feature2.py', 'w') as f:
        f.write("from feature1 import feature1\n\n"
                "def feature2():\n"
                "    return f'Feature 2 uses {feature1()}'\n")

    with open('feature3.py', 'w') as f:
        f.write("from feature2 import feature2\n\n"
                "def feature3():\n"
                "    return f'Feature 3 builds on {feature2()}'\n")

    run_git_command(["add", "."])
    run_git_command(["commit", "-m", "Implement multiple interdependent features in one commit"])

def check_scenario(repo_path):
    os.chdir(repo_path)
    
    # Check if we have three branches with one commit each
    branches = run_git_command(["branch"]).split("\n")
    branches = [b.strip() for b in branches if b.strip()]
    if len(branches) != 3:
        return False
    
    # Check the content and order of the branches
    expected_order = ['feature1', 'feature2', 'feature3']
    for i, branch in enumerate(sorted(branches)):
        run_git_command(["checkout", branch])
        
        # Check if the branch has only one commit (plus the initial commit)
        commit_count = len(run_git_command(["log", "--oneline"]).split("\n"))
        if commit_count != 2:
            return False
        
        # Check if the correct file exists in each branch
        if not os.path.exists(f'{expected_order[i]}.py'):
            return False
        
        # Check if the dependencies are correct
        with open(f'{expected_order[i]}.py', 'r') as f:
            content = f.read()
            if i > 0 and f'from {expected_order[i-1]}' not in content:
                return False
    
    return True

scenario = Scenario(
    title="Split Commit to Multiple Branches",
    difficulty="Hard",
    description="You've made a large commit that includes changes to multiple interdependent features. Your company has a convention where each PR should only contain one commit.",
    task="Split the 'Implement multiple interdependent features in one commit' into three separate branches, each with one commit for a single feature. Ensure that the dependencies between features are maintained.",
    hint="You can use either interactive rebase or cherry-pick to split the commit:\n"
         "1. For interactive rebase: On the branch with the complex commit, use 'git rebase -i HEAD~1', change 'pick' to 'edit' for the commit, then use 'git reset HEAD^' to unstage changes. Create new branches from this point and commit changes one by one.\n"
         "2. For cherry-pick: Create a new branch from the commit before the complex one. Then use 'git cherry-pick -n <complex-commit-hash>' to apply changes without committing. Create new branches from this point and commit the changes one by one.\n"
         "In both cases, pay attention to the order of the features due to their dependencies.",
    generate_func=generate_scenario,
    check_func=check_scenario
)
