from .user import User

class Users:

    def __init__(self, users: list[User] = None):
        self.users = users if users is not None else []

    def get_user_by_username(self, username: str) -> User:
        return next((u for u in self.users if u.username == username), None)
    
    def get_user_by_ip(self, ip_addr: str) -> User:
        return next((u for u in self.users if u.ip_addr == ip_addr), None)
    

    def add_user(self, user: User) -> None: 
        self.users.append(user)

    def print_all_users(self) -> None:
        for user in self.users:
            print("---")
            print(user.username)
            print(user.ip_addr)
            print("---")

