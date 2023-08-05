import os
import subprocess
from typing import Optional

import fire

from rocket.logger import configure_logger

logger = configure_logger()


def _add_index_urls_to_cmd(cmd, index_urls):
    if index_urls:
        return f"{' '.join(index_urls)} {cmd}"
    else:
        return cmd


class Rocket:
    """Entry point of the installed program, all public methods are options of the program"""

    # in seconds
    _interval_repeat_watch: int = 2
    _python_executable: str = "python3"
    _rocket_executable: str = "rocket"

    def setup(self):
        """
        Initialize the application.
        """
        if os.path.exists("setup.py") or os.path.exists(f"pyproject.toml"):
            print("Packaing file already exists so no need to create a new one")
            return

        content = """
import setuptools

setuptools.setup(
    name="myproject",
    version="0.0.1",
    author="",
    author_email="",
    description="",
    url="https://github.com/getyourguide/databricks-rocket",
    packages=setuptools.find_packages(),
)
        """

        with open("setup.py", "a") as myfile:
            myfile.write(content)

        print("Setup.py file created, feel free to modify it with your needs.")

    def launch(
            self,
            project_location: str = ".",
            dbfs_path: Optional[str] = None,
            watch=True,
            disable_watch=False,
    ):
        """
        Entrypoint of the application, triggers a build and deploy
        :param project_location:
        :param dbfs_folder: path where the wheel will be stored, ex: dbfs:/tmp/myteam/myproject
        :return:
        """

        if os.getenv("DATABRICKS_TOKEN") is None:
            raise Exception("DATABRICKS_TOKEN must be set for db-rocket to work")

        if not dbfs_path:
            dbfs_path = f"dbfs:/temp/{os.environ['USER']}"

        self.project_location = project_location
        project_directory = os.path.dirname(project_location)
        project_directory = project_directory[:-1]

        self.dbfs_folder = dbfs_path + project_directory

        if watch and not disable_watch:
            # first time build and then watch so we have an immediate build
            self._build_and_deploy()
            return self._watch()
        else:
            logger.debug("Watch disabled")

        return self._build_and_deploy()

    def _build_and_deploy(self):
        self._build()
        result = self._deploy()
        return result

    def _watch(self) -> None:
        """
        Listen to filesystem changes to trigger again
        """
        command = 'rocket trigger --disable_watch=True'

        cmd = f"""watchmedo \
                shell-command \
                --patterns='*.py'  \
                --wait --drop \
                --interval {self._interval_repeat_watch} \
                --debug-force-polling \
                --ignore-directories \
                --ignore-pattern '*.pyc;*dist*;\..*;*egg-info' \
                --recursive  \
                --command='{command}' 
              """
        logger.debug(f"watch command: {cmd}")
        os.system(cmd)

    def trigger(
            self,
            project_location: str = ".",
            dbfs_path: Optional[str] = None,
            watch=True,
            disable_watch=False,
    ):
        """
        Entrypoint of the application, triggers a build and deploy
        :param project_location:
        :param dbfs_folder: path where the wheel will be stored, ex: dbfs:/tmp/myteam/myproject
        :return:
        """
        # use launch rather than trigger
        self.launch(project_location=project_location, dbfs_path=dbfs_path, watch=watch, disable_watch=disable_watch)

    def _deploy(self):
        """
        Copies the built library to dbfs
        """

        try:
            self._shell(
                f"databricks fs cp --overwrite {self.wheel_path} {self.dbfs_folder}/{self.wheel_file}"
            )
        except Exception as e:
            raise Exception(
                f"Error while copying files to databricks, is your databricks token set and valid? Try to generate a new token and update existing one with `databricks configure --token`. Error details: {e}"
            )

        install_cmd = f'{self.dbfs_folder.replace("dbfs:/", "/dbfs/")}/{self.wheel_file}'
        install_cmd = _add_index_urls_to_cmd(install_cmd, self.index_urls)

        print(
            f"""Done! in your notebook install the library by running:
            
%pip install --upgrade pip
%pip install {install_cmd} --force-reinstall
        """
        )

    def _build(self):
        """
        builds a library with that project
        """
        logger.info("We are now building your Python repo as a library...")

        # cleans up dist folder from previous build
        dist_location = f"{self.project_location}/dist"
        self._shell(f"rm {dist_location}/* 2>/dev/null || true")

        if os.path.exists(f"{self.project_location}/setup.py"):
            logger.info("Found setup.py. Building python library")
            self._shell(
                f"cd {self.project_location} ; {self._python_executable} -m build --outdir {dist_location} 2>/dev/null"
            )
            self.index_urls = []
            if os.path.exists(f"{self.project_location}/requirements.txt"):
                with open(f"{self.project_location}/requirements.txt") as f:
                    self.index_urls = [line.strip() for line in f.readlines() if "index-url" in line]

        elif os.path.exists(f"{self.project_location}/pyproject.toml"):
            logger.info("Found pyproject.toml. Building python library with poetry")
            self._shell(f"cd {self.project_location} ; poetry build --format wheel")
            requirements = self._shell(
                f"cd {self.project_location} ; poetry export --with-credentials --without-hashes")
            self.index_urls = [line.strip() for line in requirements.split("\n") if "index-url" in line]
        else:
            raise Exception(
                "To be turned into a library your project has to contain a setup.py or pyproject.toml file"
            )

        self.wheel_file = self._shell(
            f"cd {dist_location}; ls *.whl 2>/dev/null | head -n 1"
        ).replace("\n", "")
        self.wheel_path = f"{dist_location}/{self.wheel_file}"
        logger.debug(f"Build Successful. Wheel: '{self.wheel_path}' ")

    @staticmethod
    def _shell(cmd) -> str:
        logger.debug(f"Running shell command: {cmd} ")
        return subprocess.check_output(cmd, shell=True).decode("utf-8")

def main():
    fire.Fire(Rocket)
