import os

EXCLUDED_DIRS = {'__pycache__', 'migrations', 'data', 'logs', 'models', 'notebooks', 'src', 'tests', 'tmp', 'venv', '.venv'}

FONT = 'Arial'

REPORT_FILE_NAME = "Project_Metrics_Report.pdf"

SOURCE_ROOT = os.path.abspath(os.path.join(__file__, '../../../'))

RESULTS_DIR = os.path.abspath(os.path.join(__file__, '../results'))
