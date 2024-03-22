# How to use histogram generator workflow

## Installation

1. Go to the workflows folder in your repository. This can be found at `.github/workflows/`. If it does not exist,
   create it.
2. Create 2 new files in the workflows folder, one for the weekly report and one for the general report. For example:
    - `histogram_weekly_generator.yml`
    - `histogram_general_report.yml`
3. Copy the content of the files in this folder to the files you just created.
4. In the project root folder, create two new files:
    - `generate_histogram.py`
    - `generate_weekly_histogram.py`
5. Copy the content of the files in this folder to the files you just created.
6. Change the repository name in the `generate_histogram.py` file to the name of your repository. For example:
   ```python
   repository = "username/repo_name" # Replace this
   ```
7. Create 
