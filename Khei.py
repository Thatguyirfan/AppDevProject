import Order, shelve, datetime

from flask import render_template, request, session, redirect, url_for

from Forms import CreateUpdateOrderForm

def add_to_cart(id):
    products = {}
    db = shelve.open('products.db', 'w')  # getting product_dict
    try:
        products = db["Products"]
    except:
        print("Error in retrieving products from storage.db")
    product_info = products[id]

    cart_list = []  # list consists of productID added into cart
    if "Cart" in session:  # checking if any session existed
        print("Found cart")
        cart_list = session["Cart"]
    else:
        print("New cart created")
    cart_list.append(id)
    session["Cart"] = cart_list
    db.close()

    total = 0
    viewCartList = []
    # x = 0

    for i in cart_list:
        productObject = product_info
        if productObject not in viewCartList:
            viewCartList.append(productObject)
        
        price_Item = productObject.get_price()
        total += price_Item

    print("the cart total is ", total)
    return redirect(url_for("cartPage"))

# does pretty much the same thing as add_to_cart
def addQuantity(id):
    products = {}
    db = shelve.open('products.db', 'r')
    try:
        products = db["Products"]
    except:
        print("Error in retrieving products from storage.db")
    product_info = products[id]

    cart_list = []  # list consists of productID added into cart
    if "Cart" in session:  # checking if any session existed
        print("Found cart")
        cart_list = session["Cart"]
    else:
        print("New cart created")
    cart_list.append(id)
    session["Cart"] = cart_list
    db.close()

    total = 0
    viewCartList = []
    # x = 0

    for i in cart_list:
        productObject = product_info
        if productObject not in viewCartList:
            viewCartList.append(productObject)
        
        price_Item = productObject.get_price()
        total += price_Item
        # x += 1

    print("the cart total is ", total)
    return redirect(url_for("cartPage"))

def minusQuantity(id):
    products = {}
    db = shelve.open('products.db', 'r')
    try:
        products = db["Products"]
    except:
        print("Error in retrieving products from storage.db")
    product_info = products[id]
  

    cart_list = []
    if "Cart" in session:
        print("Found cart")
        cart_list = session["Cart"]
    else:
        print("New cart created")
    cart_list.remove(id)  # cannot use pop cause of index error
    session["Cart"] = cart_list

    products = db["Products"]
    db.close()

    total = 0
    viewCartList = []
    # x = 0

    for i in cart_list:
        productObject = product_info
        if productObject not in viewCartList:
            viewCartList.append(productObject)
        
        price_Item = productObject.get_price()
        total += price_Item
        # x += 1

    print("the cart total is ", total)
    return redirect(url_for("cartPage"))

def delete_item(id):
    products = {}
    db = shelve.open('products.db', 'r')
    try:
        products = db["Products"]
    except:
        print("Error in retrieving products from storage.db")
    product_info = products[id]

    cart_list = []
    if "Cart" in session:
        print("Found cart")
        cart_list = session["Cart"]
    else:
        print("New cart created")
    for i in cart_list:
        if id in cart_list:
            cart_list.remove(id)
    for i in cart_list:
        if id in cart_list:
            cart_list.remove(id)
    session["Cart"] = cart_list

    # check if item is deleted
    print(cart_list)

    db.close()

    total = 0
    viewCartList = []
    # x = 0

    for i in cart_list:
        productObject = product_info
        if productObject not in viewCartList:
            viewCartList.append(productObject)
        
        price_Item = productObject.get_price()
        total += price_Item
        # x += 1

    print("the cart total is ", total)
    return redirect(url_for("cartPage"))

def clear_cart():
    cart_list = []
    if "Cart" in session:
        print("Found cart")
        cart_list = session["Cart"]
    else:
        print("New cart created")
    for i in cart_list:
        print("clearing cart")
        cart_list.clear()
    session["Cart"] = cart_list

    return redirect(url_for("cartPage"))

def cartPage():
    cart_list = []
    if "Cart" in session:
        print("Found cart")
        cart_list = session["Cart"]
    else:
        print("New cart created")

    products = {}
    db = shelve.open('products.db', 'w')
    try:
        products = db["Products"]
    except:
        print("Error in retrieving products from storage.db")
    db.close()

    total = 0
    viewCartList = []
    # x = 0

    current_quantity = {}

    for x, i in enumerate(cart_list):
        currentProductID = cart_list[x]
        productObject = products[currentProductID]
        if productObject not in viewCartList:
            viewCartList.append(productObject)
        
        price_Item = productObject.get_price()
        total += price_Item

        if currentProductID not in current_quantity:
            current_quantity[currentProductID] = 0
        current_quantity[currentProductID] += 1
        # x += 1

    print("the cart total is ", total)
    return render_template("Cart.html", count=len(cart_list), viewCartList = viewCartList, total=total, current_quantity=current_quantity)


def checkOut_page():
    if "userID" not in session:
        session["accError"] = "Please log in first"
        session["returnToCart"] = True
        return redirect(url_for("login"))
    acc_db = shelve.open('storage.db', 'r')
    accounts = {}
    try:
        accounts = acc_db["Accounts"]
    except:
        print("Error in retrieving accounts from storage.db")
    acc_db.close()
    for key in accounts:
        if accounts[key].get_user_id() == session["userID"]:
            account = accounts[key]
            break
    if account.get_title() in ["Manager", "Employee"]:
        return redirect(url_for("dashboard"))
    cart_list = []
    if "Cart" in session:
        print("Found cart")
        cart_list = session["Cart"]
    else:
        print("New cart created")

    products = {}
    db = shelve.open('products.db', 'w')
    try:
        products = db["Products"]
    except:
        print("Error in retrieving products from storage.db")
    db.close()

    total = 0
    # x = 0
    current_quantity = {}
    for x, i in enumerate(cart_list):
        current_product = products[cart_list[x]]
        price_Item = current_product.get_price()
        total += price_Item
        if current_product.get_id() not in current_quantity:
            current_quantity[current_product.get_id()] = 0
        current_quantity[current_product.get_id()] += 1
        # x += 1

    return render_template("checkOut.html",products=products,current_quantity=current_quantity, count=len(cart_list), total=total, user=account)

def customerInfo():
    if "Cart" not in session or len(session["Cart"]) == 0:
        return redirect(url_for("dashboard"))
    if "userID" not in session:
        session["accError"] = "Please log in first"
        session["returnToCart"] = True
        return redirect(url_for("login"))
    acc_db = shelve.open('storage.db', 'c')
    accounts = {}
    try:
        accounts = acc_db["Accounts"]
    except:
        print("Error in retrieving accounts from storage.db")
    for key in accounts:
        if accounts[key].get_user_id() == session["userID"]:
            account = accounts[key]
            break
        # im not sure which data you need
    name = request.form['name']
    email = request.form['email']
    print(name,email)

    # update quantity in products

    cart_list = []
    if "Cart" in session:
        print("Found cart")
        cart_list = session["Cart"]
    else:
        print("New cart created")

    product_dict = {}
    db = shelve.open('products.db', 'w')
    try:
        product_dict = db["Products"]
    except:
        print("Error in retrieving products from storage.db")
    db['Products'] = product_dict
    product_info = db['Products']
    db.close()

    id_list = []
    for i in cart_list:
      id_list.append(i) 

    for i in id_list:
      product_object = product_dict[i]
      instocks = product_object.get_instocks()
      q = instocks["WH"]
      instocks["WH"] = q - 1

    # store orders into shelve with order id

    order_dict = {}
    db2 = shelve.open('orders.db', 'c')
    try:
      order_dict = db2["Orders"]
    except:
      print("Error in retrieving products from orders.db")
    
    order_list = []
    for id in cart_list:
      items = product_info[id]
      order_list.append(items)

    total = 0
    # x = 0
    for x, i in enumerate(cart_list):
        price_Item = product_info[cart_list[x]].get_price()
        total += price_Item
        # x += 1

    # order object in checkou or customerInfo?
    delivery_status = "Packing"
    orderDate = datetime.datetime.today().strftime('%Y-%m-%d')
    order = Order.Order(delivery_status, orderDate, total, session["userID"])
    order_id = order.get_current_id()
    order_list.append(order) # order_list contains both products and order object
    order_dict[order_id] = order_list
    print(order_dict)
    db2["Orders"] = order_dict
    db2.close()
    account.add_spent(total)
    account.add_purchase_history(order_list)
    accounts[account.get_user_id()] = account
    acc_db["Accounts"] = accounts
    acc_db.close()


    #clear cart
    cart_list = []
    if "Cart" in session:
        print("Found cart")
        cart_list = session["Cart"]
    else:
        print("New cart created")
    for i in cart_list:
        print("clearing cart")
        cart_list.clear()
    session["Cart"] = cart_list

    # current_quantity = {}
    # db1 = shelve.open('quantity.db', 'w')
    # current_quantity = db1["indiv_quantity"]
    # current_quantity.clear()
    # db1["indiv_quantity"] = current_quantity
    # db1.close()
    print("paid")

    return render_template("thankyou.html")
  
def view_order():
    if "userID" not in session:
        session["accError"] = "Please log in first"
        session["returnToCart"] = True
        return redirect(url_for("login"))
    acc_db = shelve.open('storage.db', 'r')
    accounts = {}
    try:
        accounts = acc_db["Accounts"]
    except:
        print("Error in retrieving accounts from storage.db")
    acc_db.close()
    for key in accounts:
        if accounts[key].get_user_id() == session["userID"]:
            account = accounts[key]
            break
    order_dict = {}
    update_form = CreateUpdateOrderForm(request.form)
    
    db2 = shelve.open('orders.db', 'c')
    try:
        order_dict = db2["Orders"]   # order_dict[orderid] = [productObject, orderObject]
    except:
        print("Error in retrieving products from orders.db")

    full_order_list = []
    for key in order_dict:
        if account.get_title() == "Manager" or order_dict[key][-1].get_customer_id() == account.get_user_id():
            full_order_list.append(order_dict[key])

    id_list = []
    for i in full_order_list:
        id_list.append(i[-1].get_current_id())
    
    db2.close()

    return render_template("viewOrder.html", update_form=update_form, order_dict=order_dict, full_order_list=full_order_list, user=account)

def update_order(id):
  form = CreateUpdateOrderForm(request.form)

  order_dict = {}
  db = shelve.open('orders.db', 'c')
  try:
        order_dict = db['Orders']
  except:
        print('Error in retrieving Orders form orders.db')

  if request.method == "POST" and form.validate():
        order_dict[id][-1].set_delivery_status()
        db['Orders'] = order_dict
        db.close()

        return redirect(url_for('view_order'))
  else:
        form.id.data = id
        form.order_date.data = order_dict[int(id)][-1].get_orderDate()
  return render_template("updateOrder.html", id=id, form=form)
