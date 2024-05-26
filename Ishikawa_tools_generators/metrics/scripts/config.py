import os

EXCLUDED_DIRS = {
    '__pycache__',
    'migrations',
    'data',
    'logs',
    'models',
    'notebooks',
    'src',
    'tests',
    'tmp',
    'venv',
    '.venv',
    'scripts',
    'metrics'
}

FONT = 'Arial'

DATE_FORMAT = "%d-%m-%Y"

REPORT_FILE_NAME = "Project_Metrics_Report.pdf"

SOURCE_ROOT = os.path.abspath(os.path.join(__file__, '../../../../'))

RESULTS_DIR = os.path.abspath(os.path.join(__file__, '../results'))

CHART_FILENAMES = {
    'cyclomatic': 'cyclomatic_complexity_chart.png',
    'lines_of_code': 'lines_of_code_chart.png'
}

# Chart titles and y-axis labels
CHART_TITLES = [
    ['Cyclomatic Complexity by Subdirectory Metric', 'Complexity'],
    ['Lines of Code by Subdirectory Metric', 'Lines of Code']
]

PROJECT_NAME = 'Joint Project'

PROJECT_LINK = 'https://github.com/Computer-Engineering-UdL/JointProject/tree/main'

METADATA = {
    'title': 'Project Complexity Report',
    'author': 'Aniol0012',
    'creator': PROJECT_NAME,
    'subject': 'Metrics analysis of the project',
    'keywords': 'software, complexity, cyclomatic, code analysis'
}
