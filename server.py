
from crypt import methods
from math import prod
from flask import Flask, request
from flask import abort
from about_me import me
from mock_data import catalog
import json
from config import db
from bson import ObjectId

app = Flask('assignment2')

@app.route("/", methods=["GET"])
def home():
    return "This is the home page"

@app.route("/about")
def about():
    return (me["first"] +" "+ me["last"])

@app.route("/myaddress")
def address():
    return (me["address"]["street"] + " " + me["address"]["number"])


    ################## ENDPOINTS ##################

@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    results = []
    cursor = db.products.find({})

    for product in cursor:
        product["_id"] = str(product["_id"])
        results.append(product)

    return json.dumps(results)

@app.route("/api/catalog", methods=["POST"])
def save_product():

    product = request.get_json()
    errors = ""

    try:
        if not "title" in product or len(product["title"]) < 5:
            errors +=  "Title is required or should have at least 5 chars"
        
        elif not "image" in product:
            errors += ", Product must contain image"
            
        elif not "price" in product or product["price"] < 1:
            errors += ", Product must contain a price and it need to be grater or equal than 1"
        
        if errors:
            return abort(400, errors)

        db.products.insert_one(product)
        product["_id"] = str(product["_id"])
        
        return json.dumps(product)
    
    except Exception as ex:
        return abort(500, F"Unexpected error: {ex}")

    

@app.route("/api/catalog/count", methods=["GET"])
def get_count():
    count = 0
    cursor = db.products.find({})

    for product in cursor:
        count+=1

    return json.dumps(count)

@app.route("/api/catalog/<id>", methods=["GET"])
def get_product(id):
    try:
        if not ObjectId.is_valid(id):
            return abort(400,"Invalid Id")

        product = db.products.find_one({"_id":ObjectId(id)})

        if not product:
            return abort(404, "Product not found")

        product["_id"] = str(product["_id"])
        return json.dumps(product)

    except Exception as ex:
        return abort(500, F"Unexpected error: {ex}")


@app.route("/api/catalog/total", methods=["GET"])
def get_total():
    total = 0
    cursor = db.products.find({})

    for product in cursor:
        price = product["price"]
        total += price

    return json.dumps(total)

@app.route("/api/products/<category>", methods=["GET"])
def get_category(category):
    products = []
    cursor = db.products.find({"category": category})

    for product in cursor:
        product["_id"]= str(product["_id"])
        products.append(product)

    return json.dumps(products)

@app.route("/api/categories", methods=["GET"])
def get_categories():

    categories = []
    cursor = db.products.find({})

    for product in cursor:
        category = product["category"]
        if category not in categories:
            categories.append(category)
    return json.dumps(categories)

@app.route("/api/catalog/cheapest", methods=["GET"])
def get_cheapest():
    minPrice = ""
    cursor = db.products.find({})
    for product in cursor:
        if(minPrice == ""):
            minPrice = product["price"]
        else:
            if(product["price"]<minPrice):
                minPrice = product["price"]
    return json.dumps(minPrice)





################################## COUPON CODES ######################################
#GET COUPONS
@app.route("/api/coupons", methods=["GET"])
def get_all_coupons():
    cursor = db.coupons.find({})
    results = []
    for couponCode in cursor:
        couponCode["_id"] = str(couponCode["_id"])
        results.append(couponCode)
    
    return json.dumps(results)

#SAVE COUPON CODE
@app.route("/api/coupons", methods=["POST"])
def save_coupon():
    coupon = request.get_json()
    db.coupons.insert_one(coupon)
    coupon["_id"] = str (coupon["_id"])
    return json.dumps(coupon)

    
app.run(debug=True)