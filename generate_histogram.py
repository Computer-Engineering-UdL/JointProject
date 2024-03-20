from github import Github
import matplotlib.pyplot as plt
import os

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

for issue in repo.get_issues(state="all"):
    for label in issue.labels:
        if label.name in labels_count:
            labels_count[label.name] += 1

plt.bar(labels_count.keys(), labels_count.values())
plt.xlabel('Labels')
plt.ylabel('Number of Issues')
plt.title('Histogram of Issues by Label')
plt.xticks(rotation=45)
plt.savefig("histogram_issues.png")
