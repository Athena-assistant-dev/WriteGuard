import openpyxl
from plugins.base_plugin import WritePlugin

def after_write(filepath, content):
    if filepath.endswith(".xlsx"):
        print(f"[XLSX PLUGIN] Successfully wrote Excel file: {filepath}, size: {len(content)} bytes")

def read_file(filepath):
    try:
        wb = openpyxl.load_workbook(filepath)
        content = []
        for sheet in wb.worksheets:
            content.append(f"[Sheet: {sheet.title}]")
            for row in sheet.iter_rows(values_only=True):
                content.append("\t".join([str(cell) if cell is not None else "" for cell in row]))
        return "\n".join(content)
    except Exception as e:
        return f"[XLSX READ ERROR] {e}"

class XLSXWritePlugin(WritePlugin):
    def post_write(self, path, old_content, new_content):
        if path.endswith(".xlsx"):
            print(f"[XLSX PLUGIN] Wrote: {path}")
          
