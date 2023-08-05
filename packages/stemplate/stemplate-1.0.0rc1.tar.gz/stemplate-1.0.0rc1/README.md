# PyPack

> What does it mean?

The name "PyPack" comes from the contraction of "Python" and "Package".

> What is it for?

PyPack is a template for Python package repositories on GitLab.

> Is it hard to use?

You need to be a bit familiar with python project packaging.

## Background

Designing a [package distribution](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools) for a Python project is a process that can already take some time.
Putting it all together in a repository that allows full use of [GitLab's CI/CD](https://docs.gitlab.com/ee/ci) features can seem like a daunting extra step.
The goal here is to produce a working example of a package distribution repository and to gather information deemed useful.
The Python package used as an example here is called [stemplate](https://pypi.org/project/stemplate).

## Some useful links

Here are some recommended readings for the creation of a package distribution and the implementation of the CI/CD:

* [Tool recommendations](https://packaging.python.org/en/latest/guides/tool-recommendations)
* [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects)
* [PyPi classifiers](https://pypi.org/classifiers)
* [Git Basics - Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
* [`.gitlab-ci.yml` keyword reference](https://docs.gitlab.com/ee/ci/yaml)

## Usage

To use this template follow these steps:

* Download or clone the [template repository](https://gitlab.com/stemplate/python-package).

```bash
git clone git@gitlab.com:stemplate/pypack.git
```

* Replace all occurrences of "stemplate" with the name of your Python package.
* Adapt the files as you wish.
* Remove the `.git` directory and initialize a new one:

```bash
git init --initial-branch=main
git add <your-files>
git commit -m "initial commit"
git tag -a v1.0.0rc -m "version 1.0.0rc"
```

* Build and upload the package on [Pypi](https://pypi.org):

```bash
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade twine
python3 -m pip install --upgrade build
python3 -m build
python3 -m twine upload dist/*
```

* Create an empty repository on [GitLab](https://gitlab.com) for your package distribution.
* Create an API token for the project on PyPi. (Use the url address of your GitLab repository to name the token in PyPi.)
* Add the PyPi Token variables on GitLab (Project > Settings > CI/CD > Variables):
    1. `TWINE_USERNAME`: `__token__` (Add "Protect", "Mask", and "Expand" options)
    2. `TWINE_PASSWORD`: *token value* (Add "Protect", "Mask", and "Expand" options)
* Protect `v*` tags (Project > Settings > Repository > Protected tags).
* Make sure that the `main` branch is protected (Project > Settings > Repository > Protected branch).
* Push:

```bash
git remote add origin git@gitlab.com:<user/project>.git
git push origin main --tags
```

At this stage your project is both on GitLab and on PyPi, and the pipeline should have been launched on GitLab.
The latter is configured in the [`.gitlab-ci.yml`](.gitlab-ci.yml) file.
The configuration proposed here allows to run the tests each time GitLab receives a push.

* Do not work on the main branch, create another one ("dev"?).
* Make some potential modifications so that the pipeline runs without errors.
* After merging your working branch into the main branch, if the pipeline passed, add a tag `v1.0.0` "version 1.0.0" directly on GitLab. This will automatically deploy the release on PyPi.

Repeat these steps (from creating a new branch) for each modification made to the project (without forgetting to adapt the version in the tag on GitLab).

## README template

The following is a template for the README.md file.

```markdown
# Package name

> What does it mean?

The name "Stemplate" comes from the contraction of "Stem" and "Template".

> What is it for?

Stemplate is a useless Python package.

> Is it hard to use?

Just type one of the available commands in a terminal.

## Background

The context and the problems addressed.

## Features

What the package allows you to do.

* `command1`: To ...
* `command2`: To ...

## Installation

### Virtual environment

How to create a virtual environment.

### PyPi

How to install from PyPi.

### Editable mode

How to install in editable mode.

## Usage

### Accepted arguments

How to print help.

### Command 1

How to use feature 1.

### Command 2

How to use feature 2.

### Configuration

How to configure the package.

## Credits

* Author Name
* Contributor Name

## License

License information.
```

## Credits

* Dunstan Becht

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
