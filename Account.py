import shelve
from decimal import Decimal


class Account:
    def __init__(self, full_name, address, phone, email, password, title=""):
        accounts_dict = {}

        db = shelve.open("storage.db", "c")
        try:
            accounts_dict = db["Accounts"]
        except:
            print("something wrong here?")
        db.close()

        accounts_list = []
        for key in accounts_dict:
            account = accounts_dict.get(key)
            accounts_list.append(account)
        if len(accounts_list) == 0:
            self.__user_id = 1
        else:
            self.__user_id = accounts_list[len(accounts_list) - 1].get_user_id() + 1
        self.__full_name = full_name
        self.__address = address
        self.__phone = phone
        self.__email = email
        self.__password = password
        self.__title = title

    def get_user_id(self):
        return self.__user_id

    def get_full_name(self):
        return self.__full_name

    def get_address(self):
        return self.__address

    def get_phone(self):
        return self.__phone

    def get_email(self):
        return self.__email

    def get_title(self):
        return self.__title

    def check_password(self, password):
        # returns true for password correct and false for password incorrect
        return self.__password == password

    # skipped getter for password for safety, instead use check_password and provide a password to check against

    def set_full_name(self, full_name):
        self.__full_name = full_name

    def set_address(self, address):
        self.__address = address

    def set_phone(self, phone):
        self.__phone = phone

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_title(self, title):
        self.__title = title


class Customer(Account):
    def __init__(self, full_name, address, phone, email, password):
        super().__init__(full_name, address, phone, email, password, "Bronze Member")
        self.__coins = 0
        self.__purchase_history = []
        self.__vouchers = []
        self.__multiplier = 1
        self.__spent = Decimal(0.00)

    def get_coins(self):
        return self.__coins

    def get_purchase_history(self):
        return self.__purchase_history

    def get_vouchers(self):
        return self.__vouchers

    def get_multiplier(self):
        return self.__multiplier

    def get_spent(self):
        return self.__spent

    def add_spent(self, spent):
        try:
            spent = Decimal(spent)
        except ValueError:
            return None
        coins_added = spent * self.get_multiplier()
        self.__spent += spent
        self.__coins += int(coins_added)
        if self.get_title() != "Platinum Member":
            if self.get_spent() > 14999:
                self.set_multiplier(4)
                self.set_title("Platinum Member")
            elif self.get_spent() > 4999:
                self.set_multiplier(3)
                self.set_title("Gold Member")
            elif self.get_spent() > 1999:
                self.set_multiplier(2)
                self.set_title("Silver Member")

    def remove_coins(self, coins_removed):
        try:
            coins_removed = int(coins_removed)
        except ValueError:
            return None
        self.__coins -= coins_removed

    def set_coins(self, coins):
        try:
            coins = int(coins)
        except ValueError:
            return None
        self.__coins = coins

    def add_purchase_history(self, purchase):
        self.__purchase_history.append(purchase)

    def set_purchase_history(self, purchase_history):
        self.__purchase_history = purchase_history

    def add_vouchers(self, voucher):
        self.__vouchers.append(voucher)

    def remove_vouchers(self, voucher):
        try:
            index = self.__vouchers.index(voucher)
        except ValueError:
            return None
        self.__vouchers.pop(index)

    def set_vouchers(self, vouchers):
        self.__vouchers = vouchers

    def set_multiplier(self, multiplier):
        try:
            multiplier = int(multiplier)
        except ValueError:
            return None
        self.__multiplier = multiplier


class Employee(Account):
    def __init__(self, full_name, address, phone, email, password, schedule={}, salary='0', working_location="", nric=""):
        super().__init__(full_name, address, phone, email, password, "Employee")
        self.__schedule = schedule
        self.__hours_clocked = 0
        self.__salary = salary
        self.__working_location = working_location
        self.__nric = nric

    def get_schedule(self):
        return self.__schedule

    def get_hours_clocked(self):
        return self.__hours_clocked

    def get_salary(self):
        return self.__salary

    def get_working_location(self):
        return self.__working_location
    
    def get_nric(self):
        return self.__nric

    def set_schedule(self, schedule):
        self.__schedule = schedule

    def add_hours_clocked(self, clocked):
        try:
            clocked = Decimal(clocked)
        except ValueError:
            return None
        self.__hours_clocked += clocked

    def remove_hours_clocked(self, clocked):
        try:
            clocked = Decimal(clocked)
        except ValueError:
            return None
        self.__hours_clocked -= clocked

    def set_hours_clocked(self, clocked):
        try:
            clocked = Decimal(clocked)
        except ValueError:
            return None
        self.__hours_clocked = clocked

    def set_salary(self, salary):
        try:
            salary = int(salary)
        except ValueError:
            return None
        self.__salary = salary

    def set_working_location(self, working_location):
        try:
            working_location = str(working_location)
        except ValueError:
            return None
        self.__working_location = working_location
    
    def set_nric(self, nric):
        self.__nric = nric


class Manager(Account):
    def __init__(self, full_name, address, phone, email, password):
        super().__init__(full_name, address, phone, email, password, "Manager")
        self.__title = "Manager"
