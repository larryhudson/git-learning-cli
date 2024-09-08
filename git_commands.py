import subprocess

def run_git_command(command, repo_path=None):
    if repo_path:
        command = ["-C", repo_path] + command
    result = subprocess.run(["git"] + command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Git command failed: {result.stderr}")
    return result.stdout.strip()
