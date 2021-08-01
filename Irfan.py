import Customer, datetime, shelve, Feedback

from flask import render_template, request, redirect, url_for, session

from Forms import StoreEntry, GetCount, ChooseRecords, RecordsFilter, FeedbackForm, FeedbackFilter

from Stores import tuple_list

def store_entry():
    if "instore" in session:
        return redirect(url_for('store_entry_details', store=session["instore"]["store"], id=session["instore"]["nric"]))
    store_entry_form = StoreEntry(request.form)
    now = datetime.datetime.now()
    current_date = now.strftime("%a, %d/%m/%Y")
    current_time = now.strftime("%H:%M")

    if request.method == "POST" and store_entry_form.validate():
        store_dict = {}
        cust_dict = {}
        # conversion
        db = shelve.open('storage.db', 'c')
        try:
            store_dict = db["Stores"]
            cust_dict = store_dict[store_entry_form.store.data]
        except:
            print('Error in retrieving Stores from storage.db')

        if store_entry_form.nric.data in cust_dict:
          count = 0
          for key in cust_dict:
            if key[:10] == store_entry_form.nric.data:
              count += 1

          nric = store_entry_form.nric.data + "(" + str(count) + ")"
          nric = nric.upper()

        else:
          nric = store_entry_form.nric.data
          nric = nric.upper()

        accounts_dict = db["Accounts"]
        is_employee = False
        employee_id = ""
        store_name = ""
        for store in tuple_list:
            if store[0] == store_entry_form.store.data:
                store_name = store[1]
                break
        for acc in accounts_dict:
            if accounts_dict[acc].get_title() == "Employee" and accounts_dict[acc].get_nric() == store_entry_form.nric.data.upper() and accounts_dict[acc].get_working_location() == store_name:
                is_employee = True
                employee_id = acc
                break

        title = "Employee" if is_employee else "Customer"

        customer = Customer.Customer(store_entry_form.nric.data,
                                     store_entry_form.temperature.data,
                                     store_entry_form.entrytime.data,
                                     store_entry_form.date.data,
                                     store_entry_form.mobile.data,
                                     title)
        cust_dict[nric] = customer
        store_dict[store_entry_form.store.data] = cust_dict
        db["Stores"] = store_dict
        db.close()

        session["instore"] = {"nric": nric, "store": store_entry_form.store.data}
        if is_employee:
            session["instore"]["employee_id"] = employee_id

        return redirect(url_for('store_entry_details', store=store_entry_form.store.data, id=nric))

    return render_template('storeentry.html', store_entry_form=store_entry_form, date=current_date, entrytime=current_time)

def store_entry_details(store, id):
    if "instore" in session:
        db = shelve.open('storage.db', 'c')
        store_dict = db["Stores"]
        accounts_dict = db["Accounts"]
        cus_dict = store_dict[store]
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        date = cus_dict[id.upper()].get_date()
        entrytime = cus_dict[id.upper()].get_entrytime()

        if request.method == 'POST':
            cus_dict[id.upper()].set_exittime(current_time)

            store_dict[store] = cus_dict
            db["Stores"] = store_dict
            db["Accounts"] = accounts_dict
            if "employee_id" in session["instore"]:
                checked_in = datetime.datetime.strptime(cus_dict[id.upper()].get_entrytime(), "%H:%M")
                checked_out = datetime.datetime.strptime(cus_dict[id.upper()].get_exittime(), "%H:%M")
                hours_clocked = checked_out - checked_in
                hours = hours_clocked.seconds / 3600
                employee = accounts_dict[session["instore"]["employee_id"]]
                employee.add_hours_clocked(hours)
                accounts_dict[session["instore"]["employee_id"]] = employee
                db["Accounts"] = accounts_dict

            try:
                session.pop("instore")
                db.close()

            except:
                return redirect(url_for('home'))

            return redirect(url_for('home'))
        return render_template('storeexit.html', store=store, id=id, date=date, entrytime=entrytime)
    return redirect(url_for('home'))

def store_count():
    form = GetCount(request.form)
    if request.method == "POST":
        store = form.store.data
        day = form.day.data

        return redirect(url_for('retrieve_count', store=store, day=day))
    return render_template("storecount.html", form=form)

def retrieve_count():
    form = GetCount(request.form)
    store = request.args.get('store', None)
    day = request.args.get('day', None)
    db = shelve.open('storage.db', 'r')
    store_dict = db["Stores"]
    try:
        cus_dict = store_dict[store]
        db.close()
    except:
        return redirect(url_for('home'))

    fullcuslist = []
    for key in cus_dict:
        customer = cus_dict.get(key)
        fullcuslist.append(customer)

    time_dict = {}
    for i in range(0, 24):
      count = 0
      weeks = 0
      check_date = ''
      try:
        for cus in fullcuslist:
            date = datetime.datetime.strptime(cus.get_date(), "%a, %d/%m/%Y")
            if date.strftime("%a") == day:
              time = datetime.datetime.strptime(cus.get_entrytime(), "%H:%M")
              if int(time.strftime("%H")) == i:
                if float(cus.get_temperature()) <= 37.4:
                  count += 1
                  if date != check_date:
                    weeks += 1
                    check_date = date
        
        avg_count = count / weeks
        time_dict[i] = avg_count

      except ZeroDivisionError:
        time_dict[i] = count
            
    labels = []
    series = []
    for i in time_dict:
      labels.append(i)
      series.append(time_dict[i])
    
    if request.method == "POST":
      newstore = form.store.data
      newday = form.day.data


      return redirect(url_for('retrieve_count', store=newstore, day=newday))
    return render_template("showstorecount.html", form=form,  st=labels, count_list=series)

def choose_records():
    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    db = shelve.open('storage.db', 'r')
    try:
        accounts_dict = db["Accounts"]
    except:
        db.close()
        return redirect(url_for('home'))
    if accounts_dict[session["userID"]].get_title() not in ["Employee", "Manager"]:
        db.close()
        return redirect(url_for('home'))
    form = ChooseRecords(request.form)
    if request.method == "POST":
        store = form.store.data

        return redirect(url_for('retrieve_records', store=store))
    return render_template("chooseentryrecord.html", form=form)

def retrieve_records(store):
    filter_form = RecordsFilter(request.form)
    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    db = shelve.open('storage.db', 'r')
    try:
        accounts_dict = db["Accounts"]
    except:
        db.close()
        return redirect(url_for('home'))
    if accounts_dict[session["userID"]].get_title() not in ["Employee", "Manager"]:
        db.close()
        return redirect(url_for('home'))
    try:
        key_list = []
        store_dict = db["Stores"]
        if store in store_dict:
            cus_dict = store_dict[store]
            for key in cus_dict:
              key_list.append(key)
            key_list.reverse()
        else:
            cus_dict = {}
    except:
        store_dict = {}
        cus_dict = {}
        print("error retrieving store dict")
    db.close()
    loc = ""
    for location in tuple_list:
        if store == location[0]:
            loc = location[1]
            break
            
    if request.method == "POST":
        filter = filter_form.filter.data
        if filter == "Customers":
          for cus in cus_dict:
            if cus_dict[cus].get_title() != "Customer":
              key_list.remove(cus)

        elif filter == "Employees":
          for employee in cus_dict:
            if cus_dict[employee].get_title() != "Employee":
              key_list.remove(employee)

    return render_template('entryrecords.html', cus_dict=cus_dict, store=store, key_list=key_list, loc=loc, filter_form=filter_form, filter=filter_form.filter.data)

# def update_user(store, id):
#     if "userID" not in session:
#         session["accError"] = "Please log in first"
#         return redirect(url_for("login"))
#     db = shelve.open('storage.db', 'c')
#     try:
#         accounts_dict = db["Accounts"]
#     except:
#         db.close()
#         return redirect(url_for('home'))
#     if accounts_dict[session["userID"]].get_title() not in ["Employee", "Manager"]:
#         db.close()
#         return redirect(url_for('home'))
#     form = UpdateCustomer(request.form)
#     now = datetime.datetime.now()
#     current_date = now.strftime("%a, %d/%m/%Y")
#     current_time = now.strftime("%H:%M")

#     if request.method == 'POST' and form.validate():
#         store_dict = {}
#         try:
#             store_dict = db["Stores"]
#             cus_dict = store_dict[form.store.data]
#         except:
#             print('Error in retrieving Stores from storage.db')

#         cus_dict[id].set_temperature(form.temperature.data)
#         cus_dict[id].set_mobile(form.mobile.data)

#         store_dict[form.store.data] = cus_dict
#         db["Stores"] = store_dict
#         db.close()

#         session['user_updated'] = 'Customer'

#         return redirect(url_for('retrieve_records', store=store))
#     return render_template('updatecustomer.html', form=form, date=current_date, time=current_time, store=store, id=id)

def delete_customer(store, id):
    if "userID" not in session:
        session["accError"] = "Please log in first"
        return redirect(url_for("login"))
    db = shelve.open('storage.db', 'c')
    try:
        accounts_dict = db["Accounts"]
    except:
        db.close()
        return redirect(url_for('home'))
    if accounts_dict[session["userID"]].get_title() not in ["Employee", "Manager"]:
        db.close()
        return redirect(url_for('home'))
    store_dict = db["Stores"]
    cus_dict = store_dict[store]

    try:
        cus_dict.pop(id)
    except KeyError:
        return redirect(url_for('retrieve_records', store=store))
    store_dict[store] = cus_dict
    db["Stores"] = store_dict
    db.close()

    session['user_deleted'] = 'Customer'

    return redirect(url_for('retrieve_records', store=store))

def feedback():
    feedback_form = FeedbackForm(request.form)
    now = datetime.datetime.now()
    current_date = now.strftime("%a, %d/%m/%Y")

    feedback_dict = {}
    db = shelve.open('storage.db', 'c')
    try:
      feedback_dict = db['Feedback']
    except:
      print('Error in retrieving Feedback from storage.db')

    if request.method == 'POST' and feedback_form.validate():
      feedback = Feedback.Feedback(feedback_form.name.data, 
                                  feedback_form.mobile.data, 
                                  feedback_form.email.data, 
                                  feedback_form.reason.data, 
                                  feedback_form.message.data,
                                  current_date,
                                  feedback_form.store.data)

      if len(feedback_dict) == 0:
        feedback_dict[1] = feedback
      else:
        feedback_number = len(feedback_dict) + 1
        feedback_dict[feedback_number] = feedback

      db['Feedback'] = feedback_dict
      db.close()
      print(feedback_dict)

      return redirect(url_for('feedback_ack'))
    return render_template('feedback.html', feedback_form=feedback_form)


def feedback_ack():
  return render_template('feedback_ack.html')


def view_feedback():

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

    filter_form = FeedbackFilter(request.form)

    feedback_dict = db['Feedback']

    db.close()
    feedback_list = []
    for key in feedback_dict:
        feedback_list.append(feedback_dict[key])
    feedback_list.reverse()

    filter_list = []
    if request.method == "POST":
        store = filter_form.store.data
        reason = filter_form.reason.data
        
        loc = ""
        for location in tuple_list:
          if store == location[1]:
            loc = location[0]
            break

        if store != "All" and reason != "All":
          for i in feedback_list:
            if i.get_store() == loc:
              filter_list.append(i)

            for i in filter_list:
              if i.get_reason() != reason:
                filter_list.remove(i)

        elif store != "All":
          for i in feedback_list:
            if i.get_store() == loc:
              filter_list.append(i)

        elif reason != "All":
          for i in feedback_list:
            if i.get_reason() == reason:
                filter_list.append(i)

    filter_list.reverse()

    return render_template('viewFeedback.html', filter_form=filter_form, feedback_list=feedback_list, store_filter=filter_form.store.data, reason_filter=filter_form.reason.data, filter_list=filter_list)
