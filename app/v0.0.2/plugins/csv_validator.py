from plugins.base_plugin import WritePlugin
import csv
import io

class CSVValidator(WritePlugin):
    extensions = [".csv"]

    def validate(self, path, content):
        try:
            sample = content.decode("utf-8")
            csv.reader(io.StringIO(sample))
            return True, ""
        except Exception as e:
            return False, str(e)