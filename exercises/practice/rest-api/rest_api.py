from collections import defaultdict
from functools import reduce
import json

class User:
    def __init__(self, data) -> None:
        self.name = data["name"]
        self.owes = defaultdict(float, data.get("owes", {}))
        self.owed_by = defaultdict(float, data.get("owed_by", {}))

    def __repr__(self) -> str:
        return f"<User name={self.name}, owes={self.owes}, owed_by={self.owed_by}>"

    def get_balance(self, other_user=None):
        """
        compute balance for user, optionally filtering by relationship with a single other user
        """
        credits = [
            amount
            for name, amount
            in self.owed_by.items()
            if (other_user and other_user.name == name) or True
        ]

        debts = [
            amount
            for name, amount
            in self.owes.items()
            if (other_user and other_user.name == name) or True
        ]

        return sum(credits) - sum(debts)
    
    @property
    def data(self):
        return {
            "name": self.name,
            "owes": self.owes,
            "owed_by": self.owed_by,
            "balance": self.get_balance(),
        }
    def set_new_balance_with(self, other_user, amount):
        if amount > 0:
            # the other user owes this user money
            self.update_owed_by(other_user, amount)
            self.clear_owes(other_user)
        elif amount < 0:
            # this user owes money to the other user
            self.update_owes(other_user, amount)
            self.clear_owed_by(other_user)
        else:
            # the two users are even.
            self.clear_owed_by(other_user)
            self.clear_owes(other_user)

    def update_owed_by(self, other_user, amount):
        self.owed_by[other_user.name] = abs(amount)

    def clear_owed_by(self, other_user):
        """
        clear record of other_user owing user if exists
        """
        self.owed_by.pop(other_user.name, None)

    def update_owes(self, other_user, amount):
        self.owes[other_user.name] = abs(amount)

    def clear_owes(self, other_user):
        """
        clear record of user owing other_user if exists
        """
        self.owes.pop(other_user.name, None)

    def create_debt(self, lender, amount):
        """
        compute the new balance for both users and update
        """
        my_balance = self.get_balance(other_user=lender)
        my_new_balance = my_balance - amount

        other_balance = lender.get_balance(other_user=self)
        other_new_balance = other_balance + amount

        self.set_new_balance_with(other_user=lender, amount=my_new_balance)
        lender.set_new_balance_with(other_user=self, amount=other_new_balance)


class Database:
    """
    should use objects internally, but return dicts
    """
    def __init__(self, data) -> None:
        self.users = [
            User(data)
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
        user = User({"name": user_name})
        self.users.append(user)
        return user

    def create_iou(self, iou):
        """
        example: {"lender": "Adam", "borrower": "Bob", "amount": 3.0}
        """

        """
        TODO: the net balance between users should be shown. 
        Instead of {'name': 'Adam', 'owes': {'Bob': 3.0}, 'owed_by': {'Bob': 2.0}, 'balance': -1.0}
        show {'name': 'Adam', 'owes': {'Bob': 1.0}, 'owed_by': {}, 'balance': -1.0}
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

        borrower.create_debt(lender=lender, amount=amount)
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