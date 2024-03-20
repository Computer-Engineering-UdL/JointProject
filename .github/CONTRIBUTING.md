# Contributing

### 1. Conventional Commits

In order to maintain a clean and organized code, this project uses
the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This means that every commit
message should follow the next pattern:

```
<type>[optional scope]: <description>
```

Where `<type>` can be one of the following:

- `chore`: Changes to the build process or auxiliary tools and libraries such as documentation generation.
- `ci`: Changes to our CI configuration files and scripts.
- `docs`: Changes to the documentation.
- `feat`: A new feature for the user, not a new feature for build script.
- `fix`: A bug fix for the user, not a fix to a build script.
- `perf`: A code change that improves performance.
- `refactor`: A code change that neither fixes a bug nor adds a feature.
- `revert`: Changes that revert a previous commit.
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semicolons, etc.).
- `test`: Adding missing tests or correcting existing tests.
- `security`: Changes that affect the security of the project.
- `translation`: Changes that affect the translation of the project.
- `changeset`: Changeset commit.
- `init`: Initial commit.
- `other`: Any other type of change.

### 2. Flake8

This project uses the [Flake8](https://flake8.pycqa.org/en/latest/) linter to check the code style. This means that
every pull request should pass the Flake8 checks in order to be merged.

In order to check the code style, run the following command:

```bash
flake8 .
```

To ignore any file or directory use the `--exclude` flag, for example:

```bash
flake8 . --exclude=venv,migrations
```


### 3. Prettier

This project also uses the [Prettier](https://prettier.io/) linter to check the code style. This means that
every pull request should pass the Prettier checks in order to be merged.

In order to check the code style, run the following command:

```bash
prettier --check .
```

Or if you want to format the code:

```bash
prettier --write .
```


### 3. Pull requests

Finally, it is strongly recommended to create a pull request using the [Conventional Comments](https://conventionalcomments.org/) specification.
