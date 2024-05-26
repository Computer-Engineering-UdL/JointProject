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


def create_pdf(pdf, complexity_per_dir, total_complexity):
    page_width = 210
    table_width = 160
    col_widths = [100, 60]
    table_start = (page_width - table_width) / 2

    pdf.add_page()
    pdf.set_font(c.FONT, size=12)
    pdf.cell(200, 10, txt=f'Cyclomatic Complexity by Subdirectory', ln=True)
    pdf.ln(3)

    pdf.set_x(table_start)
    for dir, complexity in sorted(complexity_per_dir.items()):
        pdf.cell(col_widths[0], 10, txt=f'{dir}', border=1)
        pdf.cell(col_widths[1], 10, txt=f'Complexity: {complexity}', border=1)
        pdf.ln(10)
        pdf.set_x(table_start)

    pdf.ln(10)
    pdf.set_font(c.FONT, 'B', 12)
    pdf.cell(200, 10, txt=f'Total Cyclomatic Complexity: {total_complexity}', ln=True)


if __name__ == "__main__":
    pdf = PDF()
    pdf.alias_nb_pages()
    complexity_per_dir, total_complexity = cyclomatic_complexity.calculate_cyclomatic_complexity(c.SOURCE_ROOT)
    create_pdf(pdf, complexity_per_dir, total_complexity)
    pdf.output(c.REPORT_FILE_NAME)
    print(f"PDF generated and saved as {c.REPORT_FILE_NAME}")
