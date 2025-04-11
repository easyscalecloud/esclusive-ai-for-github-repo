# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
from esclusive_ai_for_github_repo.paths import dir_project_root

os.environ["CI"] = "true"
os.environ["GITHUB_SERVER_URL"] = "https://github.com"
os.environ["GITHUB_REPOSITORY"] = "easyscalecloud/esclusive-ai-for-github-repo"
os.environ["GITHUB_REF_NAME"] = "main"
os.environ["GITHUB_TOKEN"] = "dummy-token"

from esclusive_ai_for_github_repo.main import (
    get_url_content,
    write_text,
    Paths,
    DocumentGroup,
    Config,
    build_knowledge_base,
    create_tag,
    create_release,
    upload_assets,
    publish_knowledge_base,
)

def test_build_knowledge_base():
    paths = Paths(
        dir_project_root=dir_project_root,
        path_python_executable=Path(sys.executable),
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
