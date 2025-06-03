from time import time_ns

class Message:
    
    def __init__(self, text, user, timestamp = None):
        self.text = text
        self.user = user
        self.timestamp = timestamp if timestamp else time_ns()


    def to_dict(self):
        return {'text': self.text, 'user': self.user}


    @staticmethod
    def from_dict(d):
        return Message(d['text'], d['user'])
