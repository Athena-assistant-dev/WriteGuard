import os
from fpdf import FPDF
from PIL import Image

def write_pdf(pdf_path, text_lines, images=None, table_data=None):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add text lines
    for line in text_lines:
        pdf.multi_cell(0, 10, txt=line)

    # Add simple table from 2D list
    if table_data:
        pdf.ln(5)
        col_widths = [40] * len(table_data[0])
        for row in table_data:
            for i, cell in enumerate(row):
                pdf.cell(col_widths[i], 10, str(cell), border=1)
            pdf.ln(10)

    # Add images
    if images:
        for img_path in images:
            if os.path.isfile(img_path):
                try:
                    cover = Image.open(img_path)
                    width, height = cover.size
                    aspect = width / height
                    new_width = 100
                    new_height = int(new_width / aspect)
                    pdf.image(img_path, x=(210-new_width)/2, y=None, w=new_width, h=new_height)
                    pdf.ln(10)
                except Exception as e:
                    print(f"Failed to add image {img_path}: {e}")

    pdf.output(pdf_path)
    return pdf_path

def main():
    # Example usage
    lines = ["Sample Enhanced PDF", "", "Includes table and image"]
    table = [["Name", "Role", "Status"], ["Alice", "Engineer", "Active"], ["Bob", "Designer", "Inactive"]]
    write_pdf("example.pdf", lines, images=["example.jpg"], table_data=table)

if __name__ == "__main__":
    main()