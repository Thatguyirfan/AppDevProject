import phonenumbers, shelve
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, PasswordField, validators, DecimalField, DateField, TimeField, IntegerField, FileField
from Stores import stores, tuple_list


def validate_phone(self, phone):
    try:
        p = phonenumbers.parse("+65" + phone.data)
        if not phonenumbers.is_valid_number(p):
            raise ValueError()
    except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
        raise validators.ValidationError('Invalid phone number.')


def validate_nric(form, field):
    if len(field.data) == 9:
        if field.data[0].upper() == "T" or field.data[0].upper() == "S":
            if field.data[-1].isalpha():
                if field.data[1:8].isdigit():
                    return True
                else:
                    raise validators.ValidationError("Invalid NRIC")
            else:
                raise validators.ValidationError("Invalid NRIC")
        else:
            raise validators.ValidationError("Invalid NRIC")
    else:
        raise validators.ValidationError("Must be 9 characters long")


def validate_temp(form, field):
    if len(field.data) == 4:
        if field.data[:2].isdigit() and field.data[-1].isdigit():
            if field.data[2] == '.':
                return True
            else:
                raise validators.ValidationError("Invalid format")
        else:
            raise validators.ValidationError("Invalid format")
    else:
        raise validators.ValidationError("Invalid format")


def validate_name(form, field):
  if len(field.data) < 31:
    if field.data.isdigit() != True:
      return True
    else:
      raise validators.ValidationError("Invalid name")
  else:    
    raise validators.ValidationError("Invalid name")


class CreateUserForm(Form):
    first_name = StringField(
        "First Name",
        [validators.Length(min=1, max=150),
         validators.DataRequired()])
    last_name = StringField(
        "Last Name",
        [validators.Length(min=1, max=150),
         validators.DataRequired()])
    gender = SelectField(
        "Gender", [validators.DataRequired()],
        choices=[("", "Select"), ("F", "Female"), ("M", "Male")],
        default="F")
    membership = RadioField(
        "Membership",
        choices=[("F", "Fellow"), ("S", "Senior"), ("P", "Professional")],
        default="F")
    remarks = TextAreaField("Remarks", [validators.Optional()])


class ForgotPasswordForm(Form):
    email = StringField(
        "Email",
        [validators.Email(), validators.DataRequired()])


class LoginForm(Form):
    email = StringField(
        "Email",
        [validators.Email(), validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])


class RegisterForm(Form):
    full_name = StringField(
        "Full Name",
        [validators.Length(min=1, max=150),
         validators.DataRequired()])
    address = StringField(
        "Address",
        [validators.Length(min=1, max=150),
         validators.DataRequired()])
    phone = StringField("Phone", [validators.DataRequired()])
    email = StringField(
        "Email",
        [validators.Email(), validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse("+65" + phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise validators.ValidationError('Invalid phone number.')
    
    salary = IntegerField("Salary", [validators.Optional()])
    working_location = SelectField("Working Location", [validators.Optional()], choices=tuple_list, default='')
    nric = StringField("NRIC", [validators.Optional(), validate_nric])


class EditProfileForm(Form):
    full_name = StringField(
        "Full Name",
        [validators.Length(min=1, max=150),
         validators.DataRequired()])
    address = StringField(
        "Address",
        [validators.Length(min=1, max=150),
         validators.DataRequired()])
    phone = StringField("Phone", [validators.DataRequired()])
    email = StringField(
        "Email",
        [validators.Email(), validators.DataRequired()])
    salary = IntegerField("Salary", [validators.Optional()])
    working_location = SelectField("Working Location", [validators.Optional()], choices=tuple_list, default='')


class EditScheduleForm(Form):
    Monday0 = StringField(label='', default="")
    Monday1 = StringField(label='', default="")
    Monday2 = StringField(label='', default="")
    Monday3 = StringField(label='', default="")
    Monday4 = StringField(label='', default="")
    Monday5 = StringField(label='', default="")
    Monday6 = StringField(label='', default="")
    Monday7 = StringField(label='', default="")
    Monday8 = StringField(label='', default="")
    Monday9 = StringField(label='', default="")
    Tuesday0 = StringField(label='', default="")
    Tuesday1 = StringField(label='', default="")
    Tuesday2 = StringField(label='', default="")
    Tuesday3 = StringField(label='', default="")
    Tuesday4 = StringField(label='', default="")
    Tuesday5 = StringField(label='', default="")
    Tuesday6 = StringField(label='', default="")
    Tuesday7 = StringField(label='', default="")
    Tuesday8 = StringField(label='', default="")
    Tuesday9 = StringField(label='', default="")
    Wednesday0 = StringField(label='', default="")
    Wednesday1 = StringField(label='', default="")
    Wednesday2 = StringField(label='', default="")
    Wednesday3 = StringField(label='', default="")
    Wednesday4 = StringField(label='', default="")
    Wednesday5 = StringField(label='', default="")
    Wednesday6 = StringField(label='', default="")
    Wednesday7 = StringField(label='', default="")
    Wednesday8 = StringField(label='', default="")
    Wednesday9 = StringField(label='', default="")
    Thursday0 = StringField(label='', default="")
    Thursday1 = StringField(label='', default="")
    Thursday2 = StringField(label='', default="")
    Thursday3 = StringField(label='', default="")
    Thursday4 = StringField(label='', default="")
    Thursday5 = StringField(label='', default="")
    Thursday6 = StringField(label='', default="")
    Thursday7 = StringField(label='', default="")
    Thursday8 = StringField(label='', default="")
    Thursday9 = StringField(label='', default="")
    Friday0 = StringField(label='', default="")
    Friday1 = StringField(label='', default="")
    Friday2 = StringField(label='', default="")
    Friday3 = StringField(label='', default="")
    Friday4 = StringField(label='', default="")
    Friday5 = StringField(label='', default="")
    Friday6 = StringField(label='', default="")
    Friday7 = StringField(label='', default="")
    Friday8 = StringField(label='', default="")
    Friday9 = StringField(label='', default="")


class ChangePasswordForm(Form):
    current_password = PasswordField("Current Password",
                                     [validators.DataRequired()])
    new_password = PasswordField("New Password", [validators.DataRequired()])
    confirm_password = PasswordField("Confirm New Password",
                                     [validators.DataRequired()])


class GetCount(Form):
    store = SelectField('Select Store', choices=tuple_list, default='')
    day = SelectField(
        'Select Day',
        choices=[
            ('Mon', 'Monday'),
            ('Tue', 'Tuesday'),
            ('Wed', 'Wednesday'),
            ('Thu', 'Thursday'),
            ('Fri', 'Friday'),
            ('Sat', 'Saturday'),
            ('Sun', 'Sunday'),
        ],
        default='')


class StoreEntry(Form):
    nric = StringField('NRIC: ', [validators.DataRequired(), validate_nric])
    temperature = StringField('Temperature(°C): ',
                              [validators.DataRequired(), validate_temp])
    date = StringField('Date: ')
    entrytime = StringField('Time: ')
    mobile = StringField('Mobile No.: ', [validators.DataRequired()])
    store = SelectField(
        'Select Store: ', [validators.DataRequired()],
        choices=tuple_list,
        default='')


class ChooseRecords(Form):
    store = SelectField('Select Store: ', choices=tuple_list, default='')


class RecordsFilter(Form):
    filter = RadioField('Display: ', choices=[("All", "All"), ("Customers", "Customers only"), ("Employees", "Employees only")], default="All")


class FeedbackForm(Form):
    name = StringField('Name: ', [validators.DataRequired(), validate_name])
    mobile = StringField('Mobile No.: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    reason = SelectField('Reason of form: ', choices=[('Compliment', 'Compliment'), ('Suggestion', 'Suggestion'), ('Complaint', 'Complaint'), ('Others', 'Others')])
    message = TextAreaField('Message: ', [validators.DataRequired(), validators.Length(min=1, max=100)])
    store = SelectField('Select Store: ', choices=tuple_list, default='')

  
class FeedbackFilter(Form):
  store = SelectField('Store: ', choices=['All', 'Orchard Central', '100 AM', 'City Square Mall', 'Square 2', 'Clarke Quay Central', 'JCube', 'Jem', 'HarbourFront Centre'], default='All')
  reason = SelectField('Reason: ', choices=[('All', 'All'), ('Compliment', 'Compliment'), ('Suggestion', 'Suggestion'), ('Complaint', 'Complaint'), ('Others', 'Others')], default='All')


# class UpdateCustomer(Form):
#     nric = StringField('NRIC: ', [validators.DataRequired(), validate_nric])
#     temperature = StringField('Temperature(°C): ',
#                               [validators.DataRequired(), validate_temp])
#     date = StringField('Date: ')
#     entrytime = StringField('Time: ')
#     mobile = StringField('Mobile No.: ', [validators.DataRequired()])
#     store = StringField('Store: ', [validators.DataRequired()])

class CreateProductForm(Form):
    name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    description = TextAreaField('Product Description', [validators.Optional()])
    ingredients = TextAreaField('Product Ingredients', [validators.optional()])
    price = DecimalField('Product Price ($)', [validators.DataRequired()], places=2)
    instocks_WH = IntegerField('Instocks @ Warehouse', [validators.Optional()], default=0)
    instocks_CQ = IntegerField('Instocks @ Clarke Quay', [validators.Optional()], default=0)
    instocks_Orchard = IntegerField('Instocks @ Orchard', [validators.Optional()], default=0)
    instocks_CitySq = IntegerField('Instocks @ City Square Mall', [validators.Optional()], default=0)
    instocks_Sq2 = IntegerField('Instocks @ Square 2', [validators.Optional()], default=0)
    instocks_100AM = IntegerField('Instocks @ 100AM', [validators.Optional()], default=0)
    instocks_JCube = IntegerField('Instocks @ JCube', [validators.Optional()], default=0)
    instocks_Jem = IntegerField('Instocks @ Jem', [validators.Optional()], default=0)
    category = SelectField('Product Category', [validators.DataRequired()], choices=[("", 'Select'), ('S', 'Snacks'), ('D', "Drinks")], default="")
    img = FileField("Product Image", [validators.Optional()])

db = shelve.open('products.db', 'c')
mylist = []
try:
    product_dict = db["Products"]
    mylist = [("", 'Select')]
    for key in product_dict:
        i = product_dict[key]
        currentList = (i.get_id(), i.get_name())
        mylist.append(currentList)

except:
    print("no products avail")
db.close()

class CreateRestockForm(Form):
    product = SelectField('Product', [validators.DataRequired()], choices=mylist, default="")
    quantity = IntegerField('Product Quantity', [validators.DataRequired()], default=0)
    send_to = SelectField('Delivery Location', [validators.DataRequired()], choices=[('', 'Select'), ('WH', "Warehouse"), ('CQ', 'Clarke Quay'), ('Orchard', 'Orchard'), ('CitySq', 'City Square'), ('Sq2', 'Square 2'), ('HundredAM', '100AM'), ('JCube', 'JCube'), ('Jem', 'Jem')], default='')

#khei
class CreateUpdateOrderForm(Form):
  deliveryStatus = SelectField('Delivery Status: ', [validators.DataRequired()], choices=[("Packing"), ('Ready To Deliver'), ('On The Way'), ('Delivered')])
  id = StringField('Order ID: ', [validators.DataRequired()])
  order_date = StringField('Order Date: ', [validators.DataRequired()])


def validate_age(form, field):
    if 15 < field.data < 100:
        return True
    else:
        raise validators.ValidationError("Invalid age")

class CreateApplicationForm(Form):
    name = StringField('Name (As in NRIC)', [validators.DataRequired(), validate_name])
    age = IntegerField('Age', [validators.DataRequired(), validate_age])
    phoneNo = StringField('Contact Number', [validators.DataRequired(), validate_phone])
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    commitmentPeriod = IntegerField('Commitment Period (months)',
                                    [validators.DataRequired()])
    location = SelectField('Preferred Area', [validators.DataRequired()],
                           choices=[('', 'Select'), ('CQ', 'Clarke Quay'), ('Orchard', 'Orchard'),
                                    ('CitySq', 'City Square'), ('Sq2', 'Square 2'), ('HundredAM', '100AM'),
                                    ('JCube', 'JCube'), ('Jem', 'Jem')], default='')