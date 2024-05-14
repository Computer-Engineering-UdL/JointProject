import os
import pandas as pd
from datetime import datetime, timedelta
from github import Github
import matplotlib.pyplot as plt
from generate_histogram import repo_name


def generate_weekly_report(github_token) -> None:
    g = Github(github_token)
    repo = g.get_repo(f"{repo_name}")

    # Get all issues for the repo
    issues = repo.get_issues(state='all')

    # Dictionary to store the counts of opened and closed issues for each day of the week
    weekly_counts = {
        'Monday': {'opened': 0, 'closed': 0},
        'Tuesday': {'opened': 0, 'closed': 0},
        'Wednesday': {'opened': 0, 'closed': 0},
        'Thursday': {'opened': 0, 'closed': 0},
        'Friday': {'opened': 0, 'closed': 0},
        'Saturday': {'opened': 0, 'closed': 0},
        'Sunday': {'opened': 0, 'closed': 0}
    }

    def get_day_of_week(date_str) -> str:
        date = datetime.strptime(date_str[:10], '%Y-%m-%d')
        return date.strftime('%A')

    current_date = datetime.now()
    one_week_ago = current_date - timedelta(days=7)

    for issue in issues:
        created_at = issue.created_at.replace(tzinfo=None)
        if created_at >= one_week_ago:
            day_of_week = get_day_of_week(str(created_at))
            weekly_counts[day_of_week]['opened'] += 1

        if issue.closed_at:
            closed_at = issue.closed_at.replace(tzinfo=None)
            if closed_at >= one_week_ago:
                day_of_week = get_day_of_week(str(closed_at))
                weekly_counts[day_of_week]['closed'] += 1

    # Extract all the data from the dictionary
    dias = list(weekly_counts.keys())
    abiertas = [weekly_counts[d]["opened"] for d in weekly_counts]
    cerradas = [weekly_counts[d]["closed"] for d in weekly_counts]

    data = {
        "Day of the week": dias,
        "Opened": abiertas,
        "Closed": cerradas
    }

    # Create the table
    df = pd.DataFrame(data)
    fig, ax = plt.subplots()
    ax.axis('off')
    tabla = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     cellLoc='center',
                     loc='center')
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(12)
    tabla.scale(1.5, 1.5)
    plt.savefig('weekly_table.png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.show()

    current_date = datetime.now()
    one_week_ago = current_date - timedelta(days=7)


github_token = os.getenv('GITHUB_TOKEN')

generate_weekly_report(github_token)
