import os
from fpdf import FPDF
from datetime import datetime
import Ishikawa_tools_generators.metrics.scripts.config as c
from Ishikawa_tools_generators.metrics.scripts import cyclomatic_complexity


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
        self.cell(-139, 10, c.PROJECT_NAME, 0, 0, 'C', link=c.PROJECT_LINK)
        self.set_text_color(0)
        self.set_font(c.FONT, 'I', 8)


def create_pdf(pdf, total_complexity, chart_filename):
    pdf.add_page()
    pdf.set_font(c.FONT, size=12)
    pdf.image(chart_filename, x=10, y=30, w=190)
    pdf.ln(105)
    pdf.set_font(c.FONT, 'B', 12)
    pdf.cell(0, 10, f'Total Cyclomatic Complexity: {total_complexity}', 0, 1, 'C')

    pdf.set_title(c.METADATA['title'])
    pdf.set_author(c.METADATA['author'])
    pdf.set_creator(c.METADATA['creator'])
    pdf.set_subject(c.METADATA['subject'])
    pdf.set_keywords(c.METADATA['keywords'])


if __name__ == "__main__":
    pdf = PDF()
    pdf.alias_nb_pages()
    complexity_per_dir, total_complexity = cyclomatic_complexity.calculate_cyclomatic_complexity(c.SOURCE_ROOT)
    cyclomatic_complexity.create_complexity_chart(complexity_per_dir, c.CHART_FILENAME)
    create_pdf(pdf, total_complexity, c.CHART_FILENAME)
    pdf.output(c.REPORT_FILE_NAME)
    print(f"PDF generated and saved as {c.REPORT_FILE_NAME}")
