from github import Github
import matplotlib.pyplot as plt
import os
import datetime

token = os.getenv('GITHUB_TOKEN')
repo_name = "Computer-Engineering-UdL/JointProject"

g = Github(token)
repo = g.get_repo(repo_name)

labels_count = {
    "back-end": 0,
    "bug": 0,
    "database": 0,
    "documentation": 0,
    "front-end": 0,
    "tests": 0,
    "wontfix": 0,
}


def get_date():
    """The format is: MX-WY-Report -> where X is number of month and Y is number of week"""
    now = datetime.datetime.now()
    month = now.strftime("%m")
    week_of_year = int(now.strftime("%U"))
    first_day_of_month = now.replace(day=1)
    week_of_first_day = int(first_day_of_month.strftime("%U"))
    week_of_month = week_of_year - week_of_first_day + 1
    return f"M{month}-W{week_of_month}-Report"


def count_labels() -> None:
    """Count the number of issues with each label"""
    for issue in repo.get_issues(state="all"):
        for label in issue.labels:
            if label.name in labels_count:
                labels_count[label.name] += 1


def generate_plot() -> None:
    """Generate a histogram of the number of issues with each label"""
    plt.figure(figsize=(10, 6))
    plt.bar(labels_count.keys(), labels_count.values())
    plt.xlabel('Labels')
    plt.ylabel('Number of Issues')
    plt.title(f'Histogram of Issues by Label - {get_date()}')
    plt.xticks(rotation=20)
    plt.yticks(range(0, max(labels_count.values()) + 1))
    plt.savefig("histogram_issues.png")


def main() -> None:
    count_labels()
    generate_plot()


if __name__ == '__main__':
    main()
