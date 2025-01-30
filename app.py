from flask import Flask, render_template, jsonify, request, session
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Load concerns data
CONCERNS = [
    {
        "id": "hyperpigmentation",
        "name": "Hyperpigmentation",
        "description": "Dark patches and uneven skin tone",
        "image": "https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
        "recommended_products": ["1", "5"]  # IDs from products.json
    },
    {
        "id": "hairfall",
        "name": "Hair Fall",
        "description": "Excessive hair loss and thinning",
        "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
        "recommended_products": ["3", "6"]
    },
    {
        "id": "acne",
        "name": "Acne & Blemishes",
        "description": "Breakouts, spots, and blemishes",
        "image": "https://images.unsplash.com/photo-1513263196760-5955c29c7c51?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
        "recommended_products": ["1", "5"]
    },
    {
        "id": "dryness",
        "name": "Dryness & Dehydration",
        "description": "Dry, flaky, and dehydrated skin",
        "image": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
        "recommended_products": ["2"]
    },
    {
        "id": "aging",
        "name": "Signs of Aging",
        "description": "Fine lines, wrinkles, and loss of firmness",
        "image": "https://images.unsplash.com/photo-1571008887538-b36bb32f4571?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
        "recommended_products": ["2", "5"]
    },
    {
        "id": "damaged_hair",
        "name": "Damaged Hair",
        "description": "Dry, brittle, and damaged hair",
        "image": "https://images.unsplash.com/photo-1519735777090-ec97162dc266?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
        "recommended_products": ["3", "4", "6"]
    }
]

def load_products():
    with open('products.json', 'r') as f:
        data = json.load(f)
        return data['products']

def filter_products(products, category=None, min_price=None, max_price=None, min_rating=None):
    filtered = products
    
    if category and category != 'all':
        filtered = [p for p in filtered if p['category'].lower() == category.lower()]
    if min_price is not None and min_price != '':
        filtered = [p for p in filtered if p['price'] >= float(min_price)]
    if max_price is not None and max_price != '':
        filtered = [p for p in filtered if p['price'] <= float(max_price)]
    if min_rating is not None and min_rating != '':
        filtered = [p for p in filtered if p['rating'] >= float(min_rating)]
    
    return filtered

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/concerns')
def concerns():
    return render_template('concerns.html', concerns=CONCERNS)

@app.route('/get_recommendations/<concern_id>')
def get_recommendations(concern_id):
    # Find the concern
    concern = next((c for c in CONCERNS if c['id'] == concern_id), None)
    if not concern:
        return jsonify({'error': 'Concern not found'}), 404
    
    # Get recommended products
    all_products = load_products()
    recommended_products = [p for p in all_products if p['id'] in concern['recommended_products']]
    
    # Add a short description for each product
    for product in recommended_products:
        product['short_description'] = f"Perfect for {concern['name'].lower()}"
    
    return jsonify({'products': recommended_products})

@app.route('/products')
def products():
    all_products = load_products()
    
    # Get filter parameters
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    min_rating = request.args.get('min_rating', '')
    
    # Apply filters if any
    products = filter_products(all_products, category, min_price, max_price, min_rating)
    
    # Get unique categories for filter options
    categories = sorted(list(set(p['category'] for p in all_products)))
    
    # Get price range for the slider
    price_range = {
        'min': min(p['price'] for p in all_products),
        'max': max(p['price'] for p in all_products)
    }
    
    return render_template('products.html', 
                         products=products, 
                         categories=categories,
                         selected_category=category,
                         selected_min_price=min_price,
                         selected_max_price=max_price,
                         selected_rating=min_rating,
                         price_range=price_range)

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    all_products = load_products()
    
    # Get the full product details for items in cart
    cart_products = []
    subtotal = 0
    
    for product_id, quantity in cart.items():
        product = next((p for p in all_products if p['id'] == product_id), None)
        if product:
            product_copy = dict(product)  # Create a copy to avoid modifying the original
            product_copy['quantity'] = quantity
            cart_products.append(product_copy)
            # Calculate price after discount
            price = product['price'] * (1 - product['discount']/100) if product['discount'] > 0 else product['price']
            subtotal += price * int(quantity)
    
    return render_template('cart.html', cart_items=cart_products, subtotal=subtotal)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('product_id')
    if product_id:
        cart = session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1
        session['cart'] = cart
        return jsonify({'success': True, 'cart_count': sum(cart.values())})
    return jsonify({'success': False}), 400

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.json.get('product_id')
    if not product_id:
        return jsonify({'success': False}), 400
    
    # Get the cart from session
    cart = session.get('cart', {})
    
    # Remove the item
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
    
    # Calculate new subtotal
    all_products = load_products()
    subtotal = 0
    for pid, qty in cart.items():
        product = next((p for p in all_products if p['id'] == pid), None)
        if product:
            price = product['price'] * (1 - product['discount']/100) if product['discount'] > 0 else product['price']
            subtotal += price * int(qty)
    
    return jsonify({
        'success': True, 
        'subtotal': subtotal,
        'is_empty': len(cart) == 0
    })

@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')
    
    if not product_id or not quantity:
        return jsonify({'success': False}), 400
    
    # Get the cart from session
    cart = session.get('cart', {})
    
    # Update quantity
    cart[product_id] = quantity
    session['cart'] = cart
    
    # Calculate new subtotal
    all_products = load_products()
    subtotal = 0
    for pid, qty in cart.items():
        product = next((p for p in all_products if p['id'] == pid), None)
        if product:
            price = product['price'] * (1 - product['discount']/100) if product['discount'] > 0 else product['price']
            subtotal += price * int(qty)
    
    return jsonify({'success': True, 'subtotal': subtotal})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)
