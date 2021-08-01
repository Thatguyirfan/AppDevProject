import Account, shelve, re

from flask import render_template, request, redirect, url_for, session

from Forms import RegisterForm, LoginForm, ForgotPasswordForm, EditProfileForm, EditScheduleForm, ChangePasswordForm, CreateApplicationForm

from Stores import stores, tuple_list

# TEST CODES: Creates manager and employee accounts automatically if none exists.
db = shelve.open("storage.db", "c")
accounts_dict = {}
try:
    accounts_dict = db["Accounts"]
except:
    print("Error in retrieving Accounts from storage.db.")
mgr_exists = False
emp_exists = False
for key in accounts_dict:
    if accounts_dict[key].get_title() == "Manager":
        mgr_exists = True
    elif accounts_dict[key].get_title() == "Employee":
        emp_exists = True
if not mgr_exists:
    manager = Account.Manager("Test Manager", "Test St", "91234567", "manager@test.com", "testpassword")
    accounts_dict[manager.get_user_id()] = manager
if not emp_exists:
    employee = Account.Employee("Test Employee", "Test St", "91234567", "employee@test.com", "testpassword", {"Monday": ["Cashier", "Test"], "Tuesday": [], "Wednesday": ["Hello", "Bye", "Ahhh"], "Thursday": ["", "Sleep"], "Friday": []}, 3000, stores[len(stores) - 1], "S9999999A")
    accounts_dict[employee.get_user_id()] = employee
db["Accounts"] = accounts_dict
db.close()
# END TEST CODES

def register():
    if "userID" in session:
        return redirect(url_for("dashboard"))
    register_form = RegisterForm(request.form)
    if request.method == "POST" and register_form.validate():
        accounts_dict = {}
        db = shelve.open("storage.db", "c")

        try:
            accounts_dict = db["Accounts"]
        except:
            print("Error in retrieving Accounts from storage.db.")

        already_registered = False
        for key in accounts_dict:
            if accounts_dict[key].get_email() == register_form.email.data:
                already_registered = True

        if already_registered:
            db.close()
            session["accError"] = "Email already exists in our database"
            return redirect(url_for("register"))
        account = Account.Customer(register_form.full_name.data, register_form.address.data, register_form.phone.data, register_form.email.data, register_form.password.data)
        accounts_dict[account.get_user_id()] = account
        db["Accounts"] = accounts_dict

        db.close()

        session["userID"] = account.get_user_id()

        return redirect(url_for("dashboard"))
    return render_template("register.html", form=register_form)

def login():
    if "userID" in session:
        return redirect(url_for("dashboard"))
    login_form = LoginForm(request.form)
    if request.method == "POST" and login_form.validate():
        accounts_dict = {}
        db = shelve.open("storage.db", "c")

        try:
            accounts_dict = db["Accounts"]
        except:
            print("Error in retrieving Accounts from storage.db.")

        exists = False
        for key in accounts_dict:
            if accounts_dict[key].get_email() == login_form.email.data:
                exists = True
                account = accounts_dict[key]
        db.close()
        if not exists or not account.check_password(login_form.password.data):
            if not exists:
                session["accError"] = "Email does not exist in our database"
            else:
                session["accError"] = "Password does not match"
            return redirect(url_for("login"))

        db.close()

        session["userID"] = account.get_user_id()

        return redirect(url_for("dashboard"))
    return render_template("login.html", form=login_form)

def logout():
    if "userID" in session:
        del session["userID"]
    return redirect(url_for("home"))

def forgot_password():
    if "userID" in session:
        return redirect(url_for("dashboard"))
    forgot_password_form = ForgotPasswordForm(request.form)
    if request.method == "POST" and forgot_password_form.validate():
        accounts_dict = {}
        db = shelve.open("storage.db", "c")

        try:
            accounts_dict = db["Accounts"]
        except:
            print("Error in retrieving Accounts from storage.db.")

        exists = False
        for key in accounts_dict:
            if accounts_dict[key].get_email() == forgot_password_form.email.data:
                exists = True
        db.close()
        if not exists:
            session["accError"] = "Email does not exist in our database"
            return redirect(url_for("forgot_password"))
        session["accSuccess"] = "Password reset link has been sent to your email"
        return redirect(url_for("forgot_password"))
    return render_template("forgotpassword.html", form=forgot_password_form)

def edit_profile():
    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    accounts_dict = {}
    db = shelve.open("storage.db", "c")
    try:
        accounts_dict = db["Accounts"]
    except:
        print("Error in retrieving Accounts from storage.db.")
    account = accounts_dict.get(session["userID"])
    edit_profile_form = EditProfileForm(request.form)
    if request.method == "POST" and edit_profile_form.validate():
        already_registered = False
        for key in accounts_dict:
            if key != account.get_user_id() and accounts_dict[key].get_email() == edit_profile_form.email.data:
                already_registered = True
        if already_registered:
            db.close()
            session["accError"] = "Email already exists in our database"
            return redirect(url_for("edit_profile"))
        account.set_full_name(edit_profile_form.full_name.data)
        account.set_address(edit_profile_form.address.data)
        account.set_phone(edit_profile_form.phone.data)
        account.set_email(edit_profile_form.email.data)
        accounts_dict[account.get_user_id()] = account
        db["Accounts"] = accounts_dict
        db.close()
        session["accSuccess"] = "Profile updated successfully"
        return redirect(url_for("edit_profile"))
    else:
        edit_profile_form.full_name.data = account.get_full_name()
        edit_profile_form.address.data = account.get_address()
        edit_profile_form.phone.data = account.get_phone()
        edit_profile_form.email.data = account.get_email()
    return render_template("editprofile.html", user=account, form=edit_profile_form)

def dashboard():
    if "returnToCart" in session and session["returnToCart"]:
        session["returnToCart"] = False
        return redirect(url_for("cartPage"))
    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    accounts_dict = {}
    db = shelve.open("storage.db", "c")
    try:
        accounts_dict = db["Accounts"]
    except:
        print("Error in retrieving Accounts from storage.db.")
    account = accounts_dict.get(session["userID"])
    accounts_dict[session["userID"]] = account
    db["Accounts"] = accounts_dict
    db.close()
    return render_template('dashboard.html', user=account)

def manage_accounts():
    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    db = shelve.open('storage.db', 'r')
    try:
        accounts_dict = db["Accounts"]
    except:
        db.close()
        return redirect(url_for('home'))
    if accounts_dict[session["userID"]].get_title() != "Manager":
        db.close()
        return redirect(url_for('home'))
    accounts_dict = db["Accounts"]
    db.close()
    session["from"] = "accounts"
    users_accounts_dict = {}
    for account in accounts_dict:
        if accounts_dict[account].get_title() not in ["Employee", "Manager"]:
            users_accounts_dict[account] = accounts_dict[account]
    return render_template("manageusers.html", users=users_accounts_dict)

def manage_employees():
    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    db = shelve.open('storage.db', 'r')
    try:
        accounts_dict = db["Accounts"]
    except:
        db.close()
        return redirect(url_for('home'))
    if accounts_dict[session["userID"]].get_title() != "Manager":
        db.close()
        return redirect(url_for('home'))
    accounts_dict = db["Accounts"]
    db.close()
    session["from"] = "employees"
    employees_accounts_dict = {}
    for account in accounts_dict:
        if accounts_dict[account].get_title() == "Employee":
            employees_accounts_dict[account] = accounts_dict[account]
    return render_template("manageemployees.html", users=employees_accounts_dict)

def delete_self():
    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    accounts_dict = {}
    db = shelve.open("storage.db", "c")
    try:
        accounts_dict = db["Accounts"]
    except:
        print("Error in retrieving Accounts from storage.db.")
    accounts_dict.pop(session["userID"])
    db["Accounts"] = accounts_dict
    db.close()
    del session["userID"]
    session["accSuccess"] = "Your account has been deleted"
    return redirect(url_for("login"))

def update_schedule(id):
    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    accounts_dict = {}
    db = shelve.open("storage.db", "c")
    try:
        accounts_dict = db["Accounts"]
    except:
        db.close()
        return redirect(url_for('home'))
    if accounts_dict[session["userID"]].get_title() != "Manager":
        db.close()
        return redirect(url_for('home'))
    account = accounts_dict.get(id)
    if account.get_title() != "Employee":
        db.close()
        return redirect(url_for('home'))
    form = EditScheduleForm(request.form)
    if request.method == "POST" and form.validate():
        dictionary = {}
        for field in form:
            label = field.id
            day = re.sub('\d', '', label)
            if not day in dictionary:
                dictionary[day] = []
            dictionary[day].append(field.data)
        session["accSuccess"] = "Schedule updated successfully"
        account.set_schedule(dictionary)
        accounts_dict[account.get_user_id()] = account
        db["Accounts"] = accounts_dict
        db.close()
        return redirect(url_for('update_schedule', id=id))
            
    else:
        for day in account.get_schedule():
            for timeslot in account.get_schedule()[day]:
                form[day + str(account.get_schedule()[day].index(timeslot))].data = account.get_schedule()[day][account.get_schedule()[day].index(timeslot)]
    return render_template("editschedule.html", user=account, form=form)

def create_employee():
    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    accounts_dict = {}
    db = shelve.open("storage.db", "c")
    try:
        accounts_dict = db["Accounts"]
    except:
        db.close()
        return redirect(url_for('home'))
    if accounts_dict[session["userID"]].get_title() != "Manager":
        db.close()
        return redirect(url_for('home'))
    create_employee_form = RegisterForm(request.form)
    if request.method == "POST" and create_employee_form.validate():

        already_registered = False
        for key in accounts_dict:
            if accounts_dict[key].get_email() == create_employee_form.email.data:
                already_registered = True

        if already_registered:
            db.close()
            session["accError"] = "Email already exists in our database"
            return redirect(url_for("create_employee"))
        loc = ""
        for location in tuple_list:
            if create_employee_form.working_location.data == location[0]:
                loc = location[1]
                break
        account = Account.Employee(create_employee_form.full_name.data, create_employee_form.address.data, create_employee_form.phone.data, create_employee_form.email.data, create_employee_form.password.data, {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}, create_employee_form.salary.data, loc, create_employee_form.nric.data)
        accounts_dict[account.get_user_id()] = account
        db["Accounts"] = accounts_dict

        db.close()

        session["accSuccess"] = "Account created"
        return redirect(url_for("manage_employees"))
    return render_template("register.html", form=create_employee_form)     

def update_account(id):
    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    accounts_dict = {}
    db = shelve.open("storage.db", "c")
    try:
        accounts_dict = db["Accounts"]
    except:
        db.close()
        return redirect(url_for('home'))
    if accounts_dict[session["userID"]].get_title() != "Manager":
        db.close()
        return redirect(url_for('home'))
    account = accounts_dict.get(id)
    form = EditProfileForm(request.form)
    if request.method == "POST" and form.validate():
        already_registered = False
        for key in accounts_dict:
            if key != account.get_user_id() and accounts_dict[key].get_email() == form.email.data:
                already_registered = True
        if already_registered:
            db.close()
            session["accError"] = "Email already exists in our database"
            return redirect(url_for("edit_profile"))
        account.set_full_name(form.full_name.data)
        account.set_address(form.address.data)
        account.set_phone(form.phone.data)
        account.set_email(form.email.data)
        if account.get_title() == "Employee":
            account.set_salary(form.salary.data)
            loc = ""
            for location in tuple_list:
                if form.working_location.data == location[0]:
                    loc = location[1]
                    break
            account.set_working_location(loc)
        accounts_dict[account.get_user_id()] = account
        db["Accounts"] = accounts_dict
        db.close()
        session["accSuccess"] = "Profile updated successfully"
        return redirect(url_for("update_account", id=id))
    else:
        form.full_name.data = account.get_full_name()
        form.address.data = account.get_address()
        form.phone.data = account.get_phone()
        form.email.data = account.get_email()
        if account.get_title() == "Employee":
            form.salary.data = account.get_salary()
            form.working_location.data = account.get_working_location().replace(" ", "")
    return render_template("editprofile.html", user=account, form=form)

def delete_account(id):
    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    db = shelve.open('storage.db', 'c')
    try:
        accounts_dict = db["Accounts"]
    except:
        db.close()
        return redirect(url_for('home'))
    if accounts_dict[session["userID"]].get_title() != "Manager":
        db.close()
        return redirect(url_for('home'))
    accounts_dict = {}
    try:
        accounts_dict = db["Accounts"]
    except:
        print("Error in retrieving Accounts from storage.db.")
    account = accounts_dict[id]
    accounts_dict.pop(id)
    db["Accounts"] = accounts_dict
    db.close()
    session["user_deleted"] = account.get_full_name() + " has been deleted."
    if "from" in session and session["from"] == "employees":
        return redirect(url_for("manage_employees"))
    return redirect(url_for("manage_accounts"))

def change_password():
    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    accounts_dict = {}
    db = shelve.open("storage.db", "c")
    try:
        accounts_dict = db["Accounts"]
    except:
        print("Error in retrieving Accounts from storage.db.")
    account = accounts_dict.get(session["userID"])
    change_password_form = ChangePasswordForm(request.form)
    if request.method == "POST" and change_password_form.validate():
        if not account.check_password(change_password_form.current_password.data):
            db.close()
            session["accError"] = "Current password does not match with our records"
            return redirect(url_for("change_password"))
        if change_password_form.new_password.data != change_password_form.confirm_password.data:
            db.close()
            session["accError"] = "New password does not match confirm password"
            return redirect(url_for("change_password"))
        if account.check_password(change_password_form.new_password.data):
            db.close()
            session["accError"] = "New password cannot be the same as your current one"
            return redirect(url_for("change_password"))
        account.set_password(change_password_form.new_password.data)
        accounts_dict[account.get_user_id()] = account
        db["Accounts"] = accounts_dict
        db.close()
        session["accSuccess"] = "Password has been updated"
        return redirect(url_for("change_password"))
    return render_template("changepassword.html", form=change_password_form)

def careers():
    create_application = CreateApplicationForm(request.form)
    if request.method == "POST" and create_application.validate():

        applicants = {}
        currentDict = {}
        currentID = 0
        db = shelve.open('storage.db', 'c')
        try:
            applicants = db["Applicants"]
            currentID = db["ApplicantsID"]
        except:
            print("No applicants! Creating a new one...")

        name = create_application.name.data
        age = create_application.age.data
        phoneNo = create_application.phoneNo.data
        email = create_application.email.data
        location = create_application.location.data
        commitmentPeriod = create_application.commitmentPeriod.data
        currentID += 1

        myDict = {"name": name, "age": age, "phoneNo": phoneNo, "email": email, "location": location, "commitmentPeriod": commitmentPeriod}
        applicants[currentID] = myDict
        db["Applicants"] = applicants
        db["ApplicantsID"] = currentID

        session["accSuccess"] = "Application submitted successfully! We will get back to you soon."
        return redirect(url_for('careers'))  # brings user to home page
    return render_template('createApplication.html', form=create_application)

def view_applicants():
    db = shelve.open('storage.db', 'c')

    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    acc_db = shelve.open('storage.db', 'c')
    try:
        accounts = acc_db["Accounts"]
    except:
        print("Error in retrieving accounts from storage.db")
    for key in accounts:
        if accounts[key].get_user_id() == session["userID"]:
            account = accounts[key]
            break
    
    if account.get_title() != "Manager":
        return redirect(url_for("home"))

    try:
        applicants = db["Applicants"]
    except:
        print("There are no applicants!")

    return render_template('viewApplicants.html', applicants=applicants)

def update_applicants(id):
    db = shelve.open('storage.db', 'c')

    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    acc_db = shelve.open('storage.db', 'c')
    try:
        accounts = acc_db["Accounts"]
    except:
        print("Error in retrieving accounts from storage.db")
    for key in accounts:
        if accounts[key].get_user_id() == session["userID"]:
            account = accounts[key]
            break
    
    if account.get_title() != "Manager":
        return redirect(url_for("home"))

    applicants = {}
    try:
        applicants = db["Applicants"]
    except:
        print("There are no applicants!")

    update_applicant = CreateApplicationForm(request.form)
    if request.method == "POST" and update_applicant.validate():
        name = update_applicant.name.data
        age = update_applicant.age.data
        phoneNo = update_applicant.phoneNo.data
        email = update_applicant.email.data
        location = update_applicant.location.data
        commitmentPeriod = update_applicant.commitmentPeriod.data

        myDict = {"name": name, "age": age, "phoneNo": phoneNo, "email": email, "location": location,
                  "commitmentPeriod": commitmentPeriod}
        applicants[id] = myDict
        db["Applicants"] = applicants
        db.close()
    else:
        applicants = db["Applicants"]
        x = applicants[id]
        name = x["name"]
        age = x["age"]
        phoneNo = x["phoneNo"]
        email = x["email"]
        location = x["location"]
        commitmentPeriod = x["commitmentPeriod"]

        update_applicant.name.data = name
        update_applicant.age.data = age
        update_applicant.phoneNo.data = phoneNo
        update_applicant.email.data = email
        update_applicant.location.data = location
        update_applicant.commitmentPeriod.data = commitmentPeriod

        return render_template("updateApplicants.html", form=update_applicant)

    return redirect(url_for("view_applicants"))

def delete_applicant(id):
    db = shelve.open('storage.db', 'c')

    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    acc_db = shelve.open('storage.db', 'c')
    try:
        accounts = acc_db["Accounts"]
    except:
        print("Error in retrieving accounts from storage.db")
    for key in accounts:
        if accounts[key].get_user_id() == session["userID"]:
            account = accounts[key]
            break
    
    if account.get_title() != "Manager":
        return redirect(url_for("home"))

    try:
        applicants = db["Applicants"]
    except:
        print("No one applied :(")

    applicants.pop(id)

    db["Applicants"] = applicants

    return redirect(url_for("view_applicants"))
