import re
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt
from account.user import User
from account.bank_account import BankAccount

console = Console()

class BankOperator:
    def __init__(self):
        self.users = []
        self.accounts = []
        self.valid_account_types = ["Savings", "Current"]

    def create_user(self):
        console.print("\n[bold cyan]Creating a new user[/bold cyan]")
        name = Prompt.ask("Enter user name")
        email = Prompt.ask("Enter user email")
        
        # Issue #7: Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            console.print("[bold red]Invalid email address![/bold red]")
            return
        
        user = User(name, email)
        self.users.append(user)
        console.print(f"[bold green]User {name} created successfully![/bold green]")

    def list_users(self):
        if not self.users:
            console.print("[bold yellow]No users available.[/bold yellow]")
            return
        
        console.print("\n[bold cyan]List of Users[/bold cyan]")
        for i, user in enumerate(self.users, 1):
            console.print(f"{i}. {user.name} ({user.email})")

    def create_account(self):
        # Issue #1 & #4: Prevent account creation if no users exist
        if not self.users:
            console.print("[bold red]No users available. Please create a user first.[/bold red]")
            return
        
        console.print("\n[bold cyan]Creating a new account[/bold cyan]")
        self.list_users()
        
        # Issue #3 & #5: Validate user selection
        try:
            user_index = int(Prompt.ask("Select user by number")) - 1
            if user_index < 0 or user_index >= len(self.users):
                console.print("[bold red]Invalid user selection.[/bold red]")
                return
        except ValueError:
            console.print("[bold red]Invalid user selection.[/bold red]")
            return
        
        user = self.users[user_index]
        
        # Issue #6: Validate account type
        account_type = Prompt.ask("Enter account type", choices=self.valid_account_types)
        if account_type not in self.valid_account_types:
            console.print("[bold red]Invalid account type![/bold red]")
            return
        
        account = BankAccount(user, account_type)
        self.accounts.append(account)
        console.print(f"[bold green]{account_type} account created for {user.name}![/bold green]")

    def deposit_money(self):
        if not self.accounts:
            console.print("[bold yellow]No accounts available.[/bold yellow]")
            return
        
        account = self._select_account()
        if not account:
            return
        
        amount = FloatPrompt.ask("Enter deposit amount")
        if amount <= 0:
            console.print("[bold red]Amount must be positive![/bold red]")
            return
        
        account.deposit(amount)
        console.print(f"[bold green]Deposited ${amount:.2f}. New balance: ${account.balance:.2f}[/bold green]")

    def withdraw_money(self):
        if not self.accounts:
            console.print("[bold yellow]No accounts available.[/bold yellow]")
            return
        
        account = self._select_account()
        if not account:
            return
        
        amount = FloatPrompt.ask("Enter withdrawal amount")
        if amount <= 0:
            console.print("[bold red]Amount must be positive![/bold red]")
            return
        
        if account.balance < amount:
            console.print("[bold red]Insufficient funds![/bold red]")
            return
        
        account.withdraw(amount)
        console.print(f"[bold green]Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}[/bold green]")

    def view_transactions(self):
        if not self.accounts:
            console.print("[bold yellow]No accounts available.[/bold yellow]")
            return
        
        account = self._select_account()
        if not account:
            return
        
        console.print(f"\n[bold cyan]Transactions for {account.user.name}'s {account.account_type} account[/bold cyan]")
        if not account.transactions:
            console.print("[bold yellow]No transactions available.[/bold yellow]")
            return
        
        for transaction in account.transactions:
            console.print(transaction)

    def _select_account(self):
        console.print("\n[bold cyan]Available Accounts[/bold cyan]")
        for i, account in enumerate(self.accounts, 1):
            console.print(f"{i}. {account.user.name}'s {account.account_type} (Balance: ${account.balance:.2f})")
        
        try:
            account_index = int(Prompt.ask("Select account by number")) - 1
            if account_index < 0 or account_index >= len(self.accounts):
                console.print("[bold red]Invalid account selection.[/bold red]")
                return None
            return self.accounts[account_index]
        except ValueError:
            console.print("[bold red]Invalid account selection.[/bold red]")
            return None
