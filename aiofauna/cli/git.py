import hashlib
import os
import subprocess


def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()


def git_add():
    run_command("git add .")


def git_commit(path: str = "."):
    sha = hashlib.sha256()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "rb") as f:
                    sha.update(f.read())
                    print(sha.hexdigest())
        for path in dirs:
            git_commit(path)

    run_command(f'git commit -m "{sha.hexdigest()}"')


def git_push():
    run_command("git push origin main")


def main():
    git_add()
    git_commit()
    git_push()
