import os

import matplotlib.pyplot as plt

import Ishikawa_tools_generators.metrics.scripts.config as c


def get_filename(filename: str):
    return os.path.join(c.RESULTS_DIR, c.CHART_FILENAMES[filename])


def create_metric_chart(data, filename, title, ylabel):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.bar(data.keys(), data.values(), color='#428FED')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
