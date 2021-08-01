import shelve


class Order:
    def __init__(self, deliveryStatus, orderDate, total, customerId):
        mydict1 = shelve.open('quantity.db', 'c')
        if 'order_id' in mydict1:
            self.__last_id = mydict1['order_id']
        else:
            self.__last_id = 0

        self.__total = total
        self.__orderDate = orderDate
        self.__deliveryStatus = deliveryStatus
        self.__current_id = self.__last_id + 1
        self.__customer_id = customerId

        mydict1['order_id'] = self.__current_id
        mydict1.close()

    def set_delivery_status(self, deliveryStatus):
        self.__deliveryStatus = deliveryStatus

    def set_orderDate(self, orderDate):
        self.__orderDate = orderDate

    def get_total(self):
        return self.__total

    def get_current_id(self):
        return self.__current_id
    
    def get_customer_id(self):
        return self.__customer_id

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_delivery_status(self):
        return self.__deliveryStatus

    def get_orderDate(self):
        return self.__orderDate
