import os
import random
import time
from git_commands import run_git_command
from .model import Scenario

def generate_scenario(repo_path):
    os.chdir(repo_path)

    run_git_command(["checkout", "-b", "main"])

    # Create a simple Python script
    with open('calc.py', 'w') as f:
        f.write("""
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b
""")

    run_git_command(["add", "calc.py"])
    run_git_command(["commit", "-m", "Initial calculator implementation"])

    # Make 20 commits, introducing a bug randomly
    bug_commit = random.randint(5, 15)
    for i in range(20):
        time.sleep(1)  # Ensure unique timestamps for commits
        if i == bug_commit:
            # Introduce a bug in the multiply function
            with open('calc.py', 'a') as f:
                f.write("""
def multiply(a, b):
    return a * b + 1  # Bug: always adds 1 to the result
""")
        else:
            # Add a harmless comment
            with open('calc.py', 'a') as f:
                f.write(f"\n# Commit {i}")

        run_git_command(["commit", "-am", f"Update {i}"])

def check_scenario(repo_path):
    os.chdir(repo_path)
    with open('calc.py', 'r') as f:
        content = f.read()
    return "return a * b" in content and "return a * b + 1" not in content

scenario = Scenario(
    title="Find a Bug with Git Bisect",
    difficulty="Hard",
    description="A bug was introduced in the 'multiply' function of calc.py somewhere in the last 20 commits.",
    task="Use git bisect to identify the commit that introduced the bug. The bug causes the multiply function to always add 1 to the correct result.",
    hint="Start the bisect process, then use a script to test the multiply function at each step.",
    generate_func=generate_scenario,
    check_func=check_scenario
)
