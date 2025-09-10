from plugins.base_plugin import WritePlugin
import toml

class TOMLValidator(WritePlugin):
    extensions = [".toml"]

    def validate(self, path, content):
        try:
            toml.loads(content.decode("utf-8"))
            return True, ""
        except Exception as e:
            return False, str(e)