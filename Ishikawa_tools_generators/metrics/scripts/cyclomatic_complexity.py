import os
from radon.complexity import cc_visit
import Ishikawa_tools_generators.metrics.scripts.config as c


def calculate_cyclomatic_complexity(directory):
    results = []
    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if d not in c.EXCLUDED_DIRS]
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        code = f.read()
                        blocks = cc_visit(code)
                        for block in blocks:
                            results.append(f"{filepath}: {block.name} - Complexity {block.complexity}")
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    return results


def save_results(results, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as file:
        for result in results:
            file.write(result + "\n")


if __name__ == "__main__":
    directory = os.path.abspath(os.path.join(__file__, '../../../../'))
    output_file = os.path.abspath(os.path.join(__file__, '../../results/cyclomatic_results.txt'))
    results = calculate_cyclomatic_complexity(directory)
    save_results(results, output_file)
    print(f"Results saved to {output_file}")
