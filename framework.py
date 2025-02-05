from flask import Flask, render_template, request, redirect, session, flash
from GBD.db import (
    init_db,
    add_user,
    get_user_by_username,
    add_catalogue_item,
    get_catalogue_items,
    update_catalogue_item,
    delete_catalogue_item,
    add_special_product,
    get_special_products,
    update_special_product,
    delete_special_product
)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'limbus'

PASSWORD_PROTECTION_KEY = "management_access"

@app.route('/')
def root():
    return render_template('welcome.html')

@app.route('/catalogue')
def catalogue():
    if 'user_id' not in session:
        return render_template('error.html', message="You must be logged in to view the catalogue.")
    
    items = get_catalogue_items()
    return render_template('catalogue.html', items=items, query=None)


@app.route('/catalogue/search', methods=['GET'])
def search_catalogue():
    if 'user_id' not in session:
        return render_template('error.html', message="You must be logged in to search the catalogue.")
    
    query = request.args.get('q', '').strip()
    items = get_catalogue_items()  # Retrieve all items from the catalogue
    if query:
        items = [item for item in items if query.lower() in item['name'].lower() or query.lower() in item['description'].lower()]
    
    return render_template('catalogue.html', items=items, query=query)


@app.route('/management', methods=['GET', 'POST'])
def management():
    # Ensure the user has entered the correct password
    if not session.get(PASSWORD_PROTECTION_KEY):
        return redirect('/management-password')

    if request.method == 'POST':
        action = request.form['action']
        item_id = request.form.get('item_id')
        name = request.form.get('name')
        description = request.form.get('description')

        if action == 'create':
            add_catalogue_item(name, description)
            flash('Catalogue item added successfully.', 'success')
        elif action == 'update' and item_id:
            update_catalogue_item(item_id, name, description)
            flash('Catalogue item updated successfully.', 'success')
        elif action == 'delete' and item_id:
            delete_catalogue_item(item_id)
            flash('Catalogue item deleted successfully.', 'success')

    items = get_catalogue_items()
    special_products = get_special_products()
    return render_template('management.html', items=items, special_products=special_products)

@app.route('/special_product/create', methods=['POST'])
def create_special_product():
    if not session.get(PASSWORD_PROTECTION_KEY):
        return redirect('/management-password')

    name = request.form['name']
    description = request.form['description']

    if add_special_product(name, description):
        flash('Special product added successfully.', 'success')
    else:
        flash('Error adding special product.', 'danger')
    return redirect('/management')

@app.route('/special_product/update', methods=['POST'])
def update_special_product_route():
    if not session.get(PASSWORD_PROTECTION_KEY):
        return redirect('/management-password')

    item_id = request.form['item_id']
    name = request.form['name']
    description = request.form['description']

    if update_special_product(item_id, name, description):
        flash('Special product updated successfully.', 'success')
    else:
        flash('Error updating special product.', 'danger')
    return redirect('/management')

@app.route('/special_product/delete', methods=['POST'])
def delete_special_product_route():
    if not session.get(PASSWORD_PROTECTION_KEY):
        return redirect('/management-password')

    item_id = request.form['item_id']
    
    if delete_special_product(item_id):
        flash('Special product deleted successfully.', 'success')
    else:
        flash('Error deleting special product.', 'danger')
    return redirect('/management')

@app.route('/management-password', methods=['GET', 'POST'])
def management_password():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'Limbus':
            session[PASSWORD_PROTECTION_KEY] = True
            flash('Access granted.', 'success')
            return redirect('/management')
        else:
            flash('Invalid password. Access denied.', 'danger')
    return render_template('management_password.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        flash('You are already logged in.', 'warning')
        return redirect('/catalogue')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if add_user(username, password):
            flash('Registration successful. Please log in.', 'success')
            return redirect('/login')
        else:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect('/register')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        flash('You are already logged in.', 'warning')
        return redirect('/catalogue')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)

        if user and user[2] == password:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful.', 'success')
            return redirect('/catalogue')
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/')

@app.route('/ceo')
def ceo():
    return render_template('ceo.html')

@app.route('/employees')
def employees():
    return render_template('employees.html')

@app.route('/special_product')
def special_product():
    # Fetch the list of special products from the database
    special_products = get_special_products()
    
    # Render the template and pass the products to it
    return render_template('SpecialProducts.html', products=special_products)

# Route for viewing details of a specific special product
@app.route('/special_product/<int:product_id>')
def special_product_page(product_id):
    # Fetch the list of special products from the database
    special_products = get_special_products()
    
    # Find the specific product by product_id
    product = next((item for item in special_products if item[0] == product_id), None)
    
    # Render the detail page for the specific product
    return render_template('special_product_page.html', product=product)

@app.route('/legal_information')
def legal_information():
    return render_template('legalinformation.html')

@app.route('/locator')
def locator():
    return render_template('locator.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
