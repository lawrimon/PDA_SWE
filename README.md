<h1 align="center">Welcome to PDA :wave:</h1>

<p align="center">
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg"/> 
  </a>
  <a href="https://conventionalcommits.org">
    <img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white" />
  </a>
    <a href=https://github.com/lawrimon/PDA_SWE/actions/workflows/python_ci.yaml>
    <img src="https://github.com/lawrimon/PDA_SWE/actions/workflows/python_ci.yaml/badge.svg" />
  </a>
</p>

> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
  
# Description
Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

# Documentation

- Technical Documentation
- ...

# Usage

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

# Installation

The project requires the following libraries:

- `pandas`

To install these libraries globally, run the following command (**unrecommended**):

```
pip install -r requirements.txt
```

To install these libraries in a conda environment, run the following command (**recommended**):

```
conda create --name <thisproject>
conda activate <thisproject>
pip install -r requirements.txt
```

# Development Guidelines

## Branching Model

The branching model in this project is based on the [Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow). The main branch is called `main`. The `main` branch is protected and can only be changed by pull requests. For each feature  issue, a new feature branch is created from `main`. The branch is named `feature/<issue-number>`, e.g. `feature/30`. After the feature is implemented, a pull request is created to merge the feature branch into `main`. Close the feature issue and related child tasks by adding the `closes #<issue-number>` keyword to the pull request description, e.g. `Closes #30, closes #31, closes #32`. After the pull request is merged, the feature branch is deleted. The following image shows the branching model:
<p align="center">
<img src="https://wac-cdn.atlassian.com/dam/jcr:a905ddfd-973a-452a-a4ae-f1dd65430027/01%20Git%20branch.svg?cdnVersion=821" width="500">
</p>

## Code Reviews

Each pull request must be reviewed by two developers. The reviewers must be different from the developer who created the pull request. The reviewers must approve the pull request before it can be merged. The following image shows the code review process:
<p align="center">
<img src="https://images.ctfassets.net/zsv3d0ugroxu/Z8dtCNdftgdcNAFQEnyYy/bc728a50ec535ed7ff5f062ef532efbd/PR_review_process" width="500">

## Commit Messages

Each commit message must conform to the [Commit Message Structure](#commit-structure) format which is based on the [Conventional Commits](https://conventionalcommits.org) specification.

### <a name="commit-structure"></a>Commit Message Structure
```
<type>(<scope>): <subject>
  ???       ???             ???
  ???       ???             ????????? Summary in present tense. Not capitalized. No period at the end.
  ???       ???
  ???       ????????? Component or service affected by the committed change.
  ???
  ????????? build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test
```
The `<type>` and `<subject>` fields are mandatory, the `(<scope>)` field is optional.

#### Type
Must be one of the following:

* **build**: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
* **chore**: Updating grunt tasks etc; no production code change 
* **ci**: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
* **docs**: Documentation only changes
* **feat**: A new feature
* **fix**: A bug fix
* **perf**: A code change that improves performance
* **refactor**: A code change that neither fixes a bug nor adds a feature
* **revert**: Reverting a previous commit
* **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
* **test**: Adding missing tests or correcting existing tests

#### Scope
The scope should be the name of component or service affected by the committed change.

#### Subject
The subject contains a succinct description of the change:

* use the imperative, present tense: "change" not "changed" nor "changes"
* don't capitalize the first letter
* no dot (.) at the end

#### Example
```
feat(maps_service): add user location endpoint
```

## Style Guide

### Python

The Python code in this project is automatically formatted using [Black](https://github.com/psf/black) and adheres to the [Black Code Style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html). Comments and docstrings must comform to the guidelines contained in the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).
 
# Authors

:busts_in_silhouette: **[Max Kiefer](https://github.com/Maxkie1), [Fabian Schneider](https://github.com/Fabian-Schneider01), [Gregor Boschmann](https://github.com/gregor434), [Laurin Tarta](https://github.com/lawrimon)**