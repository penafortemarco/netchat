class Message:
    
    def __init__(self, text, user, timestamp):
        self.text = text
        self.user = user
        self.timestamp = timestamp


    def to_dict(self):
        return {'text': self.text, 'user': self.user, 'timestamp': self.timestamp}


    @staticmethod
    def from_dict(d):
        return Message(d['text'], d['user'], d['timestamp'])
