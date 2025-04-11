# -*- coding: utf-8 -*-

from esclusive_ai_for_github_repo import api


def test():
    _ = api


if __name__ == "__main__":
    from esclusive_ai_for_github_repo.tests import run_cov_test

    run_cov_test(
        __file__,
        "esclusive_ai_for_github_repo.api",
        preview=False,
    )
