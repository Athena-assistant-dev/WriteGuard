from plugins.base_plugin import WritePlugin
from html.parser import HTMLParser
import logging

logger = logging.getLogger(__name__)

class HTMLValidator(WritePlugin):
    extensions = [".html", ".htm"]

    def validate(self, path, content):
        try:
            parser = HTMLParser()
            parser.feed(content.decode("utf-8"))
            return True, ""
        except Exception as e:
            logger.warning(f"HTML validation failed for {path}: {e}")
            return False, str(e)