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

# ==========================================================
# ADD PRODUCT WITH BARCODE
# ==========================================================

def add_product_with_barcode(
    name,
    category,
    purchase_price,
    selling_price,
    stock,
    minimum_stock,
    barcode
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ------------------------------------------
        # Check duplicate barcode
        # ------------------------------------------

        barcode = barcode.strip()

        if barcode:

            cursor.execute(
                """
                SELECT product_id
                FROM products
                WHERE barcode = %s
                """,
                (barcode,)
            )

            existing = cursor.fetchone()

            if existing:

                return False, (
                    "Barcode already belongs to another product."
                )

        # ------------------------------------------
        # Insert product
        # ------------------------------------------

        cursor.execute(
            """
            INSERT INTO products
            (
                barcode,
                name,
                category,
                purchase_price,
                selling_price,
                stock,
                minimum_stock
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                barcode if barcode else None,
                name,
                category,
                purchase_price,
                selling_price,
                stock,
                minimum_stock
            )
        )

        product_id = cursor.lastrowid

        connection.commit()

        return True, product_id

    except Exception as error:

        connection.rollback()

        return False, str(error)

    finally:

        cursor.close()
        connection.close()


        
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
# ADD STOCK / RECORD PURCHASE
# ==========================================================

def add_stock(
    product_id,
    quantity_added,
    supplier_id=None,
    purchase_price=0
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # --------------------------------------------------
        # Validate quantity
        # --------------------------------------------------

        if quantity_added <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        # --------------------------------------------------
        # Validate purchase price
        # --------------------------------------------------

        if purchase_price < 0:
            raise ValueError(
                "Purchase price cannot be negative."
            )

        # --------------------------------------------------
        # Get current stock
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT stock
            FROM products
            WHERE product_id = %s
            FOR UPDATE
            """,
            (product_id,)
        )

        result = cursor.fetchone()

        if not result:
            raise ValueError(
                "Product not found."
            )

        current_stock = int(
            result[0]
        )

        new_stock = (
            current_stock
            + quantity_added
        )

        # --------------------------------------------------
        # Get supplier details
        # --------------------------------------------------

        supplier_name = None

        if supplier_id is not None:

            cursor.execute(
                """
                SELECT name
                FROM suppliers
                WHERE supplier_id = %s
                """,
                (supplier_id,)
            )

            supplier_result = cursor.fetchone()

            if not supplier_result:
                raise ValueError(
                    "Selected supplier was not found."
                )

            supplier_name = supplier_result[0]

        # --------------------------------------------------
        # Update product stock
        # --------------------------------------------------

        cursor.execute(
            """
            UPDATE products
            SET stock = %s
            WHERE product_id = %s
            """,
            (
                new_stock,
                product_id
            )
        )

        # --------------------------------------------------
        # Calculate total purchase cost
        # --------------------------------------------------

        total_cost = (
            quantity_added
            * float(purchase_price)
        )

        # --------------------------------------------------
        # Record purchase
        # --------------------------------------------------

        cursor.execute(
            """
            INSERT INTO purchases (
                product_id,
                supplier_id,
                supplier,
                quantity,
                purchase_price,
                total_cost
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                product_id,
                supplier_id,
                supplier_name,
                quantity_added,
                purchase_price,
                total_cost
            )
        )

        # --------------------------------------------------
        # Record stock movement
        # --------------------------------------------------

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
                product_id,
                "STOCK IN",
                quantity_added,
                new_stock
            )
        )

        connection.commit()

        return {
            "success": True,
            "new_stock": new_stock,
            "total_cost": total_cost
        }

    except Exception:

        connection.rollback()
        raise

    finally:

        cursor.close()
        connection.close()

# ==========================================================
# GET PURCHASE HISTORY
# ==========================================================

def get_purchase_history(limit=50):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            pu.purchase_id,
            pu.supplier,
            p.name,
            pu.quantity,
            pu.purchase_price,
            pu.total_cost,
            pu.purchase_date
        FROM purchases pu
        JOIN products p
            ON pu.product_id = p.product_id
        ORDER BY pu.purchase_date DESC
        LIMIT %s
    """, (limit,))

    purchases = cursor.fetchall()

    cursor.close()
    connection.close()

    return purchases

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
# GET PRODUCT BY BARCODE
# ==========================================================

def get_product_by_barcode(barcode):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            product_id,
            name,
            category,
            purchase_price,
            selling_price,
            stock,
            minimum_stock,
            barcode
        FROM products
        WHERE barcode = %s
    """, (barcode,))

    product = cursor.fetchone()

    cursor.close()
    connection.close()

    return product

# ==========================================================
# UPDATE PRODUCT BARCODE
# ==========================================================

def update_product_barcode(product_id, barcode):

    connection = get_connection()
    cursor = connection.cursor()

    barcode = barcode.strip()

    # Empty barcode means remove barcode
    if barcode == "":
        cursor.execute(
            """
            UPDATE products
            SET barcode = NULL
            WHERE product_id = %s
            """,
            (product_id,)
        )

    else:
        # Check duplicate
        cursor.execute(
            """
            SELECT product_id
            FROM products
            WHERE barcode = %s
            AND product_id != %s
            """,
            (barcode, product_id)
        )

        existing = cursor.fetchone()

        if existing:
            cursor.close()
            connection.close()
            return False

        cursor.execute(
            """
            UPDATE products
            SET barcode = %s
            WHERE product_id = %s
            """,
            (barcode, product_id)
        )

    connection.commit()

    cursor.close()
    connection.close()

    return True


# ==========================================================
# GENERATE UNIQUE INTERNAL BARCODE
# ==========================================================

def generate_product_barcode(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # --------------------------------------------------
        # Create a 12-digit internal barcode
        # --------------------------------------------------

        barcode = f"290{int(product_id):09d}"

        # --------------------------------------------------
        # Check whether it already exists
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT product_id
            FROM products
            WHERE barcode = %s
            """,
            (barcode,)
        )

        existing = cursor.fetchone()

        if existing and existing[0] != product_id:

            cursor.close()
            connection.close()

            return False, (
                "Generated barcode already belongs "
                "to another product."
            )

        # --------------------------------------------------
        # Save barcode
        # --------------------------------------------------

        cursor.execute(
            """
            UPDATE products
            SET barcode = %s
            WHERE product_id = %s
            """,
            (barcode, product_id)
        )

        connection.commit()

        return True, barcode

    except Exception as error:

        connection.rollback()

        return False, str(error)

    finally:

        cursor.close()
        connection.close()


# ==========================================================
# GET PRODUCTS WITH BARCODE
# ==========================================================

def get_products_with_barcodes():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            product_id,
            name,
            category,
            selling_price,
            stock,
            barcode
        FROM products
        ORDER BY product_id
    """)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products


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
        stock,
        barcode
    FROM products
    WHERE
        name LIKE %s
        OR category LIKE %s
        OR barcode LIKE %s
    ORDER BY name ASC
    """

    search_keyword = f"%{keyword}%"

    cursor.execute(
        query,
        (
            search_keyword,
            search_keyword,
            search_keyword
        )
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

    try:

        for item in cart:

            product_id = item["id"]
            quantity = int(item["quantity"])
            selling_price = float(item["price"])
            subtotal = float(item["subtotal"])

            # --------------------------------------------------
            # Get the CURRENT purchase cost of the product
            # --------------------------------------------------

            cursor.execute("""
                SELECT purchase_price
                FROM products
                WHERE product_id = %s
                FOR UPDATE
            """, (product_id,))

            result = cursor.fetchone()

            if not result:
                raise ValueError(
                    f"Product {product_id} not found."
                )

            purchase_price = float(
                result[0]
            )

            # --------------------------------------------------
            # Save sale item including purchase price
            # --------------------------------------------------

            cursor.execute("""
                INSERT INTO sale_items (
                    sale_id,
                    product_id,
                    quantity,
                    selling_price,
                    purchase_price,
                    subtotal
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                sale_id,
                product_id,
                quantity,
                selling_price,
                purchase_price,
                subtotal
            ))

            # --------------------------------------------------
            # Get current stock
            # --------------------------------------------------

            cursor.execute("""
                SELECT stock
                FROM products
                WHERE product_id = %s
                FOR UPDATE
            """, (product_id,))

            current_stock = cursor.fetchone()[0]

            # --------------------------------------------------
            # Check stock
            # --------------------------------------------------

            if current_stock < quantity:

                raise ValueError(
                    f"Insufficient stock for product ID "
                    f"{product_id}."
                )

            stock_after = (
                current_stock - quantity
            )

            # --------------------------------------------------
            # Update stock
            # --------------------------------------------------

            cursor.execute("""
                UPDATE products
                SET stock = %s
                WHERE product_id = %s
            """, (
                stock_after,
                product_id
            ))

            # --------------------------------------------------
            # Record SALE stock movement
            # --------------------------------------------------

            cursor.execute("""
                INSERT INTO stock_movements (
                    product_id,
                    movement_type,
                    quantity,
                    stock_after
                )
                VALUES (%s, %s, %s, %s)
            """, (
                product_id,
                "SALE",
                quantity,
                stock_after
            ))

        connection.commit()

    except Exception:

        connection.rollback()
        raise

    finally:

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
# TODAY'S PURCHASE ANALYTICS
# ==========================================================

def get_today_purchase_analytics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(total_cost), 0),
            COUNT(*)
        FROM purchases
        WHERE DATE(purchase_date) = CURDATE()
    """)

    total_amount, transaction_count = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "amount": float(total_amount or 0),
        "count": int(transaction_count or 0)
    }


# ==========================================================
# TODAY'S REALIZED PROFIT ANALYTICS
# RETURN-AWARE
# ==========================================================

def get_today_profit_analytics():

    connection = get_connection()
    cursor = connection.cursor()

    # ------------------------------------------------------
    # Total revenue and original COGS from today's sales
    # ------------------------------------------------------

    cursor.execute("""
        SELECT
            COALESCE(SUM(si.subtotal), 0),
            COALESCE(
                SUM(
                    si.purchase_price * si.quantity
                ),
                0
            )
        FROM sale_items si
        JOIN sales s
            ON si.sale_id = s.sale_id
        WHERE DATE(s.sale_date) = CURDATE()
    """)

    sales_revenue, sales_cogs = cursor.fetchone()

    sales_revenue = float(
        sales_revenue or 0
    )

    sales_cogs = float(
        sales_cogs or 0
    )

    # ------------------------------------------------------
    # Today's refunds
    # ------------------------------------------------------

    cursor.execute("""
        SELECT
            COALESCE(SUM(r.refund_amount), 0)
        FROM returns r
        WHERE DATE(r.return_date) = CURDATE()
    """)

    total_refunds = float(
        cursor.fetchone()[0] or 0
    )

    # ------------------------------------------------------
    # Cost of returned items
    #
    # Use the historical purchase_price saved in sale_items
    # ------------------------------------------------------

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(
                    si.purchase_price * r.quantity
                ),
                0
            )
        FROM returns r
        JOIN sale_items si
            ON r.sale_item_id = si.sale_item_id
        WHERE DATE(r.return_date) = CURDATE()
    """)

    returned_cogs = float(
        cursor.fetchone()[0] or 0
    )

    # ------------------------------------------------------
    # Return-aware calculations
    # ------------------------------------------------------

    net_revenue = (
        sales_revenue
        - total_refunds
    )

    net_cogs = (
        sales_cogs
        - returned_cogs
    )

    gross_profit = (
        net_revenue
        - net_cogs
    )

    profit_margin = (
        (gross_profit / net_revenue) * 100
        if net_revenue > 0
        else 0
    )

    cursor.close()
    connection.close()

    return {
        "revenue": sales_revenue,
        "refunds": total_refunds,
        "net_revenue": net_revenue,
        "cost_of_goods": sales_cogs,
        "returned_cogs": returned_cogs,
        "net_cogs": net_cogs,
        "gross_profit": gross_profit,
        "profit_margin": profit_margin
    }


# ==========================================================
# SUPPLIER MANAGEMENT
# ==========================================================

def get_all_suppliers():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            supplier_id,
            name,
            phone,
            email,
            address,
            notes,
            created_at
        FROM suppliers
        ORDER BY name ASC
    """)

    suppliers = cursor.fetchall()

    cursor.close()
    connection.close()

    return suppliers


def search_suppliers(keyword):

    connection = get_connection()
    cursor = connection.cursor()

    search_keyword = f"%{keyword}%"

    cursor.execute("""
        SELECT
            supplier_id,
            name,
            phone,
            email,
            address,
            notes,
            created_at
        FROM suppliers
        WHERE
            name LIKE %s
            OR phone LIKE %s
            OR email LIKE %s
        ORDER BY name ASC
    """, (
        search_keyword,
        search_keyword,
        search_keyword
    ))

    suppliers = cursor.fetchall()

    cursor.close()
    connection.close()

    return suppliers


def add_supplier(
    name,
    phone=None,
    email=None,
    address=None,
    notes=None
):

    name = name.strip()

    if not name:
        raise ValueError(
            "Supplier name is required."
        )

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO suppliers (
                name,
                phone,
                email,
                address,
                notes
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            name,
            phone.strip() if phone else None,
            email.strip() if email else None,
            address.strip() if address else None,
            notes.strip() if notes else None
        ))

        connection.commit()

        supplier_id = cursor.lastrowid

        return supplier_id

    except Exception:

        connection.rollback()
        raise

    finally:

        cursor.close()
        connection.close()


def update_supplier(
    supplier_id,
    name,
    phone=None,
    email=None,
    address=None,
    notes=None
):

    name = name.strip()

    if not name:
        raise ValueError(
            "Supplier name is required."
        )

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE suppliers
            SET
                name = %s,
                phone = %s,
                email = %s,
                address = %s,
                notes = %s
            WHERE supplier_id = %s
        """, (
            name,
            phone.strip() if phone else None,
            email.strip() if email else None,
            address.strip() if address else None,
            notes.strip() if notes else None,
            supplier_id
        ))

        connection.commit()

        return True

    except Exception:

        connection.rollback()
        raise

    finally:

        cursor.close()
        connection.close()


def delete_supplier(supplier_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Check whether supplier has purchase records
        cursor.execute("""
            SELECT COUNT(*)
            FROM purchases
            WHERE supplier_id = %s
        """, (supplier_id,))

        purchase_count = cursor.fetchone()[0]

        if purchase_count > 0:

            raise ValueError(
                "This supplier has purchase records "
                "and cannot be deleted."
            )

        cursor.execute("""
            DELETE FROM suppliers
            WHERE supplier_id = %s
        """, (supplier_id,))

        connection.commit()

        return True

    except Exception:

        connection.rollback()
        raise

    finally:

        cursor.close()
        connection.close()


# ==========================================================
# SUPPLIER SUMMARY
# ==========================================================

def get_supplier_summary(supplier_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(total_cost), 0),
            COUNT(*),
            COALESCE(SUM(quantity), 0),
            MAX(purchase_date)
        FROM purchases
        WHERE supplier_id = %s
    """, (supplier_id,))

    total_spent, purchase_count, total_units, last_purchase = (
        cursor.fetchone()
    )

    cursor.close()
    connection.close()

    return {
        "total_spent": float(total_spent or 0),
        "purchase_count": int(purchase_count or 0),
        "total_units": int(total_units or 0),
        "last_purchase": last_purchase
    }

# ==========================================================
# SUPPLIER PURCHASE HISTORY
# ==========================================================

def get_supplier_purchase_history(supplier_id, limit=50):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            pu.purchase_id,
            p.name,
            pu.quantity,
            pu.purchase_price,
            pu.total_cost,
            pu.purchase_date
        FROM purchases pu
        JOIN products p
            ON pu.product_id = p.product_id
        WHERE pu.supplier_id = %s
        ORDER BY pu.purchase_date DESC
        LIMIT %s
    """, (
        supplier_id,
        limit
    ))

    history = cursor.fetchall()

    cursor.close()
    connection.close()

    return history


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


# ==========================================================
# GET SALE ITEMS FOR RETURN
# ==========================================================

def get_sale_items_for_return(sale_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            si.sale_item_id,
            si.product_id,
            p.name,
            si.quantity,
            si.selling_price,
            si.subtotal,
            COALESCE(
                (
                    SELECT SUM(r.quantity)
                    FROM returns r
                    WHERE r.sale_item_id = si.sale_item_id
                ),
                0
            ) AS returned_quantity
        FROM sale_items si
        JOIN products p
            ON si.product_id = p.product_id
        WHERE si.sale_id = %s
        ORDER BY si.sale_item_id
    """, (sale_id,))

    items = cursor.fetchall()

    cursor.close()
    connection.close()

    return items

# ==========================================================
# GET SALE DETAILS FOR RETURN
# ==========================================================

def get_sale_for_return(sale_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            sale_id,
            customer_id,
            total_amount,
            gst_amount,
            discount_amount,
            payment_method,
            sale_date
        FROM sales
        WHERE sale_id = %s
    """, (sale_id,))

    sale = cursor.fetchone()

    cursor.close()
    connection.close()

    return sale


# ==========================================================
# GET RETURN HISTORY
# ==========================================================

def get_return_history(limit=50):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            r.return_id,
            r.sale_id,
            COALESCE(c.name, 'Walk-in Customer'),
            p.name,
            r.quantity,
            r.refund_amount,
            r.return_date
        FROM returns r
        JOIN sales s
            ON r.sale_id = s.sale_id
        LEFT JOIN customers c
            ON s.customer_id = c.customer_id
        JOIN products p
            ON r.product_id = p.product_id
        ORDER BY r.return_date DESC
        LIMIT %s
    """, (limit,))

    returns = cursor.fetchall()

    cursor.close()
    connection.close()

    return returns


# ==========================================================
# PROCESS PRODUCT RETURN
# ==========================================================

def process_return(
    sale_id,
    sale_item_id,
    product_id,
    quantity
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # --------------------------------------------------
        # Validate quantity
        # --------------------------------------------------

        if quantity <= 0:
            raise ValueError(
                "Return quantity must be greater than zero."
            )

        # --------------------------------------------------
        # Get original sale item
        # --------------------------------------------------

        cursor.execute("""
            SELECT
                quantity,
                selling_price
            FROM sale_items
            WHERE
                sale_item_id = %s
                AND sale_id = %s
                AND product_id = %s
            FOR UPDATE
        """, (
            sale_item_id,
            sale_id,
            product_id
        ))

        sale_item = cursor.fetchone()

        if not sale_item:
            raise ValueError(
                "Sale item not found."
            )

        sold_quantity = int(
            sale_item[0]
        )

        selling_price = float(
            sale_item[1]
        )

        # --------------------------------------------------
        # Calculate already returned quantity
        # --------------------------------------------------

        cursor.execute("""
            SELECT COALESCE(
                SUM(quantity),
                0
            )
            FROM returns
            WHERE sale_item_id = %s
        """, (sale_item_id,))

        already_returned = int(
            cursor.fetchone()[0]
        )

        # --------------------------------------------------
        # Calculate remaining returnable quantity
        # --------------------------------------------------

        remaining_quantity = (
            sold_quantity
            - already_returned
        )

        if quantity > remaining_quantity:

            raise ValueError(
                f"Only {remaining_quantity} "
                f"unit(s) can still be returned."
            )

        # --------------------------------------------------
        # Calculate refund
        # --------------------------------------------------

        refund_amount = (
            selling_price * quantity
        )

        # --------------------------------------------------
        # Record return
        # --------------------------------------------------

        cursor.execute("""
            INSERT INTO returns (
                sale_id,
                sale_item_id,
                product_id,
                quantity,
                refund_amount
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """, (
            sale_id,
            sale_item_id,
            product_id,
            quantity,
            refund_amount
        ))

        # --------------------------------------------------
        # Return stock to inventory
        # --------------------------------------------------

        cursor.execute("""
            UPDATE products
            SET stock = stock + %s
            WHERE product_id = %s
        """, (
            quantity,
            product_id
        ))

        # --------------------------------------------------
        # Get updated stock
        # --------------------------------------------------

        cursor.execute("""
            SELECT stock
            FROM products
            WHERE product_id = %s
        """, (product_id,))

        stock_after = cursor.fetchone()[0]

        # --------------------------------------------------
        # Record RETURN stock movement
        # --------------------------------------------------

        cursor.execute("""
            INSERT INTO stock_movements (
                product_id,
                movement_type,
                quantity,
                stock_after
            )
            VALUES (
                %s,
                %s,
                %s,
                %s
            )
        """, (
            product_id,
            "RETURN",
            quantity,
            stock_after
        ))

        connection.commit()

        return {
            "success": True,
            "refund_amount": refund_amount,
            "returned_quantity": quantity,
            "remaining_returnable": (
                remaining_quantity - quantity
            )
        }

    except Exception:

        connection.rollback()
        raise

    finally:

        cursor.close()
        connection.close()