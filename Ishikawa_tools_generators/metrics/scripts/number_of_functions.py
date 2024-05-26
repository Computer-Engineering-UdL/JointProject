import os
import ast
import Ishikawa_tools_generators.metrics.scripts.config as c


class FunctionCounter(ast.NodeVisitor):
    def __init__(self):
        self.function_count = 0

    def visit_FunctionDef(self, node):
        self.function_count += 1
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.function_count += 1
        self.generic_visit(node)


def calculate_number_of_functions(directory):
    functions_per_dir = {}
    total_functions = 0

    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if d not in c.EXCLUDED_DIRS]
        dir_functions = 0
        current_dir = os.path.basename(root)
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        code = f.read()
                    tree = ast.parse(code)
                    counter = FunctionCounter()
                    counter.visit(tree)
                    dir_functions += counter.function_count
                    total_functions += counter.function_count
                except Exception as e:
                    print(f"Error analyzing {filepath}: {e}")

        if dir_functions > 0 and current_dir not in c.EXCLUDED_DIRS:
            functions_per_dir[current_dir] = dir_functions

    return functions_per_dir, total_functions
