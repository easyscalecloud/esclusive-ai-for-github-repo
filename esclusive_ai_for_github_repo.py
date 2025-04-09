# -*- coding: utf-8 -*-

# Copyright (C) 2025 Sanhe Hu <sanhehu@easyscalecloud.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Knowledge Base Builder for GitHub Repositories.

This tools to fetch and consolidate documentation from one GitHub repository
into a single knowledge base file. It handles file filtering,
and content extraction using the ``docpack`` library.

The main workflow:

1. Load configuration from a JSON file
2. Extract files matching include/exclude patterns
3. Combine all content into a single knowledge base file
4. Publish the knowledge base file to GitHub as a release
"""

import typing as T
import os
import sys
import json
import shutil
import dataclasses
from pathlib import Path
from urllib import request
from functools import cached_property

from github import Github, GithubException, Repository
from docpack.api import GitHubPipeline

__version__ = "0.1.1"
__license__ = "AGPL-3.0-or-later"
__author__ = "Sanhe Hu"
__author_email__ = "sanhehu@easyscalecloud.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "sanhehu@easyscalecloud.com"

release_name = "knowledge-base"

IS_CI = "CI" in os.environ

if IS_CI:
    # See: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables
    GITHUB_SERVER_URL = os.environ["GITHUB_SERVER_URL"]
    GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
    GITHUB_REF_NAME = os.environ["GITHUB_REF_NAME"]
    ACC_NAME, REPO_NAME = GITHUB_REPOSITORY.split("/", 1)
    # See: https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication
    GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]


def get_url_content(url: str) -> str:
    """
    Fetch and return the content of a URL as a string.
    """
    with request.urlopen(url) as response:
        return response.read().decode("utf-8").strip()


@dataclasses.dataclass
class Paths:
    """
    Path manager for the knowledge base builder.

    This class handles all file paths and directory structures used by the knowledge base
    builder, including temporary files, output locations, and dependency management.

    .. code-block:: bash

        /project_root               # dir_project_root
        /project_root/tmp               # dir_tmp
    """

    dir_project_root: Path = dataclasses.field()
    path_python_executable: Path = dataclasses.field()

    @property
    def dir_bin(self) -> Path:
        """Directory containing the Python executable and pip."""
        return self.path_python_executable.parent

    @property
    def path_bin_pip(self) -> Path:
        """Path to the pip executable."""
        return self.dir_bin / "pip"

    @cached_property
    def dir_tmp(self) -> Path:
        """
        Temporary directory for working files.
        """
        dir_tmp = self.dir_project_root / "tmp"
        dir_tmp.mkdir(exist_ok=True)
        return dir_tmp

    @property
    def path_esclusive_ai_for_github_repo_config_json(self) -> Path:
        return self.dir_project_root.joinpath(
            ".github",
            "workflows",
            "esclusive_ai_for_github_repo_config.json",
        )

    @property
    def path_prompt_md(self) -> Path:
        """Path to the prompt.md file for AI Prompt."""
        return self.dir_tmp / "prompt.md"

    @property
    def dir_knowledge_base(self):
        """Directory where knowledge base files will be stored."""
        return self.dir_tmp / "knowledge_base"

    @property
    def path_all_in_one_knowledge_base(self) -> Path:
        """Path to the consolidated knowledge base output file."""
        return self.dir_knowledge_base / "all_in_one_knowledge_base.txt"


@dataclasses.dataclass
class Config:
    """
    Configuration for the knowledge base builder.
    """

    include: list[str] = dataclasses.field()
    exclude: list[str] = dataclasses.field()

    @classmethod
    def from_dict(cls, dct: dict[str, T.Any]):
        return cls(**dct)

    @classmethod
    def from_json(cls, path_config: Path):
        print("=== Load config")
        print(f"load config from {path_config}")
        dct = json.loads(path_config.read_text(encoding="utf-8"))
        config = cls.from_dict(dct)
        print("done")
        return config


def build_knowledge_base(
    paths: Paths,
    config: "Config",
):
    """
    Build the knowledge base from all configured sources.

    1. Extract documentation from the GitHub repository.
    2. Combine all extracted files into a single knowledge base file.
    """
    print("=== Build knowledge base")
    print("--- Extract documents from git repo ...")
    github_pipeline = GitHubPipeline(
        domain=GITHUB_SERVER_URL,
        account=ACC_NAME,
        repo=REPO_NAME,
        branch=GITHUB_REF_NAME,
        dir_repo=paths.dir_project_root,
        include=config.include,
        exclude=config.exclude,
        dir_out=paths.dir_knowledge_base,
    )
    github_pipeline.fetch()
    print("--- Combine documents into a single file ...")
    prompt = paths.path_prompt_md.read_text(encoding="utf-8")
    lines = [prompt]
    for path in paths.dir_knowledge_base.glob("*.xml"):
        lines.append(path.read_text(encoding="utf-8"))
    content = "\n".join(lines)
    paths.path_all_in_one_knowledge_base.write_text(content, encoding="utf-8")


def create_tag(repo: Repository):
    default_branch = repo.default_branch
    commit = repo.get_branch(default_branch).commit
    commit_sha = commit.sha
    tag = repo.create_git_tag(
        tag=release_name,
        message=f"Release {release_name}",
        object=commit_sha,
        type="commit",
    )
    repo.create_git_ref(
        ref=f"refs/tags/{release_name}",
        sha=tag.sha,
    )


def create_release(repo: Repository):
    print(f"--- Create release {release_name!r} if not exists ...")
    try:
        release = repo.get_release(release_name)
    except GithubException as e:
        if e.status == 404:  # pragma: no cover
            release = None
        else:
            raise e

    if release is None:
        print(f"Release not exists, creating it ...")
        create_tag(repo)
        release = repo.create_git_release(
            tag=release_name,
            name=release_name,
            message=f"Release {release_name}",
        )
    else:
        print("Release already exists.")
    return release


def upload_assets(
    release: Repository,
    paths: Paths,
):
    print("--- Publish all in one knowledge base")
    file_label = "all_in_one_knowledge_base.txt"
    for asset in release.get_assets():
        if asset.name == file_label:
            asset.delete_asset()
    release.upload_asset(
        path=f"{paths.path_all_in_one_knowledge_base}",
        label=file_label,
    )


def publish_knowledge_base(paths: Paths):
    print("=== Publish knowledge base")
    gh = Github(GITHUB_TOKEN)
    repo = gh.get_repo(GITHUB_REPOSITORY)
    release = create_release(repo)
    upload_assets(release=release, paths=paths)


if __name__ == "__main__":
    paths = Paths(
        dir_project_root=Path.cwd().absolute(),
        path_python_executable=Path(sys.executable).absolute(),
    )
    print(f"{paths.dir_project_root = !s}")
    print(f"{paths.dir_bin = !s}")
    print(f"{paths.path_python_executable = !s}")
    print(f"{paths.path_bin_pip = !s}")
    print(f"{paths.path_esclusive_ai_for_github_repo_config_json = !s}")
    print(f"{paths.dir_tmp = !s}")
    print(f"{paths.dir_knowledge_base = !s}")
    print(f"{paths.path_all_in_one_knowledge_base = !s}")
    print(f"{paths.path_prompt_md = !s}")
    config = Config.from_json(paths.path_esclusive_ai_for_github_repo_config_json)
    build_knowledge_base(paths=paths, config=config)
    publish_knowledge_base(paths=paths)
