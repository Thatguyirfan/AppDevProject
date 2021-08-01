class Customer:
    def __init__(self, nric, temperature, entrytime, date, mobile, title):
        self.__nric = nric.upper()
        self.__temperature = temperature
        self.__entrytime = entrytime
        self.__date = date
        self.__mobile = mobile
        self.__exittime = ""
        self.__title = title

    def set_nric(self, nric):
        self.__nric = nric.upper()

    def set_temperature(self, temperature):
        self.__temperature = temperature

    def set_entrytime(self, entrytime):
        self.__entrytime = entrytime

    def set_date(self, date):
        self.__date = date

    def set_mobile(self, mobile):
        self.__mobile = mobile

    def set_exittime(self, exittime):
        self.__exittime = exittime

    def set_title(self, title):
      self.__title = title

    def get_nric(self):
        return self.__nric

    def get_temperature(self):
        return self.__temperature

    def get_entrytime(self):
        return self.__entrytime

    def get_date(self):
        return self.__date

    def get_mobile(self):
        return self.__mobile

    def get_exittime(self):
        return self.__exittime

    def get_title(self):
      return self.__title
