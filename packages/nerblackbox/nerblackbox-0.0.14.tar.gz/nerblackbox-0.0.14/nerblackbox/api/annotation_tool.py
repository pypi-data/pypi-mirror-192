import zipfile
import os
from configparser import ConfigParser
from typing import Optional
from os.path import isfile
from doccano_client import DoccanoClient
from nerblackbox.modules.annotation.annotation import (
    nerblackbox2doccano,
    doccano2nerblackbox,
)


class AnnotationTool:
    def __init__(self, tool: str, config_file: Optional[str] = None):
        assert tool == "doccano", f"only doccano implemented."
        if config_file is None:
            url = "http://localhost:8080"
            username = "admin"
            password = "password"
        else:
            assert isfile(config_file), f"config file {config_file} does not exist."
            config = ConfigParser()
            config.read(config_file)
            config_dict = dict(config.items("main"))
            url = config_dict["url"]
            username = config_dict["username"]
            password = config_dict["password"]
            print(f"> read config from {config_file}")

        self.client = DoccanoClient(url)
        self.client.login(username=username, password=password)

    def download(self, project, file_path: str):
        # 1. download data
        downloaded_file_path = self.client.download(
            project.id,
            "JSONL",
        )
        print(
            f"> download data from project = {project.name} to {downloaded_file_path}"
        )

        # 2. unzip
        with zipfile.ZipFile(downloaded_file_path, "r") as zip_ref:
            zip_ref.extractall("original_data")
        os.remove(downloaded_file_path)
        print(f"> unzip file + remove zip")

        # 3. translate format from doccano to nerblackbox
        doccano2nerblackbox("original_data/admin.jsonl", file_path)
        print(f"> translate data to nerblackbox format")
        print(f"> save data at {file_path}")

    def upload(self, project_name: str, file_path: str):
        # 0. translate format from nerblackbox to doccano
        file_path = nerblackbox2doccano(file_path)
        print(f"> translated data to doccano format")

        # 1. create project
        project = self.client.create_project(
            project_name,
            project_type="SequenceLabeling",
            description="description",
        )
        print(f"> created project {project_name}")

        # 2. create label
        self.client.create_label_type(project.id, "span", "PI", color="#000000")
        print(f"> added label 'PI'")

        # 3. upload data
        self.client.upload(
            project.id,
            [file_path],
            "SequenceLabeling",
            "JSONL",
            "text",
            "label",
        )
        print(f"> uploaded file {file_path}")

        return project
