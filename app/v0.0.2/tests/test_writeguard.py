import os
import unittest
from smart_safe_write import smart_safe_write

class TestWriteGuard(unittest.TestCase):
    def setUp(self):
        self.test_file = "/tmp/writeguard_test.txt"
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

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()