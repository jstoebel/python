from collections import defaultdict
from functools import reduce
import json

class User:
    def __init__(self, name) -> None:
        self.name = name
        self.owes = defaultdict(float) 
        self.owed_by = defaultdict(float)

    @property
    def balance(self):
        credits = [
            amount
            for _name, amount
            in self.owed_by.items()
        ]

        debts = [
            amount
            for _name, amount
            in self.owes.items()
        ]

        return sum(credits) - sum(debts)
    
    @property
    def data(self):
        return {
            "name": self.name,
            "owes": self.owes,
            "owed_by": self.owed_by,
            "balance": self.balance,
        }

    def add_debt(self, lender_name, amount):
        self.owes[lender_name] += amount

    def add_credit(self, borrower_name, amount):
        self.owed_by[borrower_name] += amount

class Database:
    """
    should use objects internally, but return dicts
    """
    def __init__(self, data) -> None:
        self.users = [
            User(data["name"])
            for data in data["users"]
        ]

    def get_users(self, names_to_include=None):
        return sorted(
            (
                user
                for user
                in self.users
                if user.name in names_to_include
            ),
            key=(lambda user: user.name)
        )

    def create_user(self, user_name):
        user = User(user_name)
        self.users.append(user)
        return user

    def create_iou(self, iou):
        """
        example: {"lender": "Adam", "borrower": "Bob", "amount": 3.0}
        """
        amount = iou["amount"]
        lender = next(
            user
            for user in self.users
            if user.name == iou["lender"]
        )
        

        borrower = next(
            user
            for user in self.users
            if user.name == iou["borrower"]
        )

        lender.add_credit(borrower_name=borrower.name, amount=amount)
        borrower.add_debt(lender_name=lender.name, amount=amount)
        return self.get_users([lender.name, borrower.name])


class RestAPI:
    def __init__(self, database=None):
        self.database = Database(database)

    def get(self, url, payload=None):
        if url == "/users":
            return self.get_users(payload)

    def get_users(self, payload):
        if payload:
            names_to_include = json.loads(payload)["users"]
            users = self.database.get_users(names_to_include)
        else:
            users = self.database.get_users()

        return json.dumps({
            "users": [u.data for u in users]
        })

    def post(self, url, payload=None):
        if url == "/add":
            user_name = json.loads(payload)["user"]
            user = self.database.create_user(user_name)
            return json.dumps(user.data)
        if url == "/iou":
            iou_payload = json.loads(payload)
            users = self.database.create_iou(iou_payload)
            return json.dumps({
                "users": [u.data for u in users]
            })