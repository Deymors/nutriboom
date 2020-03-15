class Response:
    def __init__(self, stage, contactable, content, is_message_valid):
        self.stage = stage
        self.contactable = contactable
        self.content = content
        self.is_message_valid = is_message_valid
