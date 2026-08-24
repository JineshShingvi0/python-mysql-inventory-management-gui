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

# ==========================================================
# ADD STOCK TO PRODUCT
# ==========================================================

def add_stock(product_id, quantity_added):

    connection = get_connection()
    cursor = connection.cursor()

    # Get current stock
    cursor.execute(
        "SELECT stock FROM products WHERE product_id=%s",
        (product_id,)
    )

    current_stock = cursor.fetchone()[0]
    new_stock = current_stock + quantity_added

    # Update stock
    cursor.execute(
        "UPDATE products SET stock=%s WHERE product_id=%s",
        (new_stock, product_id)
    )

    # Record stock movement
    cursor.execute("""
        INSERT INTO stock_movements
        (product_id, movement_type, quantity, stock_after)
        VALUES (%s, %s, %s, %s)
    """, (
        product_id,
        "STOCK IN",
        quantity_added,
        new_stock
    ))

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
# ADD LOYALTY POINTS
# ==========================================================

def add_loyalty_points(customer_id, bill_amount):

    connection = get_connection()
    cursor = connection.cursor()

    # 1 point for every ₹100
    earned_points = int(bill_amount // 100)

    cursor.execute("""
        UPDATE customers
        SET loyalty_points = loyalty_points + %s
        WHERE customer_id = %s
    """, (earned_points, customer_id))

    connection.commit()

    cursor.close()
    connection.close()

    return earned_points


# ==========================================================
# GET LOYALTY POINTS
# ==========================================================

def get_loyalty_points(customer_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT loyalty_points
        FROM customers
        WHERE customer_id = %s
    """, (customer_id,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result["loyalty_points"] if result else 0
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

    for item in cart:

        # 1️⃣ Save sold item into sale_items table
        cursor.execute("""
            INSERT INTO sale_items
            (sale_id, product_id, quantity, selling_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            sale_id,
            item["id"],
            item["quantity"],
            item["price"],
            item["subtotal"]
        ))

        # 2️⃣ Get current stock
        cursor.execute(
            "SELECT stock FROM products WHERE product_id=%s",
            (item["id"],)
        )

        current_stock = cursor.fetchone()[0]

        stock_after = current_stock - item["quantity"]

        # 3️⃣ Update stock in products table
        cursor.execute("""
            UPDATE products
            SET stock=%s
            WHERE product_id=%s
        """, (
            stock_after,
            item["id"]
        ))

        # 4️⃣ Record SALE movement  ← ADD HERE
        cursor.execute("""
            INSERT INTO stock_movements
            (product_id, movement_type, quantity, stock_after)
            VALUES (%s, %s, %s, %s)
        """, (
            item["id"],
            "SALE",
            item["quantity"],
            stock_after
        ))

    # 5️⃣ Commit once after the loop
    connection.commit()

    cursor.close()
    connection.close()

    return True

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


# ==========================================================
# GET ALL CUSTOMERS
# ==========================================================

def get_all_customers():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            customer_id,
            name,
            phone,
            email,
            address,
            loyalty_points
        FROM customers
        ORDER BY customer_id ASC
    """)

    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return customers


# ==========================================================
# SEARCH CUSTOMERS
# ==========================================================

def search_customers(keyword):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            customer_id,
            name,
            phone,
            email,
            address,
            loyalty_points
        FROM customers
        WHERE
            name LIKE %s
            OR phone LIKE %s
        ORDER BY name
    """,
    (f"%{keyword}%", f"%{keyword}%"))

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


# ==========================================================
# ADD CUSTOMER
# ==========================================================

def add_customer(name, phone, email="", address=""):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO customers
        (name, phone, email, address)
        VALUES (%s,%s,%s,%s)
    """,
    (name, phone, email, address))

    connection.commit()

    cursor.close()
    connection.close()


# ==========================================================
# UPDATE CUSTOMER
# ==========================================================

def update_customer(customer_id, name, phone, email, address):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE customers
        SET
            name=%s,
            phone=%s,
            email=%s,
            address=%s
        WHERE customer_id=%s
    """,
    (name, phone, email, address, customer_id))

    connection.commit()

    cursor.close()
    connection.close()


# ==========================================================
# DELETE CUSTOMER
# ==========================================================

def delete_customer(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM customers WHERE customer_id=%s",
        (customer_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

# ==========================================================
# CUSTOMER SUMMARY
# ==========================================================

def get_customer_summary(customer_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            c.customer_id,
            c.name,
            c.phone,
            c.loyalty_points,
            COUNT(s.sale_id) AS total_orders,
            COALESCE(SUM(s.total_amount),0) AS total_spent,
            MAX(s.sale_date) AS last_purchase
        FROM customers c
        LEFT JOIN sales s
            ON c.customer_id = s.customer_id
        WHERE c.customer_id = %s
        GROUP BY c.customer_id
    """, (customer_id,))

    summary = cursor.fetchone()

    cursor.close()
    connection.close()

    return summary

# ==========================================================
# CUSTOMER PURCHASE HISTORY
# ==========================================================

def get_customer_purchase_history(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            sale_id,
            sale_date,
            payment_method,
            discount_amount,
            gst_amount,
            total_amount
        FROM sales
        WHERE customer_id = %s
        ORDER BY sale_date DESC
    """, (customer_id,))

    history = cursor.fetchall()

    cursor.close()
    connection.close()

    return history

# ==========================================================
# TODAY'S REVENUE
# ==========================================================

def get_today_revenue():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(total_amount),0)
        FROM sales
        WHERE DATE(sale_date)=CURDATE()
    """)

    revenue = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return float(revenue)

# ==========================================================
# TODAY'S ORDERS
# ==========================================================

def get_today_orders():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM sales
        WHERE DATE(sale_date)=CURDATE()
    """)

    orders = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return orders

# ==========================================================
# TODAY'S BUSINESS SNAPSHOT
# ==========================================================

def get_today_business_snapshot():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(gst_amount), 0),
            COALESCE(SUM(discount_amount), 0)
        FROM sales
        WHERE DATE(sale_date) = CURDATE()
    """)

    gst_today, discount_today = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "gst": float(gst_today or 0),
        "discount": float(discount_today or 0)
    }




# ==========================================================
# TODAY'S CUSTOMER & LOYALTY SNAPSHOT
# ==========================================================

def get_today_customer_loyalty_snapshot():

    connection = get_connection()
    cursor = connection.cursor()

    # New customers created today
    cursor.execute("""
        SELECT COUNT(*)
        FROM customers
        WHERE DATE(created_at) = CURDATE()
    """)

    new_customers = cursor.fetchone()[0]

    # Loyalty points issued today
    # Current loyalty rule: 1 point for every ₹100 of final bill amount
    cursor.execute("""
        SELECT
            COALESCE(
                SUM(FLOOR(total_amount / 100)),
                0
            )
        FROM sales
        WHERE DATE(sale_date) = CURDATE()
    """)

    loyalty_points = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return {
        "new_customers": int(new_customers or 0),
        "loyalty_points": int(loyalty_points or 0)
    }


# ==========================================================
# TOTAL PRODUCTS
# ==========================================================

def get_total_products():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total

# ==========================================================
# LOW STOCK PRODUCTS
# ==========================================================

def get_low_stock_products():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            name,
            stock,
            minimum_stock
        FROM products
        WHERE stock <= minimum_stock
        ORDER BY stock ASC
    """)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products

# ==========================================================
# DASHBOARD INVENTORY ALERT SUMMARY
# ==========================================================
def get_dashboard_inventory_alerts():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Healthy Products
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM products
        WHERE stock > minimum_stock
    """)
    healthy = cursor.fetchone()["total"]

    # Low Stock
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM products
        WHERE stock <= minimum_stock
        AND stock > 0
    """)
    low_stock = cursor.fetchone()["total"]

    # Out of Stock
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM products
        WHERE stock = 0
    """)
    out_stock = cursor.fetchone()["total"]

    cursor.close()
    connection.close()

    return {
        "healthy": healthy,
        "low_stock": low_stock,
        "out_stock": out_stock
    }

# ==========================================================
# DASHBOARD BUSINESS INSIGHTS
# ==========================================================

def get_dashboard_insights():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    insights = []

    # Today's Revenue
    revenue = get_today_revenue()

    if revenue >= 5000:
        insights.append(
            ("🟢 Excellent Sales Day",
             f"Today's revenue reached ₹{revenue:,.2f}.")
        )

    # Low Stock Products
    cursor.execute("""
        SELECT name, stock
        FROM products
        WHERE stock <= minimum_stock
        LIMIT 2
    """)

    for item in cursor.fetchall():
        insights.append(
            ("🟡 Low Stock Alert",
             f"{item['name'].title()} has only {item['stock']} units remaining.")
        )

    # Best Selling Product Today
    cursor.execute("""
        SELECT p.name, SUM(si.quantity) AS qty
        FROM sale_items si
        JOIN products p
        ON si.product_id = p.product_id
        JOIN sales s
        ON si.sale_id = s.sale_id
        WHERE DATE(s.sale_date)=CURDATE()
        GROUP BY p.name
        ORDER BY qty DESC
        LIMIT 1
    """)

    best = cursor.fetchone()

    if best:
        insights.append(
            ("🏆 Best Selling Product",
             f"{best['name'].title()} sold {best['qty']} units today.")
        )

    cursor.close()
    connection.close()

    return insights

# ==========================================================
# DASHBOARD TOP PRODUCTS TODAY
# ==========================================================
def get_dashboard_top_products(limit=5):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            p.name,
            SUM(si.quantity) AS quantity
        FROM sale_items si
        JOIN products p
            ON si.product_id = p.product_id
        JOIN sales s
            ON si.sale_id = s.sale_id
        WHERE DATE(s.sale_date)=CURDATE()
        GROUP BY p.name
        ORDER BY quantity DESC
        LIMIT %s
    """, (limit,))

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

# ==========================================================
# BEST SELLING PRODUCTS
# ==========================================================

def get_best_selling_products(limit=5):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            p.name,
            SUM(si.quantity) AS sold_quantity
        FROM sale_items si
        JOIN products p
            ON si.product_id = p.product_id
        GROUP BY p.name
        ORDER BY sold_quantity DESC
        LIMIT %s
    """, (limit,))

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products

# ==========================================================
# TOP CUSTOMERS
# ==========================================================

def get_top_customers(limit=5):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            c.name,
            SUM(s.total_amount) AS total_spent
        FROM sales s
        JOIN customers c
            ON s.customer_id = c.customer_id
        GROUP BY c.name
        ORDER BY total_spent DESC
        LIMIT %s
    """, (limit,))

    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return customers

# ==========================================================
# MONTHLY SALES SUMMARY
# ==========================================================

def get_monthly_sales():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            MONTH(sale_date) AS month,
            COALESCE(SUM(total_amount),0) AS revenue
        FROM sales
        WHERE YEAR(sale_date)=YEAR(CURDATE())
        GROUP BY MONTH(sale_date)
        ORDER BY MONTH(sale_date)
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

# ==========================================================
# LAST 7 DAYS SALES
# ==========================================================

def get_weekly_sales():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            DATE(sale_date) AS day,
            SUM(total_amount)
        FROM sales
        WHERE sale_date >= CURDATE() - INTERVAL 6 DAY
        GROUP BY DATE(sale_date)
        ORDER BY DATE(sale_date)
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

# ==========================================================
# INVENTORY VALUE SUMMARY
# ==========================================================

def get_inventory_value():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(purchase_price * stock),0),
            COALESCE(SUM(selling_price * stock),0)
        FROM products
    """)

    purchase_value, selling_value = cursor.fetchone()

    cursor.close()
    connection.close()

    purchase_value = float(purchase_value)
    selling_value = float(selling_value)

    return {
        "purchase_value": purchase_value,
        "selling_value": selling_value,
        "expected_profit": selling_value - purchase_value
    }

# ==========================================================
# STOCK MOVEMENT HISTORY
# ==========================================================

def get_stock_movements(limit=20):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            sm.movement_date,
            p.name,
            sm.movement_type,
            sm.quantity,
            sm.stock_after
        FROM stock_movements sm
        JOIN products p
            ON sm.product_id = p.product_id
        ORDER BY sm.movement_id DESC
        LIMIT %s
    """, (limit,))

    movements = cursor.fetchall()

    cursor.close()
    connection.close()

    return movements

# ==========================================================
# SALES HISTORY / LEDGER
# ==========================================================

def get_sales_history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.sale_id,
            c.name,
            s.payment_method,
            s.total_amount,
            s.sale_date
        FROM sales s
        LEFT JOIN customers c
            ON s.customer_id = c.customer_id
        ORDER BY s.sale_id DESC
    """)

    sales = cursor.fetchall()

    cursor.close()
    connection.close()

    return sales

# ==========================================================
# RECENT SALES FOR DASHBOARD
# ==========================================================
def get_recent_sales(limit=5):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.sale_id,
            c.name,
            s.payment_method,
            s.total_amount,
            s.sale_date
        FROM sales s
        JOIN customers c
            ON s.customer_id = c.customer_id
        ORDER BY s.sale_date DESC
        LIMIT %s
    """, (limit,))

    sales = cursor.fetchall()

    cursor.close()
    connection.close()

    return sales

# ==========================================================
# TODAY'S PAYMENT ANALYTICS
# ==========================================================

def get_payment_analytics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            payment_method,
            COALESCE(SUM(total_amount), 0),
            COUNT(*)
        FROM sales
        WHERE DATE(sale_date) = CURDATE()
        GROUP BY payment_method
    """)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    # Default values
    analytics = {
        "Cash": {
            "amount": 0.0,
            "count": 0
        },
        "UPI": {
            "amount": 0.0,
            "count": 0
        },
        "Card": {
            "amount": 0.0,
            "count": 0
        }
    }

    # Fill today's values
    for payment, amount, count in result:

        if payment in analytics:
            analytics[payment] = {
                "amount": float(amount or 0),
                "count": int(count or 0)
            }

    # Most used payment method TODAY
    most_used = max(
        ["Cash", "UPI", "Card"],
        key=lambda method: analytics[method]["amount"]
    )

    analytics["most_used"] = most_used

    return analytics
# ==========================================================
# INVENTORY HEALTH ANALYTICS
# ==========================================================

def get_inventory_health():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT stock, minimum_stock
        FROM products
    """)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    total_products = len(products)

    healthy = 0
    low_stock = 0
    out_of_stock = 0

    for stock, minimum in products:

        if stock == 0:
            out_of_stock += 1

        elif stock <= minimum:
            low_stock += 1

        else:
            healthy += 1

    score = 0

    if total_products > 0:
        score = round((healthy / total_products) * 100)

    return {
        "healthy": healthy,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "score": score
    }