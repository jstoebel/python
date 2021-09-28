from threading import Lock

def ensure_open_status(open_status: bool):
    def ensure_open(func):
        def _decorator(self, *args, **kwargs):
            # access a from TestSample
            if self._open is not open_status:
                raise ValueError("account is closed")
            return func(self, *args, **kwargs)
        return _decorator
    return ensure_open

def spam(func):
    def _decorator(self, *args, **kwargs):
        print("inside lock")
        return func(self, *args, **kwargs)
    return _decorator 

class BankAccount:
    def __init__(self):
        self.balance = 0
        self._open = False
        self.lock = Lock()

    @ensure_open_status(True)
    def get_balance(self):
        return self.balance

    @ensure_open_status(False)
    def open(self):
        self._open = True
        self.balance = 0

    @ensure_open_status(True)
    def deposit(self, amount):
        with self.lock:
            if amount < 0:
                raise ValueError(f"Deposit amount must be more than 0! Got {amount}")
            self.balance += amount

    @ensure_open_status(True)
    def withdraw(self, amount):
        with self.lock:
            if amount > self.balance:
                raise ValueError(f"Withdraw amount {amount} may not be higher than balance {self.balance}")

            if amount < 0:
                raise ValueError(f"Withdraw amount must be more than 0! Got {amount} ")
            self.balance -= amount

    @ensure_open_status(True)
    def close(self):
        self._open = False
