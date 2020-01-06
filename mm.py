#!/usr/bin/env python
"""
This file generates all the necessary files for packaging for the project.
Read more about it at https://github.com/jpscaletti/mastermold/
"""
data = {
    "title": "Styled Components",
    "name": "styled_components",
    "pypi_name": "styled_components",
    "version": "1.0",
    "author": "Juan-Pablo Scaletti",
    "author_email": "juanpablo@jpscaletti.com",
    "description": "Testeable, reusable, fast, and scalable server-side-rendered components.",
    "copyright": "2019",
    "repo_name": "jpscaletti/styled_components",
    "home_url": "",
    "project_urls": {},
    "development_status": "5 - Production/Stable",
    "minimal_python": 3.6,
    "install_requires": [
        "jinja2 ~= 2.10",
        "libsass ~= 1.13",
    ],
    "testing_requires": [
        "pytest",
        "pytest-cov",
    ],
    "development_requires": [
        "flake8",
        "ipdb",
        "tox",
    ],
    "coverage_omit": [],
}


def do_the_thing():
    import hecto

    hecto.copy(
        "gh:jpscaletti/mastermold.git",
        # "../mastermold",  # Path to the local copy of Master Mold
        ".",
        data=data,
        force=False,
        exclude=[
            ".*",
            ".*/*",
            "README.md",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
        ],
    )


if __name__ == "__main__":
    do_the_thing()
