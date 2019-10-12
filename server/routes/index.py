from server import app, mongo
from flask import render_template, jsonify
from flask_cors import CORS

CORS(app)

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return app.send_static_file('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return app.send_static_file('500.html')

@app.route('/api/v1/stocklevels')
def getstock():
    products = []
    for p in mongo.db.products.find({}):
        p.pop("_id")
        products.append(p)
    return jsonify(products)

@app.route('/api/v1/decrement/<int:sku>')
def decrementstock(sku):
    print("decrement SKU: %d" % sku)
    p = mongo.db.products.find_one({"sku": sku})
    updated_qty = p['qty'] - 1
    update = {"$set": {"qty": updated_qty}}
    mongo.db.products.update_one({"sku": sku}, update)
    return 'OK %d' % updated_qty
    
@app.route('/api/v1/increment/<int:sku>')
def incrementstock(sku):
    print("increment SKU: %d" % sku)
    p = mongo.db.products.find_one({"sku": sku})
    updated_qty = p['qty'] + 1
    update = {"$set": {"qty": updated_qty}}
    mongo.db.products.update_one({"sku": sku}, update)
    return 'OK %d' % updated_qty 