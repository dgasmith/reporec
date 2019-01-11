reporec
==============================
[//]: # (Badges)
[![Travis Build Status](https://travis-ci.com/dgasmith/reporec.png)](https://travis-ci.com/dgasmith/reporec)
[![codecov](https://codecov.io/gh/dgasmith/reporec/branch/master/graph/badge.svg)](https://codecov.io/gh/dgasmith/reporec/branch/master)

Records GitHub statistics for information and funding agencies.

## Installation

Clone this repository and install with `pip install .`.

## Usage

1. Write a YAML file (e.g. `yourrepos.yaml`) using the same format as the files in `examples/`. Currently `reporec` can access statistics from GitHub repositories and conda packages.
2. If you need access to GitHub statistics, get a GitHub API [Personal Access token](https://github.com/settings/tokens). `reporec`'s token requires full access to the `repo` category and subcategories. Export the GitHub API token to your shell environment with `export GITHUB_TOKEN=<your token here>`
3. Run `reporec yourrepos.yaml` to generate reports. A directory `rrdata` will be created in the current working directory, containing CSV reports named like `<repo>-<stat_source>.csv`.
4. Consider running `reporec` regularly to track statistics over time!

### Copyright

Copyright (c) 2018, Daniel G. A. Smith


#### Acknowledgements

Project based on the
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms)
