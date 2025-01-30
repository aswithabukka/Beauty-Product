from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

def load_products():
    with open('products.json', 'r') as f:
        data = json.load(f)
        return data['products']

def filter_products(products, category=None, min_price=None, max_price=None, min_rating=None):
    filtered = products
    
    if category:
        filtered = [p for p in filtered if p['category'] == category]
    if min_price is not None:
        filtered = [p for p in filtered if p['price'] >= float(min_price)]
    if max_price is not None:
        filtered = [p for p in filtered if p['price'] <= float(max_price)]
    if min_rating is not None:
        filtered = [p for p in filtered if p['rating'] >= float(min_rating)]
    
    return filtered

@app.route('/')
def home():
    products = load_products()
    
    # Get filter parameters
    category = request.args.get('category')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    min_rating = request.args.get('min_rating')
    
    # Apply filters if any
    if any([category, min_price, max_price, min_rating]):
        products = filter_products(products, category, min_price, max_price, min_rating)
    
    # Get unique categories for filter options
    categories = list(set(p['category'] for p in load_products()))
    
    return render_template('index.html', 
                         products=products, 
                         categories=categories,
                         selected_category=category,
                         selected_min_price=min_price,
                         selected_max_price=max_price,
                         selected_rating=min_rating)

@app.route('/cart')
def cart():
    return render_template('cart.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
