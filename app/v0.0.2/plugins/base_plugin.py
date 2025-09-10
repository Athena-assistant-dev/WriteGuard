class WritePlugin:
    def validate(self, path: str, content: bytes) -> (bool, str):
        """
        Validate file content. Return (True, "") if valid, otherwise (False, "error message").
        """
        raise NotImplementedError

    def post_write(self, path: str, old_content: bytes, new_content: bytes):
        """
        Optional hook to execute after a successful write.
        """
        pass