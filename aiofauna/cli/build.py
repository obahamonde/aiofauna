import os
import shutil
import subprocess


def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()


def build_frontend():
    os.chdir("app")
    run_command("yarn && yarn build")
    os.chdir("..")


def copy_index():
    if not os.path.exists("templates"):
        os.makedirs("templates")
    shutil.copy("static/index.html", "templates/index.html")


def install_requirements():
    run_command("pip install -r requirements.txt")


def main():
    build_frontend()
    copy_index()
    install_requirements()


if __name__ == "__main__":
    main()
