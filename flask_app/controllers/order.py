from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.order import Order

@app.route('/new/order')
def new_order():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":session['user_id']
    }
    toppings = ["Pepperoni", "Mushroom", "Extra cheese", "Sausage", "Onion", "Black olives", "Green pepper", "Fresh garlic"]
    return render_template('new_order.html',user=User.get_by_id(data), topping=toppings)

@app.route('/create/order',methods=['POST'])
def create_order():
    if 'user_id' not in session:
        return redirect('/')
    non_useful = ['method', 'size', 'crust', 'qty']
    data = {
        "method": request.form["method"],
        "size": request.form["size"],
        "crust": request.form["crust"],
        "qty": request.form["qty"],
        "user_id": session["user_id"]
    }
    topping  = ""
    for key in dict(request.form).keys():
        if key not in non_useful:
            topping = topping + "," + key
    data["topping"] = topping
    order = Order.save(data)
    session['id'] = order
    return redirect('/')

# @app.route('/favorite_order', methods=['GET'])
# def favorite_order():
#     if 'user_id' not in session:
#         return redirect('/')
    
#     user_data = {
#         "id":session['user_id']
#     }
#     return render_template("account.html", user=User.get_by_id(user_data), 
#                             orders=Order.get_all())
