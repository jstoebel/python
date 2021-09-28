import json

class User:
    def __init__(self, name) -> None:
        self.name = name

    @property
    def owes(self):
        return {}

    @property
    def owed_by(self):
        return {}

    @property
    def balance(self):
        return 0
    
    @property
    def data(self):
        return {
            "name": self.name,
            "owes": self.owes,
            "owed_by": self.owed_by,
            "balance": self.balance,
        }

class Database:
    """
    should use objects internally, but return dicts
    """
    def __init__(self, data) -> None:
        users = [
            User(data["name"])
            for data in data["users"]
        ]
        self.data = {"users": users}

    def get_users(self, names=None):

        names_to_include = (
            json.loads(names)["users"] 
            if names
            else self.data["users"]
        )

        users = [
            user.data
            for user
            in self.data["users"]
            if user.name in names_to_include
        ]
        return {"users": users}

    def create_user(self, user_name):
        user = User(user_name)
        self.data["users"].append(user)
        return user

class RestAPI:
    def __init__(self, database=None):
        self.database = Database(database)

    def get(self, url, payload=None):
        if url == "/users":
            return json.dumps(
                self.database.get_users(payload)
            )

    def post(self, url, payload=None):
        if url == "/add":
            user_name = json.loads(payload)["user"]
            user = self.database.create_user(user_name)
            return json.dumps(user.data)
        # if url == "/iou"

    def create_iou(self, iou):
        pass
