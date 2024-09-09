import os
from git_commands import run_git_command
from .model import Scenario

def generate_scenario(repo_path):
    os.chdir(repo_path)

    # Create a file in main
    with open('app.py', 'w') as f:
        f.write("""
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
""")
    run_git_command(["add", "app.py"])
    run_git_command(["commit", "-m", "Initial app implementation"])

    # Create a branch with changes
    run_git_command(["checkout", "-b", "feature-branch"])
    with open('app.py', 'w') as f:
        f.write("""
def greet(name):
    print(f"Hello, {name}!")

def main():
    greet("World")

if __name__ == "__main__":
    main()
""")
    run_git_command(["commit", "-am", "Implement greeting function"])

def check_scenario(repo_path):
    os.chdir(repo_path)
    run_git_command(["checkout", "main"])
    with open('app.py', 'r') as f:
        content = f.read()
    return "def greet(name):" in content and "greet(\"World\")" in content

scenario = Scenario(
    title="Create and Apply a Patch",
    difficulty="Medium",
    description="You need to share your changes in 'feature-branch' with a colleague who doesn't have access to your repository.",
    task="Create a patch file for your changes in 'feature-branch', then apply this patch to 'main'.",
    hints=[
        "Patches can be a way to review and apply changes without merging entire branches.",
        "The 'git format-patch' command creates patch files from commits, useful for sharing changes without direct repository access.",
        "The 'git am' command applies patch files to your current branch, integrating changes from patches into your repository.",
    ],
    generate_func=generate_scenario,
    check_func=check_scenario
)
