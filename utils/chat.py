from .message import Message

class Chat:

    def __init__(self, state: list[Message] = None):
        self.state = state if state is not None else []

    def add_msg(self, msg: Message):
        if Message is None: 
            raise ValueError()
        
        self.state.append(msg)

    