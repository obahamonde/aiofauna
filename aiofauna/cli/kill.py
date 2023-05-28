
import os
import signal
import subprocess


def kill_process_on_port(port):
    command = f"lsof -t -i:{port}"
    pid_str = subprocess.check_output(command, shell=True)
    if isinstance(pid_str, bytes):
        pid_str = pid_str.decode("utf-8")
    elif isinstance(pid_str, str):
        pass
    else:
        raise TypeError(f"Expected bytes or string, got {type(pid_str)}")

    if pid_str:
        for pid in pid_str.split("\n"):
            if pid:  # Check if pid is not an empty string
                os.kill(int(pid), signal.SIGKILL)
                print(f"Killed process {pid} on port {port}")
    else:
        print(f"No process on port {port}")


def main():
    port = input("Enter port number to kill process: ")
    kill_process_on_port(port)
