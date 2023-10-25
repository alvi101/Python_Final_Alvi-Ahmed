from abc import ABC, abstractmethod


class User_Account(ABC):
    all_accounts = []
    admins = []
    reserve = 1000000
    loan_given = 0
    can_loan = False

    def __init__(self, name, email, address, account_type) -> None:
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_number = len(User_Account.all_accounts) + 1
        self.balance = 0
        self.history = []

    def check_balance(self):
        print('\n--------------')
        print(f'Balance of {self.name}: BDT {self.balance}\n')

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            self.history.append('')
            transaction = {'deposit': amount}
            self.history.append(transaction)
            print('\n--------------')
            print(f'\n{amount} deposited. New balance: BDT {self.balance}\n')
        else:
            print('Deposit amount cannot be less than zero')

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            transaction = {'withdraw': amount}
            self.history.append(transaction)
            print('\n--------------')
            print(f'\n{amount} withdrawn. New balance: BDT {self.balance}\n')
        else:
            print(f'\nNot enough balance: {self.balance}\n')

    def check_history(self):
        print(f'\n-----Transaction History--------')
        for transaction in self.history:
            print(transaction)
        print('----------------\n')

    def transfer_money(self, amount, act_number):
        if amount > self.balance:
            print('\nInadequate balance')
            return

        for account in User_Account.all_accounts:
            if account.account_number == act_number:
                account.balance += amount
                self.balance -= amount
                transaction = {'transfer': amount}
                self.history.append(transaction)
                account.history.append(transaction)
                print('\n--------------')
                print(f'Transfered BDT {amount} to Account: {act_number}')
                return
        print('\nAccount does not exist\n')

    def take_loan(self, amount):
        if User_Account.can_loan and (amount <= User_Account.reserve):
            self.balance += amount
            User_Account.reserve -= amount
            User_Account.loan_given += amount
            transaction = {'loan': amount}
            self.history.append(transaction)
            print('\n--------------')
            print(
                f'{amount} loan given to {self.name}. New balance: BDT {self.balance}')
        else:
            print('Can\'t take loan. Contact admin')

    @abstractmethod
    def show_info(self):
        raise NotImplementedError


class Savings_Account(User_Account):
    def __init__(self, name, email, address) -> None:
        super().__init__(name, email, address, 'savings')
        self.privilege = 'user'
        super().all_accounts.append(self)

    def show_info(self):
        print(f'Account Name: {self.name}')
        print(f'Account Type: {self.account_type}')
        print(f'Account Number: {self.account_number}')
        print(f'Account balance: BDT {self.balance}')
        print(f'Email: {self.email}')
        print(f'Address: {self.address}')


class Current_Account(User_Account):
    def __init__(self, name, email, address) -> None:
        super().__init__(name, email, address, 'current')
        self.privilege = 'user'
        super().all_accounts.append(self)

    def show_info(self):
        print(f'Account Name: {self.name}')
        print(f'Account Type: {self.account_type}')
        print(f'Account Number: {self.account_number}')
        print(f'Account balance: BDT {self.balance}')
        print(f'Email: {self.email}')
        print(f'Address: {self.address}')


class Admin:
    all_admins = []

    def __init__(self, name, email, address, employee_id) -> None:
        self.name = name
        self.email = email
        self.address = address
        self.employee_id = employee_id
        self.privilege = 'admin'
        Admin.all_admins.append(self)

    def create_account(self, name, email, address, account_type):
        if account_type == 'savings':
            Savings_Account(name, email, address)
        else:
            Current_Account(name, email, address)

    def delele_user(self, account_number):
        accounts = User_Account.all_accounts
        for i in range(len(accounts)):
            if accounts[i].account_number == account_number:
                User_Account.all_accounts.pop(i)
                print('\n--------------')
                print(f'Account Number: {account_number} deleted')
                return
            else:
                print('\n--------------')
                print('Account does not exist')

    def show_all_accounts(self):
        print()
        print('\n---------ALL USER ACCOUNTS---------')
        for account in User_Account.all_accounts:
            account.show_info()
            print('--------------------------\n')

    def check_reserve(self):
        print(User_Account.reserve)

    def check_total_loan(self):
        print(User_Account.loan_given)

    def turn_loan_off(self):
        User_Account.can_loan = False

    def turn_loan_on(self):
        User_Account.can_loan = True


current_user = None
while True:
    print('\n--------MEGA BANK--------')
    if current_user == None:
        u = input('Are you ad Admin or User (A/U): ')
        if u == 'A':
            op = input('Register or Log in as Admin (R/L): ')
            if op == 'R':
                print('\nRegistering new admin. Please fill in details\n')
                name = input('Enter admin name: ')
                email = input('Enter admin email: ')
                address = input('Enter admin address: ')
                id = input('Set employee admin employee ID: ')
                current_user = Admin(name, email, address, id)
            elif op == 'L':
                id = input('Enter admin employee ID: ')
                for admin in Admin.all_admins:
                    if admin.employee_id == id:
                        current_user = admin
        elif u == 'U':
            op = input('Register or Log in as User (R/L): ')
            if op == 'R':
                print('\nRegistering new User. Please fill in details\n')
                name = input('Enter user name: ')
                email = input('Enter user email: ')
                address = input('Enter user address: ')
                act_type = input(
                    'Enter Account Type:\n\t1. Savings\n\t2. Current)\nAccount Type: ')
                if act_type == '1':
                    current_user = Savings_Account(name, email, address)
                elif act_type == '2':
                    current_user = Current_Account(name, email, address)
                else:
                    print('\nInvalid Account Type. Try again\n')
            elif op == 'L':
                act_number = int(input('Enter user account number: '))
                for account in User_Account.all_accounts:
                    if account.account_number == act_number:
                        current_user = account
    else:
        if current_user.privilege == 'admin':
            print(f'Welcome Admin {current_user.name}')
            print('1. Create Account')
            print('2. Delete Account')
            print('3. See all User Accounts')
            print('4. Check Total Reserve')
            print('5. Check Total Loan Given')
            print('6. Turn Loan On/Off')
            print('7. Logout')
            op = int(input('Enter option: '))
            if op == 1:
                name = input('Enter user name: ')
                email = input('Enter user email: ')
                address = input('Enter user address: ')
                act_type = input(
                    'Enter Account Type:\n\t1. Savings\n\t2. Current)\nAccount Type: ')
                if act_type == '1':
                    Savings_Account(name, email, address)
                elif act_type == '2':
                    Current_Account(name, email, address)
            elif op == 2:
                act_number = input('Enter account number: ')
                current_user.delele_user(act_number)
                print('\n------------------')
                print(f'Account: \'{act_number}\' deleted')
            elif op == 3:
                current_user.show_all_accounts()
            elif op == 4:
                current_user.check_reserve()
            elif op == 5:
                current_user.check_total_loan()
            elif op == 6:
                f = input(
                    'Turn Loan On/Off:\n\t1. On\n\t2. Off\nChoose option: ')
                if f == '1':
                    current_user.turn_loan_on()
                    print('\n-----------')
                    print(f'Loans turned on\n')
                else:
                    current_user.turn_loan_off()
                    print('\n-----------')
                    print(f'Loans turned off\n')
            elif op == 7:
                current_user = None
            else:
                print('\nInvalid option\n')
        elif current_user.privilege == 'user':
            print(
                f'\nWelcome User {current_user.name}. Act Number: {current_user.account_number}')
            print('1. Deposit')
            print('2. Withdraw')
            print('3. Check balance')
            print('4. Check Transaction History')
            print('5. Take Loan')
            print('6. Transfer Money')
            print('7. Logout')
            op = int(input('Enter option: '))
            if op == 1:
                amount = int(input('Enter deposit amount: '))
                current_user.deposit(amount)
            elif op == 2:
                amount = int(input('Enter withdraw amount: '))
                current_user.withdraw(amount)
            elif op == 3:
                current_user.check_balance()
            elif op == 4:
                current_user.check_history()
            elif op == 5:
                amount = int(input('Enter loan amount: '))
                current_user.take_loan(amount)
            elif op == 6:
                amount = int(input('Enter amount to transfe: '))
                account_num = int(input('Enter account number: '))
                current_user.transfer_money(amount, account_num)
            elif op == 7:
                current_user = None
            else:
                print('\nInvalid option\n')
