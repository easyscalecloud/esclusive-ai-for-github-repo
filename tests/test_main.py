# -*- coding: utf-8 -*-

import os

from esclusive_ai_for_github_repo.paths import dir_project_root
from esclusive_ai_for_github_repo.main import (
    Paths,
    Config,
    build_knowledge_base,
)

os.environ["CI"] = "true"
os.environ["GITHUB_SERVER_URL"] = "https://github.com"
os.environ["GITHUB_REPOSITORY"] = "easyscalecloud/esclusive-ai-for-github-repo"
os.environ["GITHUB_REF_NAME"] = "main"
os.environ["GITHUB_TOKEN"] = "dummy-token"

def test_build_knowledge_base():
    paths = Paths(
        dir_project_root=dir_project_root,
    )
    # prepare the downloaded files
    content = dir_project_root.joinpath("prompt.md").read_text()
    paths.path_prompt_md.write_text(content)

    config_data = {
        "document_groups": [
            {
                "name": "all",
                "include": [
                    "esclusive_ai_for_github_repo/**/*.py",
                    "docs/source/**/*.rst",
                    "README.rst",
                ],
                "exclude": [],
            },
            {
                "name": "python",
                "include": [
                    "esclusive_ai_for_github_repo/**/*.py",
                ],
                "exclude": [],
            },
            {
                "name": "document",
                "include": [
                    "docs/source/**/*.rst",
                    "README.rst",
                ],
                "exclude": [],
            },
        ]
    }
    config = Config.from_dict(config_data)

    build_knowledge_base(paths=paths, config=config)


if __name__ == "__main__":
    from esclusive_ai_for_github_repo.tests import run_cov_test

    run_cov_test(
        __file__,
        "esclusive_ai_for_github_repo.main",
        preview=False,
    )
