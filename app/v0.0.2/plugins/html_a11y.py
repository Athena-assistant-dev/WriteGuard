from plugins.base_plugin import WritePlugin
from bs4 import BeautifulSoup

class HTMLValidator(WritePlugin):
    def validate(self, path, content):
        try:
            soup = BeautifulSoup(content.decode("utf-8"), "html.parser")
            if not soup.find():
                return False, "No HTML structure found"
            return True, ""
        except Exception as e:
            return False, str(e)