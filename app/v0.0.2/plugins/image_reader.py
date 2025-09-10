from PIL import Image
import pytesseract

def read_file(filepath):
    try:
        img = Image.open(filepath)
        return pytesseract.image_to_string(img)
    except Exception as e:
        return f"[IMG READ ERROR] {e}"

def after_write(filepath, content):
    if any(filepath.endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
        print(f"[IMAGE PLUGIN] Wrote: {filepath}")