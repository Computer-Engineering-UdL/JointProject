## Description



> [!IMPORTANT]
> Every pull request has to be reviewed by at least one maintainer.
> The pull request should also pass the following checks:
> - **Flake8**: Every pull request should pass the Flake8 checks in order to be merged. In order to check the code style, run the following command:
> ```bash
>   flake8 .
> ```
> - **DJHTML**: Every pull request should pass the DJHTML checks in order to be merged. In order to check the Django HTML files, run the following command:
> ```bash
>  djhtml .
> ```
> - **Run the project**: Every pull request must run the project without errors, specially the new features or changes.
> - **Tests**: Every pull request should pass the tests in order to be merged. In order to run the tests, run the following
> ```bash
> python manage.py test 
> ```

## Branch Deletion

- [ ] I confirm that after my PR is successfully merged, this branch can be deleted.

<!--Mark this checkbox once the pull request has been created-->

> [!NOTE]
> I understand that this pull request is strongly recommended to follow
> the [Conventional Comments](https://conventionalcomments.org/) specification.