class User:

    def __init__(
        self, 
        username:str, 
        ip_addr: str, 
        last_update_timestamp = 0
    ):
        self.username = username
        self.ip_addr = ip_addr
        self.last_update_timestamp = last_update_timestamp

    