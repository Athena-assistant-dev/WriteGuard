from plugins.base_plugin import WritePlugin
from prance import ResolvingParser
from openapi_schema_validator import OAS30Validator
import os

class OpenAPIValidator(WritePlugin):
    extensions = [".yaml", ".yml"]

    def validate(self, path, content):
        if "openapi" not in os.path.basename(path).lower():
            return True, ""
        try:
            tmp_path = path + ".tmpcheck"
            with open(tmp_path, 'wb') as f:
                f.write(content)

            parser = ResolvingParser(tmp_path)
            spec = parser.specification

            validator = OAS30Validator(spec)
            validator.validate(spec)

            os.remove(tmp_path)
            return True, ""
        except Exception as e:
            return False, str(e)