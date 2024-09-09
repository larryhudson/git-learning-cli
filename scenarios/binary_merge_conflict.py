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
    hints=[
        "The 'git merge' command is used to integrate changes from one branch into another.",
        "When a merge conflict occurs with binary files, Git cannot automatically resolve the conflict.",
        "The 'git checkout --theirs <file>' command can be used to choose the version of the file from the branch being merged.",
        "Alternatively, 'git checkout --ours <file>' keeps the version from the current branch.",
        "After resolving a conflict, you need to stage the changes with 'git add' before continuing the merge.",
        "The 'git merge --continue' command completes the merge process after conflicts are resolved.",
        "If you encounter difficulties, 'git merge --abort' can be used to cancel the merge and start over.",
    ],
    generate_func=generate_scenario,
    check_func=check_scenario
)
