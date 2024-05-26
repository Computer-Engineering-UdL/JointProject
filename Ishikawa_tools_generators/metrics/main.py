import os
from fpdf import FPDF
from datetime import datetime
import Ishikawa_tools_generators.metrics.scripts.config as c
from Ishikawa_tools_generators.metrics.scripts import cyclomatic_complexity, lines_of_code
from Ishikawa_tools_generators.metrics import utils as u


class PDF(FPDF):
    def header(self):
        self.set_font(c.FONT, 'B', 12)
        self.cell(0, 10, c.REPORT_FILE_NAME.rstrip('.pdf').replace('_', ' '), 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font(c.FONT, 'I', 8)
        if self.page_no() > 1:
            page_str = f'Page {self.page_no()} | '
        else:
            page_str = ''
        date_str = datetime.now().strftime(c.DATE_FORMAT)
        footer_text = f'{page_str}Generated on {date_str} | '
        self.cell(0, 10, footer_text, 0, 0, 'C')

        self.set_text_color(66, 143, 237)
        self.set_font(c.FONT, 'I', 8)
        self.cell(-self.get_string_width(footer_text), 10, c.PROJECT_NAME, 0, 0, 'C', link=c.PROJECT_LINK)
        self.set_text_color(0)
        self.set_font(c.FONT, 'I', 8)


def create_pdf(pdf, total_complexity, total_lines):
    pdf.add_page()
    pdf.set_font(c.FONT, size=12)

    # Cyclomatic Complexity
    pdf.image(os.path.join(c.RESULTS_DIR, c.CHART_FILENAMES['cyclomatic']), x=10, y=30, w=190)
    pdf.ln(105)
    pdf.set_font(c.FONT, 'B', 12)
    pdf.cell(0, 10, f'Total Cyclomatic Complexity: {total_complexity}', 0, 1, 'C')

    # Lines of Code
    pdf.image(os.path.join(c.RESULTS_DIR, c.CHART_FILENAMES['lines_of_code']), x=10, y=150, w=190)
    pdf.ln(105)
    pdf.set_font(c.FONT, 'B', 12)
    pdf.cell(0, 10, f'Total Lines of Code: {total_lines}', 0, 1, 'C')

    # Metadata
    pdf.set_title(c.METADATA['title'])
    pdf.set_author(c.METADATA['author'])
    pdf.set_creator(c.METADATA['creator'])
    pdf.set_subject(c.METADATA['subject'])
    pdf.set_keywords(c.METADATA['keywords'])


def create_charts():
    # Run metrics scripts
    complexity_per_dir, total_complexity = cyclomatic_complexity.calculate_cyclomatic_complexity(c.SOURCE_ROOT)
    lines_per_dir, total_lines = lines_of_code.calculate_lines_of_code(c.SOURCE_ROOT)

    # Create charts

    ## Cyclomatic Complexity
    filename = os.path.join(c.RESULTS_DIR, c.CHART_FILENAMES['cyclomatic'])
    u.create_metric_chart(complexity_per_dir, filename,
                          'Cyclomatic Complexity by Subdirectory Metric',
                          'Complexity'
                          )

    ## Lines of Code
    filename = os.path.join(c.RESULTS_DIR, c.CHART_FILENAMES['lines_of_code'])
    u.create_metric_chart(lines_per_dir, filename, 'Lines of Code by Subdirectory Metric', 'Lines of Code')

    return total_complexity, total_lines


if __name__ == "__main__":
    pdf = PDF()
    pdf.alias_nb_pages()
    total_complexity, total_lines = create_charts()
    create_pdf(pdf, total_complexity, total_lines)
    pdf.output(c.REPORT_FILE_NAME)
    print(f"PDF generated and saved as {c.REPORT_FILE_NAME}")
