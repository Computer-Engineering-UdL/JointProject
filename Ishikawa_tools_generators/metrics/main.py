import os
from fpdf import FPDF
import Ishikawa_tools_generators.metrics.scripts.config as c
from Ishikawa_tools_generators.metrics.scripts import cyclomatic_complexity


class PDF(FPDF):
    def header(self):
        self.set_font(c.FONT, 'B', 12)
        self.cell(0, 10, c.REPORT_FILE_NAME.rstrip('.pdf'), 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font(c.FONT, 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def add_complexity_by_directory_to_pdf(pdf, results_dir):
    complexity_per_dir = {}
    total_complexity = 0

    for root, dirs, files in os.walk(results_dir, topdown=True):
        dir_complexity = 0
        for file in files:
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    for line in f:
                        if "Complexity" in line:
                            complexity = int(line.split("Complexity ")[1])
                            dir_complexity += complexity
                            total_complexity += complexity

        if dir_complexity > 0:
            complexity_per_dir[os.path.basename(root)] = dir_complexity

    pdf.add_page()
    pdf.set_font(c.FONT, size=12)
    pdf.cell(200, 10, txt='Complexity by Subdirectory', ln=True, align='C')
    for dir, complexity in complexity_per_dir.items():
        pdf.cell(200, 10, txt=f'{dir}: {complexity}', ln=True)
    pdf.cell(200, 10, txt=f'Total Complexity: {total_complexity}', ln=True)


if __name__ == "__main__":
    directory = os.path.abspath(os.path.join(__file__, '../../../'))
    output_file = os.path.abspath(os.path.join(__file__, '../../results/cyclomatic_results.txt'))
    results = cyclomatic_complexity.calculate_cyclomatic_complexity(directory)
    cyclomatic_complexity.save_results(results, output_file)

    pdf = PDF()
    pdf.alias_nb_pages()
    results_dir = os.path.abspath(os.path.join(__file__, '../../results'))
    add_complexity_by_directory_to_pdf(pdf, results_dir)
    pdf.output(c.REPORT_FILE_NAME)
