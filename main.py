import MingXuan, Irfan, XinHui, Khei

from flask import Flask, render_template


app = Flask(__name__)
app.secret_key = 'pineapples'

@app.route('/')
def home():
    return render_template("home.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorPage.html'), 404


@app.route("/snacks")
def food_snacks():
    return render_template("snacks.html")

# Ming Xuan
app.add_url_rule('/register', 'register', view_func=MingXuan.register, methods=["GET", "POST"])

app.add_url_rule('/login', 'login', view_func=MingXuan.login, methods=["GET", "POST"])

app.add_url_rule('/logout', 'logout', view_func=MingXuan.logout)

app.add_url_rule('/forgotpassword', 'forgot_password', view_func=MingXuan.forgot_password)

app.add_url_rule('/editprofile', 'edit_profile', view_func=MingXuan.edit_profile)

app.add_url_rule('/dashboard', 'dashboard', view_func=MingXuan.dashboard)

app.add_url_rule('/manageaccounts', 'manage_accounts', view_func=MingXuan.manage_accounts)

app.add_url_rule('/manageemployees', 'manage_employees', view_func=MingXuan.manage_employees)

app.add_url_rule('/deleteself', 'delete_self', view_func=MingXuan.delete_self)

app.add_url_rule('/createemployee', 'create_employee', view_func=MingXuan.create_employee, methods=["GET", "POST"])

app.add_url_rule('/updateschedule/<int:id>', 'update_schedule', view_func=MingXuan.update_schedule, methods=["GET", "POST"])

app.add_url_rule('/updateaccount/<int:id>', 'update_account', view_func=MingXuan.update_account, methods=["GET", "POST"])

app.add_url_rule('/deleteaccount/<int:id>', 'delete_account', view_func=MingXuan.delete_account)

app.add_url_rule('/changepassword', 'change_password', view_func=MingXuan.change_password, methods=["GET", "POST"])

app.add_url_rule('/careers', 'careers', view_func=MingXuan.careers, methods=["GET", "POST"])

app.add_url_rule('/viewApplicants', 'view_applicants', view_func=MingXuan.view_applicants, methods=["GET", "POST"])

app.add_url_rule('/updateApplicant/<int:id>', 'update_applicants', view_func=MingXuan.update_applicants, methods=["GET", "POST"])

app.add_url_rule('/deleteApplicant/<int:id>', 'delete_applicant', view_func=MingXuan.delete_applicant, methods=["GET", "POST"])

# Irfan
app.add_url_rule('/storeentry', 'store_entry', view_func=Irfan.store_entry, methods=["GET", "POST"])

app.add_url_rule('/storeentrydetails/<store>/<id>', 'store_entry_details', view_func=Irfan.store_entry_details, methods=["GET", "POST"])

app.add_url_rule('/storecount', 'store_count', view_func=Irfan.store_count, methods=["GET", "POST"])

app.add_url_rule('/showstorecount', 'retrieve_count', view_func=Irfan.retrieve_count, methods=["GET", "POST"])

app.add_url_rule('/chooseentryrecord', 'choose_records', view_func=Irfan.choose_records, methods=["GET", "POST"])

app.add_url_rule('/entryrecords/<string:store>', 'retrieve_records', view_func=Irfan.retrieve_records, methods=["GET", "POST"])

app.add_url_rule('/deletecustomer/<store>/<id>', 'delete_customer', view_func=Irfan.delete_customer, methods=["GET", "POST"])

app.add_url_rule('/feedback', 'feedback', view_func=Irfan.feedback, methods=['POST', 'GET'])

app.add_url_rule('/feedbackacknowledgement', 'feedback_ack', view_func=Irfan.feedback_ack, methods=['POST', 'GET'])

app.add_url_rule('/viewfeedback', 'view_feedback', view_func=Irfan.view_feedback, methods=['POST', 'GET'])

# Xin Hui
app.add_url_rule('/products', 'viewAll', view_func=XinHui.viewAll)

app.add_url_rule('/products/search', 'search', view_func=XinHui.search, methods=["POST"])

app.add_url_rule('/products/sortBy/low_to_high', 'low_to_high', view_func=XinHui.low_to_high)

app.add_url_rule('/products/sortBy/high_to_low', 'high_to_low', view_func=XinHui.high_to_low)

app.add_url_rule('/products/sortBy/a_to_z', 'a_to_z', view_func=XinHui.a_to_z)

app.add_url_rule('/products/sortBy/z_to_a', 'z_to_a', view_func=XinHui.z_to_a)

app.add_url_rule('/products/sortBy/newest', 'newest', view_func=XinHui.newest)

app.add_url_rule('/individual/<int:id>/', 'view_individual', view_func=XinHui.view_individual, methods=["GET", "POST"])

app.add_url_rule('/viewProduct', 'view_product', view_func=XinHui.view_product)

app.add_url_rule('/createProduct', 'create_product', view_func=XinHui.create_product, methods=["GET", "POST"])

app.add_url_rule('/updateProduct/<int:id>/', 'update_product', view_func=XinHui.update_product, methods=["GET", "POST"])

app.add_url_rule('/deleteProduct/<int:id>', 'delete_product', view_func=XinHui.delete_product, methods=["POST"])

app.add_url_rule('/orderInstocks', 'order_instocks', view_func=XinHui.order_instocks, methods=["GET", "POST"])

app.add_url_rule('/updateSupplierOrder/<int:id>/', 'update_supplierOrder', view_func=XinHui.update_supplierOrder, methods=["GET", "POST"])

app.add_url_rule('/deleteSupplierOrder/<int:id>/', 'delete_supplierOrder', view_func=XinHui.delete_supplierOrder, methods=["POST"])

app.add_url_rule('/viewSupplierOrder', 'view_SupplierOrder', view_func=XinHui.view_SupplierOrder)

app.add_url_rule('/confirmSupplier', 'confirm_supplier', view_func=XinHui.confirm_supplier)

# Khei
app.add_url_rule('/addToCart/<int:id>', 'add_to_cart', view_func=Khei.add_to_cart, methods=["POST", "GET"])

app.add_url_rule('/clearCart', 'clear_cart', view_func=Khei.clear_cart, methods=["POST", "GET"])

app.add_url_rule('/add/<int:id>', 'addQuantity', view_func=Khei.addQuantity)

app.add_url_rule('/minus/<int:id>', 'minusQuantity', view_func=Khei.minusQuantity)

app.add_url_rule('/deleteItem/<int:id>', 'delete_item', view_func=Khei.delete_item, methods=["POST", "GET"])

app.add_url_rule('/checkOut', 'checkOut_page', view_func=Khei.checkOut_page , methods=["POST", "GET"])

app.add_url_rule('/Cart', 'cartPage', view_func=Khei.cartPage, methods=["POST", "GET"])

app.add_url_rule('/customerInfo', 'customerInfo', view_func=Khei.customerInfo , methods=["POST", "GET"])

app.add_url_rule('/viewOrder', 'view_order', view_func=Khei.view_order, methods=["POST", "GET"])

app.add_url_rule('/updateOrder/<id>', 'update_order', view_func=Khei.update_order, methods=["POST", "GET"])

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=3000)
