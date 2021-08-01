import shelve, re


class Product:
    def __init__(self, name, description, ingredients, price, instocks, category, img):
        # getting the last ID
        mydict = shelve.open('count.db', 'c')
        if 'productID' in mydict:
            self.__last_id = mydict['productID']
        else:
            print('no productID key in shelve')
            self.__last_id = 0

        self.__count_id = self.__last_id + 1
        self.__name = name
        self.__desc = description
        self.__ingredients = ingredients
        self.__price = price
        self.__instocks = instocks  # dictionary of instocks per location
        self.__category = category
        self.__img = img
        self.price = self.__price
        self.name = self.__name

        # updated ID
        mydict['productID'] = self.__count_id
        print('productID created')
        self.__updated_id = mydict['productID']
        mydict.close()

    def set_Price(self):
        self.price = self.__price

    def set_Name(self):
        self.name = self.__name

    def set_split(self):
        self.splitName = re.split(r' ', self.get_name().lower())
        return self.splitName

    def set_instocks(self, instocks):
        self.__instocks = instocks

    def set_id(self, id):
        self.__count_id = id

    def set_name(self, name):
        self.__name = name

    def set_desc(self, desc):
        self.__desc = desc

    def set_ingredients(self, ingredients):
        self.__ingredients = ingredients

    def set_price(self, price):
        self.__price = price

    def set_category(self, category):
        self.__category = category

    def set_img(self, img):
        self.__img = img

    def get_instocks(self):
        return self.__instocks

    def get_id(self):
        return self.__count_id

    def get_name(self):
        return self.__name

    def get_desc(self):
        return self.__desc

    def get_ingredients(self):
        return self.__ingredients

    def get_price(self):
        return self.__price

    def get_category(self):
        return self.__category

    def get_img(self):
        return self.__img

    # for checking
    def get_last_id(self):
        return self.__last_id

    def get_updated_id(self):
        return self.__updated_id

class Supplier:
    def __init__(self, product, quantity, delivery):
        # getting the last ID
        mydict = shelve.open('count.db', 'c')
        if 'supplierID' in mydict:
            self.__last_id = mydict['supplierID']
        else:
            print('no supplierID key in shelve, creating new supplierID')
            self.__last_id = 0

        self.__id = self.__last_id + 1
        self.__product = product
        self.__quantity = quantity
        self.__delivery = delivery  # delivery location (CQ, Orchard, CitySq, Sq2, 100AM, JCube, Jem)
        self.__name = product.get_name()

        # updated ID
        mydict['supplierID'] = self.__id
        mydict.close()

    def set_product(self, product):
        self.__product = product

    def set_name(self):
        self.__name = self.__product.get_name()

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_delivery(self, delivery):
        self.__delivery = delivery

    def get_product(self):
        return self.__product

    def get_product_name(self):
        return self.__name

    def get_quantity(self):
        return self.__quantity

    def get_delivery(self):
        return self.__delivery

    def get_id(self):
        return self.__id
