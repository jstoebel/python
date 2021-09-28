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

class RestAPI:
    def __init__(self, database=None):
        users = [
            User(data)
            for data in database["users"]
        ]
        self.database = {"users": users}

    def get(self, url, payload=None):
        if url == "/users":
            return json.dumps(self.get_users(payload))

    def get_users(self, payload=None):

        names_to_include = (
            json.loads(payload)["users"] 
            if payload
            else self.database["users"]
        )

        users = [
            user
            for user
            in self.database["users"]
            if user["name"] in names_to_include
        ]
        return {"users": users}

    def post(self, url, payload=None):
        if url == "/add":
            user_name = json.loads(payload)["user"]
            user = User(user_name)
            self.create_user(user)
            return json.dumps(user.data)

    def create_user(self, user):
        self.database["users"].append(user)

    def create_iou(self, iou):
        pass
