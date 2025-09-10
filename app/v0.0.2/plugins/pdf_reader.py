import fitz  # PyMuPDF
from plugins.base_plugin import WritePlugin

def after_write(filepath, content):
    if filepath.endswith(".pdf"):
        size = len(content) if content else 0
        print(f"[PDF PLUGIN] Successfully wrote PDF file: {filepath}, size: {size} bytes")

def read_file(filepath):
    try:
        doc = fitz.open(filepath)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    except Exception as e:
        return f"[PDF READ ERROR] {e}"

class PDFWritePlugin(WritePlugin):
    def post_write(self, path, old_content, new_content):
        if path.endswith(".pdf"):
            print(f"[PDF PLUGIN] Wrote: {path}")
