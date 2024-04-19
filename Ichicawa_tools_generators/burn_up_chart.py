import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from burn_down_chart import get_sprint_milestone, count_closed_issues


def generate_burn_up_chart(milestone):
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

    plt.figure(figsize=(10, 6))
    plt.plot(sprint_days_np.astype('datetime64[D]').astype(datetime), closed_issues_accumulated, label='Completed Work',
             marker='o', color='green')
    plt.hlines(total_issues, sprint_days[0].astype(datetime), sprint_days[-1].astype(datetime), colors='blue',
               linestyles='dashed', label='Total Planned Work')
    plt.title('Burn-up Chart')
    plt.xlabel('Date')
    plt.ylabel('Completed Issues')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("burn_up_chart.png", format='png')


if __name__ == '__main__':
    milestone = get_sprint_milestone()
    if milestone:
        generate_burn_up_chart(milestone)
    else:
        print("Sprint Milestone not found.")
