from PIL import Image
import pytesseract
from plugins.base_plugin import WritePlugin

class ImageReaderPlugin(WritePlugin):
    extensions = [".jpg", ".jpeg", ".png"]

    def read(self, filepath):
        try:
            img = Image.open(filepath)
            return pytesseract.image_to_string(img)
        except Exception as e:
            return f"[IMG READ ERROR] {e}"

    def post_write(self, filepath, old_content=None, new_content=None):
        print(f"[IMAGE PLUGIN] Wrote: {filepath}")

# For standalone execution/testing
if __name__ == "__main__":
    plugin = ImageReaderPlugin()