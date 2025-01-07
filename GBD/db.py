import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def init_db():
    """Initialize the database and create necessary tables if they don't exist."""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Create users table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        # Create catalogue table
        c.execute('''
            CREATE TABLE IF NOT EXISTS catalogue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )
        ''')

        # Create special products table
        c.execute('''
            CREATE TABLE IF NOT EXISTS special_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

# User functions
def add_user(username, password):
    """Add a user to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error adding user: {e}")
        return False

def get_user_by_username(username):
    """Get a user from the database by their username."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

# Catalogue functions
def add_catalogue_item(name, description):
    """Add a catalogue item to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO catalogue (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error adding catalogue item: {e}")
        return False

def get_catalogue_items():
    """Fetch all catalogue items from the database and return them as a list of dictionaries."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM catalogue')
    rows = c.fetchall()
    conn.close()
    
    # Convert tuples to dictionaries
    items = []
    for row in rows:
        item = {
            'id': row[0],
            'name': row[1],
            'description': row[2]
        }
        items.append(item)
    
    return items

def update_catalogue_item(item_id, name, description):
    """Update a catalogue item in the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE catalogue SET name = ?, description = ? WHERE id = ?', (name, description, item_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error updating catalogue item: {e}")
        return False

def delete_catalogue_item(item_id):
    """Delete a catalogue item from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM catalogue WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting catalogue item: {e}")
        return False

# Special product functions
def add_special_product(name, description):
    """Add a special product to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO special_products (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error adding special product: {e}")
        return False

def get_special_products():
    """Fetch all special products from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM special_products')
    products = c.fetchall()
    conn.close()
    return products

def update_special_product(item_id, name, description):
    """Update a special product in the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE special_products SET name = ?, description = ? WHERE id = ?', (name, description, item_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error updating special product: {e}")
        return False

def delete_special_product(item_id):
    """Delete a special product from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM special_products WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting special product: {e}")
        return False

def get_special_products():
    return [
        (1, 'Trivalin', 'Our brand new experimental energizer! No germans included.', '/static/assets/product1.jpg'),
        (2, 'Trapazin', 'Got beaten into a pulp? this will help you recover faster!', '/static/assets/product2.jpg'),
        (3, 'Limbart', 'A sleeping medication ideal for those who have not slept in years.', '/static/assets/product3.jpg'),
        (4, 'Kaleidona', 'Experimental Psychoid drug still in test phase, buying voids us of any responsibility as you agree to test this.', '/static/assets/product4.jpg'),
        (5, 'Tramadol', 'Cheap mass produced analgesic. Ideal for your wounds!', '/static/assets/product5.jpg'),
        (6, 'Synapt', 'Nobody will keep you down thanks to our new muscle enhancers!', '/static/assets/product6.jpg'),
    ]
