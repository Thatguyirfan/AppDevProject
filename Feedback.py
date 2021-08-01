class Feedback:
  def __init__(self, name, mobile, email, reason, message, date, store):
    self.__name = name
    self.__mobile = mobile
    self.__email = email
    self.__reason = reason
    self.__message = message
    self.__date = date
    self._store = store

  def set_name(self, name):
    self.__name = name

  def set_mobile(self, mobile):
    self.__mobile = mobile

  def set_email(self, email):
    self.__email = email

  def set_reason(self, reason):
    self.__reason = reason

  def set_message(self, message):
    self.__message = message

  def set_date(self, date):
    self.__date = date

  def set_store(self, store):
    self.__store = store

  def get_name(self):
    return self.__name

  def get_mobile(self):
    return self.__mobile

  def get_email(self):
    return self.__email

  def get_reason(self):
    return self.__reason

  def get_message(self):
    return self.__message

  def get_date(self):
    return self.__date

  def get_store(self):
    return self._store
