import os
import re
import Ishikawa_tools_generators.metrics.scripts.config as c


def calculate_number_of_comments(directory):
    comments_per_dir = {}
    total_comments = 0

    comment_pattern = re.compile(r'#.*')

    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if d not in c.EXCLUDED_DIRS]
        dir_comments = 0
        current_dir = os.path.basename(root)
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        code = f.read()
                    comments = comment_pattern.findall(code)
                    num_comments = len(comments)
                    dir_comments += num_comments
                    total_comments += num_comments
                except Exception as e:
                    print(f"Error analyzing {filepath}: {e}")

        if dir_comments > 0 and current_dir not in c.EXCLUDED_DIRS:
            comments_per_dir[current_dir] = dir_comments

    return comments_per_dir, total_comments
