import ast
import os

import Ishikawa_tools_generators.metrics.scripts.config as c


class NestingDepthVisitor(ast.NodeVisitor):
    def __init__(self):
        self.max_depth = 0
        self.current_depth = 0

    def visit_FunctionDef(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_If(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_For(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_While(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_With(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1


def calculate_nesting_depth(directory):
    depth_per_dir = {}
    total_depth = 0

    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if d not in c.EXCLUDED_DIRS]
        dir_depth = 0
        current_dir = os.path.basename(root)
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        code = f.read()
                    tree = ast.parse(code)
                    visitor = NestingDepthVisitor()
                    visitor.visit(tree)
                    file_depth = visitor.max_depth
                    dir_depth += file_depth
                    total_depth += file_depth
                except Exception as e:
                    print(f"Error analyzing {filepath}: {e}")

        if dir_depth > 0 and current_dir not in c.EXCLUDED_DIRS:
            depth_per_dir[current_dir] = dir_depth

    return depth_per_dir, total_depth
