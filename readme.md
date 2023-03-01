<h1 align="center">Welcome to PDA :wave:</h1>

> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
  
## Description

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

## Documentation

- [Requirements Documentation](https://docs.google.com/document/d/1XM5byI64eKHCRa7sWAVpYF3cNTyOO1AmYaFOoii62lA/edit?usp=sharing)
- ...

## Usage

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

## Installation

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

## Commit Message Guidelines

Each commit message must conform to the [Commit Message Structure](#commit-structure) format.

### <a name="commit-structure"></a>Commit Message Structure
```
<type>(<scope>): <subject>
  │       │             │
  │       │             └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │       │
  │       └─⫸ Component or service affected by the committed change.
  │
  └─⫸ build|chore|ci|docs|feat|fix|perf|refactor
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

#### Scope
The scope should be the name of component or service affected by the committed change.

#### Subject
The subject contains a succinct description of the change:

* use the imperative, present tense: "change" not "changed" nor "changes"
* don't capitalize the first letter
* no dot (.) at the end

#### Example
```
feat(moodleRequest): add json support
```
 
## Authors

:busts_in_silhouette: **[Max Kiefer](https://github.com/Maxkie1), [Fabian Schneider](https://github.com/Fabian-Schneider01), [Gregor Boschmann](https://github.com/gregor434), [Laurin Tarta](https://github.com/lawrimon)**