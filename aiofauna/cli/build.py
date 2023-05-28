import os
import shutil
import subprocess
import sys
from abc import ABC, abstractmethod


class BuildStrategy(ABC):
    @abstractmethod
    def build(self) -> None:
        pass


UNDEBUGGABLE_EXIT_CODES = (1, 2, 126, 127, 128, 130, 255)


class NodeJSBinaryStrategy(BuildStrategy):
    def build(self) -> None:
        try:
            platform = sys.platform
            node = self._search_node_binary(platform)
            npm = self._search_npm_binary(platform)
            print(f"Node: {node}")
            print(f"NPM: {npm}")
            spa_project_path: str = "./app"
            subprocess.check_call([node, "--version"])
            subprocess.check_call([npm, "--version"])
            subprocess.check_call([npm, "install"], cwd=spa_project_path)
            subprocess.check_call([npm, "run", "build"], cwd=spa_project_path)
        except Exception as e:
            print(e)
            raise e

    def _search_node_binary(self, platform: str) -> str:
        if platform == "linux":
            _ref = subprocess.check_output(["which", "node"])
            return _ref.decode("utf-8").strip()
        if platform == "darwin":
            _ref = subprocess.check_output(["which", "node"])
            return _ref.decode("utf-8").strip()
        if platform == "win32":
            _ref = subprocess.check_output(["where", "node"])
            return _ref.decode("utf-8").strip()
        raise Exception("Unsupported platform: {}".format(platform))

    def _search_npm_binary(self, platform: str) -> str:
        if platform == "linux":
            _ref = subprocess.check_output(["which", "npm"])
            return _ref.decode("utf-8").strip()
        if platform == "darwin":
            _ref = subprocess.check_output(["which", "npm"])
            return _ref.decode("utf-8").strip()
        if platform == "win32":
            _ref = subprocess.check_output(["where", "npm"])
            return _ref.decode("utf-8").strip()
        else:
            try:
                self._forcefully_install_nodejs()

            except OSError as e:
                _exit_code_number = e.errno

                if _exit_code_number in UNDEBUGGABLE_EXIT_CODES:
                    self._gracefully_exit()
                else:
                    raise e
            except Exception as e:
                raise e
            else:
                self._search_npm_binary(platform)
        raise Exception("Unsupported platform: {}".format(platform))

    def _forcefully_install_nodejs(self) -> None:
        try:
            subprocess.check_call(["sudo", "apt", "install", "nodejs", "-y"])
        except Exception as e:
            raise e

    def _gracefully_exit(self) -> None:
        print("NodeJS is not installed. Please install it and try again.")
        sys.exit(1)


class PythonStrategy(BuildStrategy):
    def build(self) -> None:
        try:
            subprocess.check_call(
                ["python", "-m", "pip", "install", "-r", "requirements.txt"]
            )
            if not os.path.exists("templates"):
                os.makedirs("templates")
                shutil.copy("static/index.html", "templates/index.html")
        except Exception as e:
            raise e


class Build:
    def __init__(self, strategy: BuildStrategy) -> None:
        self.strategy = strategy

    def build(self) -> None:
        self.strategy.build()

    def __call__(self) -> None:
        self.strategy.build()


def build_node() -> None:
    build = Build(NodeJSBinaryStrategy())
    build()     
    
    
def build_python() -> None:
    build = Build(PythonStrategy())
    build()
    
    
def main() -> None:
    build_node()
    build_python()
    