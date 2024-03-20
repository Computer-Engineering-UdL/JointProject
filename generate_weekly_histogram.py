from github import Github
import matplotlib.pyplot as plt
import datetime
from generate_histogram import token, repo_name
import argparse

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


# This is the state of the issues that this is gathering:
# "all" - All issues assigned to the repository
# "open" - Open issues assigned to the repository
# "closed" - Closed issues assigned to the repository
def count_labels(state="open") -> None:
    """Count the number of issues with each label"""
    for issue in repo.get_issues(state=state):
        for label in issue.labels:
            if label.name in labels_count:
                labels_count[label.name] += 1


def generate_plot(state="open") -> None:
    """Generate a histogram of the number of issues with each label"""
    plt.figure(figsize=(10, 6))
    plt.bar(labels_count.keys(), labels_count.values())
    plt.xlabel('Labels')
    plt.ylabel(f'Number of Issues ({state})')
    plt.title(f'Histogram of Issues ({state}) by Label - {get_date()}')
    plt.xticks(rotation=20)
    plt.yticks(range(0, max(labels_count.values()) + 1))
    plt.savefig(f"histogram_issues_{state}.png")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Generate a histogram of the number of issues with each label')
    parser.add_argument('--state', type=str,
                        help='The state of the issues that this is gathering')
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.state:
        count_labels(state=args.state)
        generate_plot(state=args.state)
    else:
        count_labels()
        generate_plot()


if __name__ == '__main__':
    main()
