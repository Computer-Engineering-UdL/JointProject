import os
from radon.complexity import cc_visit
import Ishikawa_tools_generators.metrics.scripts.config as c
import matplotlib.pyplot as plt


def calculate_cyclomatic_complexity(directory):
    complexity_per_dir = {}
    total_complexity = 0

    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if d not in c.EXCLUDED_DIRS]
        dir_complexity = 0
        current_dir = os.path.basename(root)
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        code = f.read()
                    blocks = cc_visit(code)
                    for block in blocks:
                        complexity = block.complexity
                        dir_complexity += complexity
                        total_complexity += complexity
                except SyntaxError as e:
                    print(f"Syntax error in {filepath}: {e}")
                except Exception as e:
                    print(f"Error analyzing {filepath}: {e}")

        if dir_complexity > 0 and current_dir not in c.EXCLUDED_DIRS:
            complexity_per_dir[current_dir] = dir_complexity

    return complexity_per_dir, total_complexity


def create_complexity_chart(complexity_per_dir, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.bar(complexity_per_dir.keys(), complexity_per_dir.values(), color='#428FED')
    plt.ylabel('Complexity')
    plt.title('Cyclomatic Complexity by Subdirectory')
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
