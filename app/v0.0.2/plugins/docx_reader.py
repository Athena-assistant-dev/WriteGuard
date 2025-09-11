from docx import Document
from plugins.base_plugin import WritePlugin

class DocxReaderPlugin(WritePlugin):
    extensions = [".docx"]

    def read(self, filepath):
        try:
            doc = Document(filepath)
            return "\n".join(para.text for para in doc.paragraphs)
        except Exception as e:
            return f"[DOCX READ ERROR] {e}"

    def post_write(self, filepath, old_content=None, new_content=None):
        print(f"[DOCX PLUGIN] Wrote: {filepath}")

# For standalone execution/testing
if __name__ == "__main__":
    plugin = DocxReaderPlugin()
    # Assuming a sample.docx exists for testing
    # print(plugin.read("sample.docx"))