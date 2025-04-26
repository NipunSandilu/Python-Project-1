class BankAccount:
    def __init__(self, user, account_type):
        self.user = user
        self.account_type = account_type
        self.balance = 0.0
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposit: +${amount:.2f} (Balance: ${self.balance:.2f})")
        return self.balance

    def withdraw(self, amount):
        self.balance -= amount
        self.transactions.append(f"Withdrawal: -${amount:.2f} (Balance: ${self.balance:.2f})")
        return self.balance
