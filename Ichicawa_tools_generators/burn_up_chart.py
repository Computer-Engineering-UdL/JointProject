import matplotlib.pyplot as plt
import numpy as np
from github import Github
import os

# Configuración inicial
token = os.getenv('GITHUB_TOKEN')
repo_name = "Computer-Engineering-UdL/JointProject"
project_name = "Sprint 1 - Kanban"
total_issues_at_start = 20

g = Github(token)
repo = g.get_repo(repo_name)


def count_done_issues_in_project() -> int:
    projects = repo.get_projects()
    for project in projects:
        if project.name == project_name:
            columns = project.get_columns()
            for column in columns:
                if column.name == "Done":
                    cards = column.get_cards()
                    done_issues_count = sum(1 for card in cards if card.get_content() is not None)
                    return done_issues_count
    return 0


def generate_burn_down_chart(done_issues_count: int) -> None:
    days = np.arange(1, 24)
    ideal_work = np.linspace(total_issues_at_start, 0, len(days))
    actual_work = np.linspace(total_issues_at_start, total_issues_at_start - done_issues_count, len(days))

    plt.figure(figsize=(10, 6))
    plt.plot(days, ideal_work, label='Ideal', linestyle='--', color='blue')
    plt.plot(days, actual_work, label='Actual', marker='o', color='red')
    plt.title('Burn-down Graph')
    plt.xlabel('Days of the Sprint')
    plt.ylabel('Remaining Work (issues)')
    plt.legend()
    plt.grid(True)
    plt.savefig("/mnt/data/burn_down_chart.png", format='png')


if __name__ == '__main__':
    done_issues_count = count_done_issues_in_project()
    generate_burn_down_chart(done_issues_count)
