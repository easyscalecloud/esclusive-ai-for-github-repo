# -*- coding: utf-8 -*-

"""
Publish esclusive_repo_ai to GitHub as a release.
"""

import typing as T
from pathlib import Path

from github import (
    Github,
    GithubException,
    GitTag,
    GitRef,
    GitRelease,
)

from esclusive_ai_for_github_repo import __version__


# ------------------------------------------------------------------------------
# Prepare parameters
# ------------------------------------------------------------------------------
tag_name = __version__
release_name = __version__
dir_here = Path(__file__).absolute().parent
repo_name = dir_here.name
account_name = "easyscalecloud"
release_asset_list = [
    "esclusive_ai_for_github_repo.py",
    "prompt.md",
    "requirements.txt",
]
path_github_token = Path.home().joinpath(
    ".github",
    "pac",
    "MacHu-GWU",
    "sanhe-dev.txt",
)
github_token = path_github_token.read_text(encoding="utf-8").strip()
gh = Github(github_token)
repo = gh.get_repo(f"{account_name}/{repo_name}")


def get_latest_commit_sha() -> str:
    return repo.get_branch(repo.default_branch).commit.sha


def get_git_tag_and_ref(tag_name: str) -> tuple[
    T.Optional["GitTag"],
    T.Optional["GitRef"],
]:
    try:
        ref = repo.get_git_ref(f"tags/{tag_name}")
    except GithubException as e:
        if e.status == 404:
            return (None, None)
        else:  # pragma: no cover
            raise e
    except Exception as e:
        raise e

    tag_sha = ref.object.sha

    try:
        tag = repo.get_git_tag(tag_sha)
    except GithubException as e:
        if e.status == 404:
            return (None, ref)
        else:  # pragma: no cover
            raise e
    except Exception as e:
        raise e

    return (tag, ref)


def get_git_release(release_name: str) -> T.Optional["GitRelease"]:
    """
    :param release_name:

    :return: GitRelease object or None if not found
    """
    try:
        return repo.get_release(release_name)
    except GithubException as e:
        if e.status == 404:
            return None
        else:  # pragma: no cover
            raise e
    except Exception as e:  # pragma: no cover
        raise e


def is_tag_latest_on_main(tag_name: str) -> tuple[
    bool,
    T.Optional["GitTag"],
    T.Optional["GitRef"],
    T.Optional[str],
]:
    """
    Check if the tag is the latest on the main branch.

    :returns: a tuple of four elements:
    """
    latest_commit_sha = get_latest_commit_sha()
    tag, ref = get_git_tag_and_ref(tag_name)
    if tag is None:
        return (False, tag, ref, latest_commit_sha)
    else:
        flag = tag.object.sha == latest_commit_sha
        return (flag, tag, ref, latest_commit_sha)


def clean_up_existing_release(release_name: str) -> bool:
    """
    :returns: a boolean flag to indicate whether the operation is performed.
    """
    release = get_git_release(release_name)
    if release is None:
        return False
    else:
        release.delete_release()
        return True


def clean_up_existing_tag(tag_name: str) -> bool:
    """
    :returns: a boolean flag to indicate whether the operation is performed.
    """
    try:
        ref = repo.get_git_ref(f"tags/{tag_name}")
        ref.delete()
        return True
    except GithubException as e:
        if e.status == 404:
            return False
        else:  # pragma: no cover
            raise e


def create_tag(
    tag_name: str,
    latest_commit_sha: T.Optional[str] = None,
) -> tuple["GitTag", "GitRef"]:
    if latest_commit_sha is None:
        latest_commit_sha = get_latest_commit_sha()
    tag = repo.create_git_tag(
        tag=tag_name,
        message=f"Tag {tag_name}",
        object=latest_commit_sha,
        type="commit",
    )
    ref = repo.create_git_ref(
        ref=f"refs/tags/{tag_name}",
        sha=tag.sha,
    )
    return tag, ref


def create_release(tag_name: str, release_name: str) -> "GitRelease":
    return repo.create_git_release(
        tag=tag_name,
        name=release_name,
        message=f"Release {release_name}",
    )


def update_release(
    tag_name: str,
    release_name: str,
) -> tuple[
    bool,
    T.Optional["GitTag"],
    T.Optional["GitRef"],
    T.Optional["GitRelease"],
]:
    """
    Update the GitHub release and tag.

    :returns: a boolean flag to indicate whether the operation is performed.
    """
    print("Checking if the tag is latest on main branch...")
    (flag, tag, ref, latest_commit_sha) = is_tag_latest_on_main(tag_name)
    print(f"Tag = {tag}, Ref = {ref}, Latest commit SHA = {latest_commit_sha}")
    if flag is True:
        print("Tag is latest on main branch, no need to update.")
        return False, tag, ref, None
    else:
        print("Tag is not latest on main branch, updating ...")
    print("Cleaning up existing release and tag ...")
    clean_up_existing_release(release_name)
    if tag is not None:
        print("Cleaning up existing tag ...")
        clean_up_existing_tag(tag_name)
    print("Creating new tag ...")
    tag, ref = create_tag(tag_name=tag_name, latest_commit_sha=latest_commit_sha)
    print("Creating new release ...")
    release = create_release(tag_name=tag_name, release_name=release_name)
    print("Done!")
    return True, tag, ref, release


def update_assets(
    release: "GitRelease",
    path_list: T.List[Path],
):
    filename_set = {path.name for path in path_list}
    for asset in release.get_assets():
        if asset.name in filename_set:
            asset.delete_asset()
    for path in path_list:
        print(f"Uploading asset {path.name!r} ...")
        release.upload_asset(
            path=f"{path}",
            label=path.name,
        )


if __name__ == "__main__":
    flag, tag, ref, release = update_release(
        tag_name=tag_name, release_name=release_name
    )
    if release is None:
        release = get_git_release(release_name)
    update_assets(
        release=release,
        path_list=[dir_here.joinpath(file_name) for file_name in release_asset_list],
    )
