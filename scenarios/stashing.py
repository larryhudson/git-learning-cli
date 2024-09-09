import os
from git_commands import run_git_command
from .model import Scenario

def generate_scenario(repo_path):
    os.chdir(repo_path)

    with open('app.py', 'w') as f:
        f.write("""
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
""")
    run_git_command(["add", "app.py"])
    run_git_command(["commit", "-m", "Initial app implementation"])

    # Create and switch to feature branch
    run_git_command(["checkout", "-b", "feature-branch"])
    
    # Make some uncommitted changes
    with open('app.py', 'a') as f:
        f.write("""
def new_feature():
    print("This is a new feature!")

# TODO: Integrate new_feature into main
""")

    # Switch back to main and introduce a "critical bug"
    run_git_command(["checkout", "main"])
    with open('app.py', 'w') as f:
        f.write("""
def main():
    print("Hello, World!")
    critial_bug()  # Typo: should be 'critical_bug'

if __name__ == "__main__":
    main()
""")
    run_git_command(["commit", "-am", "Update main function (with bug)"])

def check_scenario(repo_path):
    os.chdir(repo_path)
    # Check if we're on feature-branch
    current_branch = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
    if current_branch != "feature-branch":
        return False
    
    # Check if the bug is fixed in main
    run_git_command(["checkout", "main"])
    with open('app.py', 'r') as f:
        content = f.read()
    if "critical_bug()" not in content:
        return False
    
    # Check if the new feature is in feature-branch
    run_git_command(["checkout", "feature-branch"])
    with open('app.py', 'r') as f:
        content = f.read()
    return "def new_feature():" in content

scenario = Scenario(
    title="Stash Changes and Apply",
    difficulty="Easy",
    description="You're working on a new feature when a critical bug is reported in the main branch.",
    task="Stash your changes in the 'feature-branch', switch to 'main', fix the typo in the function name (change 'critial_bug' to 'critical_bug'), commit the fix, then return to 'feature-branch' and apply your stashed changes.",
    hints=["Use 'git stash' to save your changes, 'git checkout' to switch branches, and 'git stash pop' to reapply your changes."],
    generate_func=generate_scenario,
    check_func=check_scenario
)
