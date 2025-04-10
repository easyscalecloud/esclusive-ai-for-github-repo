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

A tool that fetches and consolidates documentation from GitHub repositories
into knowledge base files for AI-powered assistance. This allows repository
owners to create searchable knowledge bases without complex setup.

Key features:

- Configurable file inclusion/exclusion via pattern matching
- Automatic GitHub release publishing with knowledge base assets
- CI/CD integration via GitHub Actions

Main workflow:

1. Load configuration from JSON file
2. Extract files matching include/exclude patterns
3. Process and combine content into knowledge base file(s)
4. Publish knowledge base file(s) to GitHub as release assets
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

from github import Github, GithubException, Repository, GitReleaseAsset
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


def write_text(path: Path, text: str):
    try:
        path.write_text(text, encoding="utf-8")
    except FileNotFoundError:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


@dataclasses.dataclass
class Paths:
    """
    Path manager for the knowledge base builder.

    Centralizes all file path handling to ensure consistent locations for
    inputs, outputs, and temporary files across the application. This prevents
    hardcoded paths and makes directory structure changes easier to implement.

    Directory structure:

    .. code-block:: bash
        git_repo/
        git_repo/.github/workflows/esclusive_ai_for_github_repo_config.json
        git_repo/tmp/
        git_repo/tmp/esclusive_ai_for_github_repo.py
        git_repo/tmp/requirements.txt
        git_repo/tmp/prompt.md
        git_repo/tmp/staging/
        git_repo/tmp/staging/${file_1}.xml
        git_repo/tmp/staging/${file_2}.xml
        git_repo/tmp/staging/...
        git_repo/tmp/document_groups/
        git_repo/tmp/document_groups/${group_name_1}.txt
        git_repo/tmp/document_groups/${group_name_2}.txt
        git_repo/tmp/document_groups/...
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
        """Path to the configuration JSON file."""
        return self.dir_project_root.joinpath(
            ".github",
            "workflows",
            "esclusive_ai_for_github_repo_config.json",
        )

    @property
    def path_prompt_md(self) -> Path:
        """Path to the ``prompt.md`` file for AI Prompt."""
        return self.dir_tmp / "prompt.md"

    @property
    def dir_staging(self):
        """Directory where staging files will be stored."""
        return self.dir_tmp / "staging"

    @property
    def dir_document_groups(self) -> Path:
        """Path to the consolidated knowledge base output file."""
        return self.dir_tmp / "document_groups"


@dataclasses.dataclass
class DocumentGroup:
    name: str = dataclasses.field()
    include: list[str] = dataclasses.field()
    exclude: list[str] = dataclasses.field()

    @property
    def asset_name(self) -> str:
        return f"{self.name}.txt"


@dataclasses.dataclass
class Config:
    """
    Configuration for the knowledge base builder.
    """

    document_groups: list[DocumentGroup] = dataclasses.field()

    @classmethod
    def from_dict(cls, dct: dict[str, T.Any]):
        dct["document_groups"] = [
            DocumentGroup(**dct) for dct in dct.get("document_groups", [])
        ]
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

    This is the main processing function that extracts content from
    the repository and combines it into a single knowledge base file.
    """
    print("=== Build knowledge base")
    for group in config.document_groups:
        print(f"--- processing document group {group.name!r}")
        print("Extract documents from git repo ...")
        # Clean up the staging directory to get a fresh start
        shutil.rmtree(paths.dir_staging, ignore_errors=True)
        github_pipeline = GitHubPipeline(
            domain=GITHUB_SERVER_URL,
            account=ACC_NAME,
            repo=REPO_NAME,
            branch=GITHUB_REF_NAME,
            dir_repo=paths.dir_project_root,
            include=group.include,
            exclude=group.exclude,
            dir_out=paths.dir_staging,
        )
        github_pipeline.fetch()
        print("Combine documents into a single file ...")
        prompt = paths.path_prompt_md.read_text(encoding="utf-8")
        lines = [prompt]
        for path in paths.dir_staging.glob("*.xml"):
            lines.append(path.read_text(encoding="utf-8"))
        content = "\n".join(lines)
        path_asset = paths.dir_document_groups.joinpath(group.asset_name)
        print(f"Write to asset file {path_asset}...")
        write_text(path_asset, content)


def create_tag(repo: Repository):
    """
    Create a Git tag for the knowledge base release.

    Creates a tag pointing to the latest commit on the default branch,
    which will be used for the GitHub release.
    """
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
    """
    Create or get the GitHub release for publishing the knowledge base.

    Checks if a release with the specified name already exists.
    If not, creates a new one.
    """
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
    config: "Config",
):
    """
    Upload knowledge base files as assets to the GitHub release.

    Replaces any existing assets with the same names to ensure
    the release always has the latest versions of all document groups.
    """
    print("--- Publish all in one knowledge base")
    file_label = "all_in_one_knowledge_base.txt"
    existing_assets: dict[str, GitReleaseAsset] = {
        asset.name: asset for asset in release.get_assets()
    }
    for group in config.document_groups:
        if group.asset_name in existing_assets:
            existing_assets[group.asset_name].delete_asset()
        release.upload_asset(
            path=f"{paths.dir_document_groups.joinpath(group.asset_name)}",
            label=file_label,
        )


def publish_knowledge_base(paths: Paths, config: "Config"):
    """
    Publish all document group files to GitHub releases.

    This is the main publishing function that handles GitHub authentication,
    release creation, and asset uploading for all document groups.
    """
    print("=== Publish knowledge base")
    gh = Github(GITHUB_TOKEN)
    repo = gh.get_repo(GITHUB_REPOSITORY)
    release = create_release(repo)
    upload_assets(release=release, paths=paths, config=config)


if __name__ == "__main__":
    paths = Paths(
        dir_project_root=Path.cwd().absolute(),
        path_python_executable=Path(sys.executable).absolute(),
    )
    print(f"dir_project_root                              = {paths.dir_project_root}")
    print(f"dir_bin                                       = {paths.dir_bin}")
    print(f"path_python_executable                        = {paths.path_python_executable}")
    print(f"path_bin_pip                                  = {paths.path_bin_pip}")
    print(f"path_esclusive_ai_for_github_repo_config_json = {paths.path_esclusive_ai_for_github_repo_config_json}")
    print(f"dir_tmp                                       = {paths.dir_tmp}")
    print(f"dir_staging                                   = {paths.dir_staging}")
    print(f"dir_document_groups                           = {paths.dir_document_groups}")
    print(f"path_prompt_md                                = {paths.path_prompt_md}")
    config = Config.from_json(paths.path_esclusive_ai_for_github_repo_config_json)
    build_knowledge_base(paths=paths, config=config)
    publish_knowledge_base(paths=paths, config=config)
