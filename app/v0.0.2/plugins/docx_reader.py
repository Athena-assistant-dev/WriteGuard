from docx import Document

def read_docx(filepath):
    try:
        from docx import Document
        doc = Document(filepath)
        return "\n".join(para.text for para in doc.paragraphs)
    except Exception as e:
        return f"[DOCX READ ERROR] {e}"

def after_write(filepath, content=None):
    if filepath.endswith(".docx"):
        print(f"[DOCX PLUGIN] Wrote: {filepath}")

if __name__ == "__main__":
    print(read_file("sample.docx"))