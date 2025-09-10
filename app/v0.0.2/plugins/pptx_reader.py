from pptx import Presentation

def read_file(filepath):
    try:
        prs = Presentation(filepath)
        text_runs = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text_runs.append(shape.text)
        return "\n".join(text_runs)
    except Exception as e:
        return f"[PPTX READ ERROR] {e}"

def after_write(filepath, content):
    if filepath.endswith(".pptx"):
        print(f"[PPTX PLUGIN] Wrote: {filepath}")