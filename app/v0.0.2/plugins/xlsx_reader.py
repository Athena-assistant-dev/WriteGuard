import openpyxl
from plugins.base_plugin import WritePlugin

class XlsxReaderPlugin(WritePlugin):
    extensions = [".xlsx"]

    def read(self, filepath):
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

    def post_write(self, filepath, old_content=None, new_content=None):
        size = len(new_content) if new_content else 0
        print(f"[XLSX PLUGIN] Successfully wrote Excel file: {filepath}, size: {size} bytes")

# For standalone execution/testing
if __name__ == "__main__":
    plugin = XlsxReaderPlugin()
