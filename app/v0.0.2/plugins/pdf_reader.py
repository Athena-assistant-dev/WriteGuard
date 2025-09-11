import fitz  # PyMuPDF
from plugins.base_plugin import WritePlugin

class PdfReaderPlugin(WritePlugin):
    extensions = [".pdf"]

    def read(self, filepath):
        try:
            doc = fitz.open(filepath)
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            return text
        except Exception as e:
            return f"[PDF READ ERROR] {e}"

    def post_write(self, filepath, old_content=None, new_content=None):
        size = len(new_content) if new_content else 0
        print(f"[PDF PLUGIN] Successfully wrote PDF file: {filepath}, size: {size} bytes")

# For standalone execution/testing
if __name__ == "__main__":
    plugin = PdfReaderPlugin()
