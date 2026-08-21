from database import get_connection

def get_all_products():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT product_id, name, category, selling_price, stock
    FROM products
    ORDER BY product_id;
    """

    cursor.execute(query)
    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products

def add_product(name, category, purchase_price, selling_price, stock, minimum_stock):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO products
    (name, category, purchase_price, selling_price, stock, minimum_stock)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        name,
        category,
        purchase_price,
        selling_price,
        stock,
        minimum_stock
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    return True

def update_product(product_id, name, category,
                   purchase_price, selling_price,
                   stock, minimum_stock):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE products
    SET
        name=%s,
        category=%s,
        purchase_price=%s,
        selling_price=%s,
        stock=%s,
        minimum_stock=%s
    WHERE product_id=%s
    """

    values = (
        name,
        category,
        purchase_price,
        selling_price,
        stock,
        minimum_stock,
        product_id
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    return True

def get_product_by_id(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM products
    WHERE product_id=%s
    """

    cursor.execute(query, (product_id,))

    product = cursor.fetchone()

    cursor.close()
    connection.close()

    return product

# ==========================================================
# DELETE PRODUCT
# ==========================================================

def delete_product(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM products
    WHERE product_id=%s
    """

    cursor.execute(query, (product_id,))

    connection.commit()

    deleted = cursor.rowcount

    cursor.close()
    connection.close()

    return deleted > 0

# ==========================================================
# SEARCH PRODUCTS
# ==========================================================

def search_products(keyword):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        product_id,
        name,
        category,
        selling_price,
        stock
    FROM products
    WHERE
        name LIKE %s
        OR category LIKE %s
    ORDER BY name ASC
    """

    search_keyword = f"%{keyword}%"

    cursor.execute(
        query,
        (search_keyword, search_keyword)
    )

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products

# ==========================================================
# GET PRODUCTS FOR BILLING
# ==========================================================

def get_products_for_billing():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        product_id,
        name,
        selling_price,
        stock
    FROM products
    ORDER BY name ASC
    """

    cursor.execute(query)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products

# ==========================================================
# FETCH CUSTOMER BY PHONE NUMBER
# ==========================================================

def get_customer_by_phone(phone):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            customer_id,
            name,
            phone,
            loyalty_points,
            total_spent
        FROM customers
        WHERE phone = %s
    """

    cursor.execute(query, (phone,))
    customer = cursor.fetchone()

    cursor.close()
    connection.close()

    return customer

# ==========================================================
# CREATE CUSTOMER IF NOT EXISTS
# ==========================================================

def create_customer_if_not_exists(phone, name):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Check if customer already exists
    cursor.execute(
        "SELECT customer_id FROM customers WHERE phone = %s",
        (phone,)
    )

    customer = cursor.fetchone()

    if customer:
        customer_id = customer["customer_id"]

    else:
        cursor.execute(
            """
            INSERT INTO customers (name, phone)
            VALUES (%s, %s)
            """,
            (name.title(), phone)
        )

        connection.commit()

        customer_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return customer_id

# ==========================================================
# CREATE SALE
# ==========================================================

def create_sale(customer_id, total, gst, discount, payment_method):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO sales (
            customer_id,
            total_amount,
            gst_amount,
            discount_amount,
            payment_method
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            customer_id,
            total,
            gst,
            discount,
            payment_method
        )
    )

    connection.commit()

    sale_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return sale_id

# ==========================================================
# SAVE ALL PRODUCTS OF A SALE
# ==========================================================

def add_sale_items(sale_id, cart):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO sale_items (
            sale_id,
            product_id,
            quantity,
            selling_price,
            subtotal
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    for item in cart:

        cursor.execute(
            query,
            (
                sale_id,
                item["id"],
                item["quantity"],
                item["price"],      # GUI cart stores selling price in "price"
                item["subtotal"]
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

# ==========================================================
# UPDATE PRODUCT STOCK AFTER SALE
# ==========================================================

def update_stock_after_sale(cart):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    for item in cart:

        # Get current stock
        cursor.execute(
            """
            SELECT stock
            FROM products
            WHERE product_id = %s
            """,
            (item["id"],)
        )

        product = cursor.fetchone()

        if not product:
            continue

        current_stock = product["stock"]
        new_stock = current_stock - item["quantity"]

        # Update products table
        cursor.execute(
            """
            UPDATE products
            SET stock = %s
            WHERE product_id = %s
            """,
            (new_stock, item["id"])
        )

        # Save stock movement history
        cursor.execute(
            """
            INSERT INTO stock_movements (
                product_id,
                movement_type,
                quantity,
                stock_after
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                item["id"],
                "SALE",
                -item["quantity"],
                new_stock
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

    # ==========================================================
# GET CUSTOMER ID OR CREATE NEW CUSTOMER
# ==========================================================

def get_or_create_customer(name, phone):

    customer = get_customer_by_phone(phone)

    if customer:
        return customer["customer_id"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO customers (name, phone)
        VALUES (%s, %s)
        """,
        (name, phone)
    )

    connection.commit()

    customer_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return customer_id