import os
from git_commands import run_git_command
from .model import Scenario

def generate_scenario(repo_path):
    os.chdir(repo_path)

    # Create a simple binary file (simulated with a text file)
    with open('image.bin', 'wb') as f:
        f.write(b'\x00\x01\x02\x03')
        run_git_command(["add", "image.bin"])
        run_git_command(["commit", "-m", "Add binary file"])

        # Create two branches with different modifications to the binary file
        run_git_command(["checkout", "-b", "branch1"])
        with open('image.bin', 'wb') as f:
            f.write(b'\x00\x01\x02\x03\x04')
            run_git_command(["commit", "-am", "Modify binary file in branch1"])

            run_git_command(["checkout", "main"])
            run_git_command(["checkout", "-b", "branch2"])
            with open('image.bin', 'wb') as f:
                f.write(b'\x00\x01\x02\x03\x05')
            run_git_command(["commit", "-am", "Modify binary file in branch2"])

            run_git_command(["checkout", "main"])

def check_scenario(repo_path):
    os.chdir(repo_path)
    with open('image.bin', 'rb') as f:
        content = f.read()
        return content == b'\x00\x01\x02\x03\x05'

scenario = Scenario(
    title="Resolve Binary File Merge Conflict",
    difficulty="Hard",
    description="There are conflicting changes to a binary file 'image.bin' in 'branch1' and 'branch2'.",
    task="Merge 'branch1' into 'main', then merge 'branch2', resolving the conflict by keeping the version from 'branch2'.",
    hints=["After the conflict, use 'git checkout --theirs image.bin' to keep the version from the branch you're merging in."],
    generate_func=generate_scenario,
    check_func=check_scenario
)
