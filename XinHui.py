import Product, shelve, operator

from flask import render_template, request, redirect, url_for, session, flash

from Forms import CreateProductForm, CreateRestockForm

def viewAll():
    db = shelve.open('products.db', 'r')
    product_dict = db["Products"]
    db.close()

    product_list = []
    for key in product_dict:
        product = product_dict[key]
        product_list.append(product)

    return render_template('allProducts.html', count=len(product_list), product_list=product_list)

def search():
    search_str = request.form['search']
    print("user input: ", search_str)

    db = shelve.open('products.db', 'r')
    product_dict = db["Products"]
    db.close()

    product_list = []
    for key in product_dict:
        product = product_dict[key]
        product.set_Name()
        product_list.append(product)

    for i in product_list:
        print(i.set_split())

    filter_list = []
    for i in product_list:
        if search_str.lower() in i.set_split():
            filter_list.append(i)
        else:
            print("search not in list")

    if len(filter_list) > 0:
        product_list.clear()
        for i in filter_list:
            product_list.append(i)

    return render_template('allProducts.html', product_list=product_list)

def low_to_high():
    db = shelve.open('products.db', 'r')
    product_dict = db["Products"]
    db.close()

    product_list = []
    for key in product_dict:
        product = product_dict[key]
        product.set_Price()
        product_list.append(product)
        print(product)

    product_list.sort(key=operator.attrgetter('price'))

    return render_template('allProducts.html', product_list=product_list)

def high_to_low():
    db = shelve.open('products.db', 'r')
    product_dict = db["Products"]
    db.close()

    product_list = []
    for key in product_dict:
        product = product_dict[key]
        product.set_Price()
        product_list.append(product)
        print(product)

    product_list.sort(key=operator.attrgetter('price'), reverse=True)

    return render_template('allProducts.html', product_list=product_list)

def a_to_z():
    db = shelve.open('products.db', 'r')
    product_dict = db["Products"]
    db.close()

    product_list = []
    for key in product_dict:
        product = product_dict[key]
        product.set_Name()
        product_list.append(product)
        print(product)

    product_list.sort(key=operator.attrgetter('name'))

    return render_template('allProducts.html', product_list=product_list)

def z_to_a():
    db = shelve.open('products.db', 'r')
    product_dict = db["Products"]
    db.close()

    product_list = []
    for key in product_dict:
        product = product_dict[key]
        product.set_Name()
        product_list.append(product)
        print(product)

    product_list.sort(key=operator.attrgetter('name'), reverse=True)

    return render_template('allProducts.html', product_list=product_list)

def newest():
    db = shelve.open('products.db', 'r')
    product_dict = db["Products"]
    db.close()

    product_list = []
    for key in product_dict:
        product = product_dict[key]
        product.set_Name()
        product_list.append(product)
        print(product)

    product_list.reverse()

    return render_template('allProducts.html', product_list=product_list)

def view_individual(id):
    product_dict = {}

    db = shelve.open('products.db', 'c')
    # check if the storage.db exists
    try:
        product_dict = db["Products"]
    except:
        print("Error in retrieving products from storage.db")

    product_info = product_dict[id]

    return render_template('individual.html', product_info=product_info)

def view_product():
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

    
    db = shelve.open('products.db', 'r')
    product_dict = {}

        # check if the storage.db exists
    try:
      product_dict = db["Products"]
    except:
      print("Error in retrieving products from storage.db")

    product_list = []
    for key in product_dict:
        product = product_dict.get(key)
        product_list.append(product)
        print(key, product_dict[key], "len", len(product_list))

    for i in product_list:
        print(i)

    return render_template('viewProduct.html', count=len(product_list), product_list=product_list)

def create_product():
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

    create_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and create_product_form.validate():
        db = shelve.open('products.db', 'c')
        product_dict = {}

        # check if the storage.db exists
        try:
            product_dict = db["Products"]
        except:
            print("Error in retrieving products from storage.db")

        # check if the product data already exists
        if create_product_form.name.data in product_dict:
            flash("Product already exists! Updating data...")
            db.close()
            return redirect(update_product)

        instocks = {}
        WH = create_product_form.instocks_WH.data
        CQ = create_product_form.instocks_CQ.data
        Orchard = create_product_form.instocks_Orchard.data
        CitySq = create_product_form.instocks_CitySq.data
        Sq2 = create_product_form.instocks_Sq2.data
        HundredAM = create_product_form.instocks_100AM.data
        JCube = create_product_form.instocks_JCube.data
        Jem = create_product_form.instocks_Jem.data

        instocks['WH'] = WH
        instocks['CQ'] = CQ
        instocks['Orchard'] = Orchard
        instocks['CitySq'] = CitySq
        instocks['Sq2'] = Sq2
        instocks['HundredAM'] = HundredAM
        instocks['JCube'] = JCube
        instocks['Jem'] = Jem

        c = Product.Product(create_product_form.name.data, create_product_form.description.data,
                            create_product_form.ingredients.data,
                            create_product_form.price.data, instocks, create_product_form.category.data,
                            create_product_form.img.data)

        print("category assigned:", c.get_category())
        print(c.get_instocks())

        product_dict[c.get_id()] = c

        db["Products"] = product_dict

        #  test codes
        product_dict = db["Products"]

        product = product_dict[c.get_id()]
        print(product.get_name(), "was stored in storage.db successfully with user_id ===", product.get_id())

        db.close()

        return redirect(url_for("dashboard"))

    return render_template('createProduct.html', form=create_product_form)

def update_product(id):
# mx's validation
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

# actual update product section
    update_product_form = CreateProductForm(request.form)

    if request.method == "POST" and update_product_form.validate():
        db = shelve.open('products.db', 'c')
        product_dict = {}

        # check if the storage.db exists
        try:
            product_dict = db["Products"]
        except:
            print("Error in retrieving products from products.db")

        instocks = {}
        WH = update_product_form.instocks_WH.data
        CQ = update_product_form.instocks_CQ.data
        Orchard = update_product_form.instocks_Orchard.data
        CitySq = update_product_form.instocks_CitySq.data
        Sq2 = update_product_form.instocks_Sq2.data
        HundredAM = update_product_form.instocks_100AM.data
        JCube = update_product_form.instocks_JCube.data
        Jem = update_product_form.instocks_Jem.data

        instocks["WH"] = WH
        instocks['CQ'] = CQ
        instocks['Orchard'] = Orchard
        instocks['CitySq'] = CitySq
        instocks['Sq2'] = Sq2
        instocks['HundredAM'] = HundredAM
        instocks['JCube'] = JCube
        instocks['Jem'] = Jem

        product = product_dict.get(id)
        product.set_name(update_product_form.name.data)
        product.set_desc(update_product_form.description.data)
        product.set_ingredients(update_product_form.ingredients.data)
        product.set_instocks(instocks)
        product.set_price(update_product_form.price.data)
        product.set_category(update_product_form.category.data)
        product.set_img(update_product_form.img.data)

        print(product.get_instocks())

        db['Products'] = product_dict
        db.close()

        return redirect(url_for("view_product"))
  
    else:
        product_dict = {}
        db = shelve.open('products.db', 'r')
        product_dict = db['Products']
        db.close()

        product = product_dict.get(id)
        instocks = product.get_instocks()
        update_product_form.name.data = product.get_name()
        update_product_form.description.data = product.get_desc()
        update_product_form.ingredients.data = product.get_ingredients()
        
        update_product_form.instocks_WH.data = instocks["WH"]
        update_product_form.instocks_CQ.data = instocks["CQ"]
        update_product_form.instocks_Orchard.data = instocks["Orchard"]
        update_product_form.instocks_CitySq.data = instocks["CitySq"]
        update_product_form.instocks_Sq2.data = instocks["Sq2"]
        update_product_form.instocks_100AM.data = instocks["HundredAM"]
        update_product_form.instocks_JCube.data = instocks["JCube"]
        update_product_form.instocks_Jem.data = instocks["Jem"]
        update_product_form.price.data = product.get_price()
        update_product_form.category.data = product.get_category()
        update_product_form.img.data = product.get_img()

        return render_template("updateProduct.html", form=update_product_form)

def delete_product(id):
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

    db = shelve.open('products.db', 'c')
    product_dict = {}

        # check if the storage.db exists
    try:
      product_dict = db["Products"]
    except:
      print("Error in retrieving products from storage.db")

    product_dict.pop(id)

    db['Products'] = product_dict
    db.close()

    return redirect(url_for("view_product"))

# ordering process of stocks
def order_instocks():

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

    create_instock = CreateRestockForm(request.form)
    if request.method == 'POST' and create_instock.validate():
        db = shelve.open('products.db', 'c')
        product_dict = {}
        supplierOrder_dict = {}
        currentID = 0

        # check if the storage.db exists
        try:
            product_dict = db["Products"]
        except:
            print("Products not in shelve")

        # get session["Supplier"]
        try:
            supplierOrder_dict = db["currentSupplier"]
            # current supplier session consists of dictionary consisting: productObject_id, productName, quantity and where to add quantity to
        except:
            print("There is currently nothing in session. Adding new session...")

        # getting productObject
        productObject_id = int(create_instock.product.data)
        productObject = product_dict.get(productObject_id)
        print("Chosen product's object is:",
              productObject.get_name())  # still can leave this here to confirm that the chosen object is correct tho

        # get sessionID
        try:
            currentID = db["ID"]
        except:
            print("no ID, creating one rn")
        else:
            print("ID found. old ID is", currentID)

        currentID += 1
        db["ID"] = currentID
        print("new ID is", db["ID"])

        supplierOrder_dict[currentID] = {"productObjectID": productObject_id, "productName": productObject.get_name(),
                                         "quantity": create_instock.quantity.data,
                                         "send_to": create_instock.send_to.data}  # order_id: ORDER DETAILS IN DICTIONARY
        db["currentSupplier"] = supplierOrder_dict

        for key, value in db["currentSupplier"].items():  # check if saved in shelve
            print("Product successfully stored in session:",
                  value["productName"])  # key is order id, value is the order object
            print(key)
        print("new order entry created!")

        return redirect(url_for("view_SupplierOrder"))

    return render_template('order_instocks.html', form=create_instock)

def update_supplierOrder(id):

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

    update_order = CreateRestockForm(request.form)
    if request.method == "POST" and update_order.validate():
        supplier_dict = {}
        product_dict = {}
        db = shelve.open('products.db', 'w')
        try:
            product_dict = db["Products"]
            supplier_dict = db['currentSupplier']  # current supplier session consists of dictionary consisting: productObject_id, productName, quantity and where to add quantity to
        except:
            print("Session does not exist!")

        productObject_id = int(update_order.product.data)
        productObject = product_dict[productObject_id]
        quantity = update_order.quantity.data
        delivery = update_order.send_to.data

        orderListing = supplier_dict.get(id)
        orderListing["productName"] = productObject.get_name()
        orderListing["quantity"] = quantity
        orderListing["send_to"] = delivery

        db['currentSupplier'] = supplier_dict
        db.close()

        print(productObject.get_name())

        return redirect(url_for("view_SupplierOrder"))
    else:
        supplier_dict = {}
        db = shelve.open('products.db', 'r')
        supplier_dict = db['currentSupplier']
        db.close()

        orderListing = supplier_dict.get(id)
        update_order.product.data = orderListing["productObjectID"]
        update_order.quantity.data = orderListing["quantity"]
        update_order.send_to.data = orderListing["send_to"]

        return render_template("updateSupplierOrder.html", form=update_order)

def delete_supplierOrder(id):

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

    db = shelve.open('products.db', 'c')
    supplier_dict = {}
    supplier_dict = db["currentSupplier"]  # current supplier session consists of dictionary consisting: productObject_id, productName, quantity and where to add quantity to

    supplier_dict.pop(id)

    db['currentSupplier'] = supplier_dict

    db.close()

    return redirect(url_for("view_SupplierOrder"))

def view_SupplierOrder():

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

    db = shelve.open('products.db', 'c')
    supplierDict = {}
    try:
        supplierDict = db["currentSupplier"]
        print("db found!!")
    except:
        print("No current supplier forms!")

    db.close()

    return render_template('viewSupplierOrders.html', supplierDict=supplierDict)

def confirm_supplier():

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

    # get all the items added into the checkout page
    db = shelve.open('products.db', 'c')
    supplierDict = {}
    productDict = {}
    orderDict = {}

    try:
        productDict = db["Products"]
    except:
        print("No products available!!")

    try:
        supplierDict = db["currentSupplier"]
        # current supplier session consists of dictionary consisting: productObject_id, productName, quantity and where to add quantity to
    except:
        print("Error!! Supplier not found")

    try:
        IDcount = db["ID"]
    except:
        print("ID not found")

    for key, value in supplierDict.items():
        productObjectID = value["productObjectID"]
        productObject = productDict[productObjectID]

        quantity = value["quantity"]
        delivery = value["send_to"]
        orderObject = Product.Supplier(productObject, quantity, delivery)
        orderDict[orderObject.get_id()] = orderObject
        db["Supplier"] = orderDict

    # check all objects in supplier shelve
    checkDict = db["Supplier"]
    for key, i in checkDict.items():
        print(i.get_id(), ":", i.get_product_name(), i.get_quantity(), i.get_delivery())

    # clear currentSupplier shelve + ID shelve
    supplierDict.clear()
    db["currentSupplier"] = supplierDict
    IDcount = 0
    db["ID"] = IDcount

    # ============ adding quantity =====================
    for key, value in checkDict.items():
        supplierProductObject = value.get_product()
        supplierProductID = supplierProductObject.get_id()
        productObject = productDict[supplierProductID]

        quantity = value.get_quantity()
        delivery = value.get_delivery()

        instocksList = productObject.get_instocks()
        oldQuantity = instocksList[delivery]
        newQuantity = oldQuantity + quantity
        instocksList[delivery] = newQuantity
        productObject.set_instocks(instocksList)

        x = productObject.get_instocks()
        y = x[delivery]
        print(productObject.get_name(), "=== Updated quantity:", y, "at", delivery)
        print("Old quantity:", oldQuantity, ", Ordeing:", quantity, ", New Quantity:", y)
        productDict[supplierProductID] = productObject
        db["Products"] = productDict
        print()

    db.close()
    return render_template("home.html")