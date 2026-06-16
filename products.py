from database import get_connection


def get_products(search=""):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        products.id,
        products.article,
        products.name,
        products.price,
        products.quantity,
        categories.name AS category
    FROM products
    LEFT JOIN categories
    ON categories.id = products.category_id
    WHERE products.name LIKE ? OR products.article LIKE ?
    ORDER BY products.name
    """, (f"%{search}%", f"%{search}%"))

    products = cur.fetchall()
    conn.close()
    return products


def add_product(article, name, price, quantity):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO products (article, name, price, quantity)
    VALUES (?, ?, ?, ?)
    """, (article, name, price, quantity))

    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


def create_product(parent, callback):
    """Создает диалоговое окно для добавления товара"""
    from admin_panel import ProductForm
    ProductForm(parent, callback)