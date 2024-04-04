# How to use histogram generator workflow

This workflow generates a histogram of the issues in your repository. It counts the number of open and closed issues and
creates a histogram of the issues by label. The workflow is divided into two parts: a weekly report and a general
report.

The weekly report is automatically triggered every Sunday at 23:59 and shows the issues that have been opened and closed
**only during that week**. The general report can be manually triggered on the Actions tab on your repository, and shows
all the issues that have been opened during the whole project development. The reports are saved as png files in the
artifacts section of the workflow run.

## Installation

1. Go to the **workflows folder** in your repository. This can be found at `.github/workflows/`. If it does not exist,
   create it.
2. Create **two new files** in the workflows folder, one for the weekly report and one for the general report. For
   example:
    - `histogram_weekly_generator.yml`
    - `histogram_general_report.yml`
3. **Copy the content** of the files in this folder to the files you just created.
4. In the project root folder, **create two new files**:
    - `generate_histogram.py`
    - `generate_weekly_histogram.py`
5. **Copy the content** of the files in this folder to the files you just created.
6. **Change the repository name** in the `generate_histogram.py` file to the name of your repository. For example:
   ```python
   repo_name = "username/repo_name" # Replace this
   ```
7. Go to
   your `profile settings -> Scroll down to Developer settings -> Personal access tokens -> Tokens (classic) -> Generate new token -> Generate new token (classic)`.
   Name the token **`MY_GITHUB_TOKEN`**, select the `repo` scope and set an expiration date of 3 months or more. **Copy
   the
   token and save it**, once you leave that page you will never see that token secret again.
8. Go to your `repository settings -> Secrets and variables -> New repository secret -> Name the secret:
   `**`MY_GITHUB_TOKEN`** `-> Paste the token you copied in the previous step -> Add secret`.

## Usage

### Weekly report

This workflow it automatically triggered every Sunday at 23:59. Then after the workflow is finished, it will create a
png file in the artifacts section of that workflow run. This can be found on
your `repository -> Actions -> Weekly Report - Histogram of Issues (open and closed) -> Scroll down to Artifacts`.

This workflow can be manually triggered on Actions tab on your repository.

### General report

This workflow is **NOT** automatically triggered. It can be manually triggered on the Actions tab on your repository. Go
to the `Weekly Report - Histogram of Issues (all)` and run the workflow.

Thanks, _GROUP-C_.