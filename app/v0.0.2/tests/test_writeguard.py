import os
import unittest
import io
from contextlib import redirect_stdout
from smart_safe_write import smart_safe_write

class TestWriteGuard(unittest.TestCase):
    def setUp(self):
        self.test_file = "/tmp/writeguard_test.txt"
        self.docx_file = "/tmp/writeguard_test.docx"
        self.initial_content = b"Initial content"
        with open(self.test_file, "wb") as f:
            f.write(self.initial_content)

    def test_dry_run_preview(self):
        new_content = "Changed content"
        result = smart_safe_write(
            filepath=self.test_file,
            content_bytes=new_content.encode("utf-8"),
            dry_run=True,
            preview=True,
            reason="test"
        )
        self.assertIn("diff", result)
        self.assertEqual(result.get("status"), "dry_run")

    def test_docx_plugin_is_called(self):
        # Ensure the file doesn't exist from a previous run
        if os.path.exists(self.docx_file):
            os.remove(self.docx_file)

        # Create a valid, empty docx file content in memory
        from docx import Document
        import io
        document = Document()
        doc_io = io.BytesIO()
        document.save(doc_io)
        new_content_bytes = doc_io.getvalue()

        f = io.StringIO()
        with redirect_stdout(f):
            smart_safe_write(
                filepath=self.docx_file,
                content_bytes=new_content_bytes
            )
        output = f.getvalue()
        self.assertIn("[DOCX PLUGIN] Wrote:", output)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.docx_file):
            os.remove(self.docx_file)

if __name__ == "__main__":
    unittest.main()