import matplotlib.pyplot as plt
import numpy as np
from github import Github
import os
from datetime import datetime

token = os.getenv('GITHUB_TOKEN')
repo_name = "Computer-Engineering-UdL/JointProject"
sprint_milestone_title = "Sprint 3"

g = Github(token)
repo = g.get_repo(repo_name)


def get_sprint_milestone():
    milestones = repo.get_milestones()
    for milestone in milestones:
        if milestone.title == sprint_milestone_title:
            return milestone
    return None


def count_closed_issues(milestone):
    closed_issues_count_by_day = {}
    issues = repo.get_issues(milestone=milestone, state="closed")
    for issue in issues:
        if issue.closed_at:
            closed_day = issue.closed_at.date()
            closed_issues_count_by_day[closed_day] = closed_issues_count_by_day.get(closed_day, 0) + 1
    return closed_issues_count_by_day


def generate_burn_down_chart(milestone):
    total_issues = milestone.open_issues + milestone.closed_issues
    closed_issues_count_by_day = count_closed_issues(milestone)

    start_date = np.datetime64(milestone.created_at.date())
    end_date = np.datetime64(milestone.due_on.date())
    num_days = (end_date - start_date).astype('timedelta64[D]').astype(int) + 1
    sprint_days = [start_date + np.timedelta64(i, 'D') for i in range(num_days)]

    closed_issues_accumulated = np.zeros(num_days)
    for i, day in enumerate(sprint_days):
        day_as_date = day.astype('datetime64[D]').astype(datetime)
        closed_issues_accumulated[i] = closed_issues_accumulated[i - 1] + closed_issues_count_by_day.get(day_as_date, 0)

    sprint_days_np = np.array(sprint_days)
    remaining_work = total_issues - closed_issues_accumulated

    ideal_line = np.linspace(total_issues, 0, num_days)

    plt.figure(figsize=(10, 6))
    plt.plot(sprint_days_np.astype('datetime64[D]').astype(datetime), remaining_work, label='Actual', marker='o',
             color='red')
    plt.plot(sprint_days_np.astype('datetime64[D]').astype(datetime), ideal_line, label='Ideal', linestyle='--',
             color='blue')
    plt.title('Burn-down Chart')
    plt.xlabel('Date')
    plt.ylabel('Remaining Issues')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.savefig("burn_down_chart.png", format='png')


if __name__ == '__main__':
    milestone = get_sprint_milestone()
    if milestone:
        generate_burn_down_chart(milestone)
    else:
        print("Sprint Milestone not found.")
