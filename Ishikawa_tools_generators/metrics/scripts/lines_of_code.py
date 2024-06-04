import os

import Ishikawa_tools_generators.metrics.scripts.config as c


def calculate_lines_of_code(directory):
    lines_per_dir = {}
    total_lines = 0

    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if d not in c.EXCLUDED_DIRS]
        dir_lines = 0
        current_dir = os.path.basename(root)
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        num_lines = len(lines)
                        dir_lines += num_lines
                        total_lines += num_lines
                except Exception as e:
                    print(f"Error analyzing {filepath}: {e}")

        if dir_lines > 0 and current_dir not in c.EXCLUDED_DIRS:
            lines_per_dir[current_dir] = dir_lines

    return lines_per_dir, total_lines
