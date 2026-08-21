# gui/billing.py (Clean Version)


import customtkinter as ctk
from tkinter import ttk, messagebox

from backend import (
    get_products_for_billing,
    get_or_create_customer,
    get_customer_by_phone,
    create_sale,
    add_sale_items,
    update_stock_after_sale
)

from invoice import generate_invoice

class BillingPage(ctk.CTkScrollableFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="#F9FAFB",
            corner_radius=0
        )

        # ---------------- Billing Data ----------------
        self.cart = []              # Temporary billing cart
        self.products_data = {}     # Product lookup dictionary

        # Build UI
        self.build_ui()

        # Load products from database
        self.load_products()

    # ==========================================================
    # LOAD PRODUCTS FROM DATABASE
    # ==========================================================
    def load_products(self):

        products = get_products_for_billing()

        self.products_data = {}
        product_names = []

        for product_id, name, price, stock in products:

            display_name = name.title()

            product_names.append(display_name)

            self.products_data[display_name] = {
                "id": product_id,
                "price": float(price),
                "stock": int(stock)
            }

        if product_names:
            self.product_combo.configure(values=product_names)
            self.product_combo.set(product_names[0])

    # ==========================================================
    # FETCH CUSTOMER FROM PHONE NUMBER
    # ==========================================================

    def fetch_customer(self, event=None):

        phone = self.phone_var.get().strip()

        # Wait until phone number is complete
        if len(phone) != 10:
            self.customer_name_var.set("")
            self.points_var.set("⭐ Loyalty Points : 0")
            return

        customer = get_customer_by_phone(phone)

        if customer:

            self.customer_name_var.set(customer["name"])

            self.points_var.set(
                f"⭐ Loyalty Points : {customer['loyalty_points']}"
            )

        else:

            self.customer_name_var.set("")
            self.points_var.set("⭐ Loyalty Points : New Customer")

    # ==========================================================
    # ADD PRODUCT TO BILLING CART
    # ==========================================================
    def add_item_to_cart(self):

        product_name = self.product_var.get()

        if product_name == "":
            messagebox.showwarning(
                "Product Required",
                "Please select a product."
            )
            return

        # Quantity Validation
        try:
            quantity = int(self.quantity_var.get())

            if quantity <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Enter a valid quantity."
            )
            return

        product = self.products_data[product_name]

        # Stock Validation
        if quantity > product["stock"]:
            messagebox.showerror(
                "Stock Error",
                f"Only {product['stock']} items available."
            )
            return

        subtotal = product["price"] * quantity

        # Check if already exists in cart
        for item in self.cart:

            if item["id"] == product["id"]:

                new_quantity = item["quantity"] + quantity

                if new_quantity > product["stock"]:
                    messagebox.showerror(
                        "Stock Error",
                        "Quantity exceeds available stock."
                    )
                    return

                item["quantity"] = new_quantity
                item["subtotal"] = item["price"] * new_quantity

                self.refresh_cart()
                self.quantity_var.set("1")
                return

        # Add New Item
        self.cart.append({
            "id": product["id"],
            "name": product_name,
            "price": product["price"],
            "quantity": quantity,
            "subtotal": subtotal
        })

        self.refresh_cart()

        # Reset quantity
        self.quantity_var.set("1")

    # ==========================================================
    # REFRESH BILLING CART TABLE
    # ==========================================================
    def refresh_cart(self):

        # Clear table
        for row in self.cart_table.get_children():
            self.cart_table.delete(row)

        subtotal = 0

        for item in self.cart:

            subtotal += item["subtotal"]

            self.cart_table.insert(
                "",
                "end",
                values=(
                    item["name"],
                    f"₹{item['price']:.2f}",
                    item["quantity"],
                    f"₹{item['subtotal']:.2f}"
                )
            )

        self.calculate_summary(subtotal)

    # ==========================================================
    # REMOVE SELECTED ITEM
    # ==========================================================

    def remove_selected_item(self):

        selected = self.cart_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an item from the cart."
            )
            return

        selected_values = self.cart_table.item(selected[0])["values"]

        product_name = selected_values[0]

        self.cart = [
            item for item in self.cart
            if item["name"] != product_name
        ]

        self.refresh_cart()

    # ==========================================================
    # INCREASE PRODUCT QUANTITY
    # ==========================================================

    def increase_quantity(self):

        selected = self.cart_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an item."
            )
            return

        product_name = self.cart_table.item(selected[0])["values"][0]

        product = self.products_data[product_name]

        for item in self.cart:

            if item["name"] == product_name:

                if item["quantity"] >= product["stock"]:
                    messagebox.showerror(
                        "Stock Error",
                        "No more stock available."
                    )
                    return

                item["quantity"] += 1
                item["subtotal"] = item["quantity"] * item["price"]

                break

        self.refresh_cart()

        # ==========================================================
        # DECREASE PRODUCT QUANTITY
        # ==========================================================

    def decrease_quantity(self):

        selected = self.cart_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an item."
            )
            return

        product_name = self.cart_table.item(selected[0])["values"][0]

        for item in self.cart:

            if item["name"] == product_name:

                item["quantity"] -= 1

                if item["quantity"] <= 0:
                    self.cart.remove(item)

                else:
                    item["subtotal"] = item["quantity"] * item["price"]

                break

        self.refresh_cart()
    # ==========================================================
    # BILL SUMMARY CALCULATION
    # ==========================================================

    def calculate_summary(self, subtotal):

        # Read discount %
        try:
            discount_percent = float(self.discount_percent_var.get())

            if discount_percent < 0:
                discount_percent = 0

            if discount_percent > 100:
                discount_percent = 100

        except ValueError:
            discount_percent = 0

        # Calculate discount
        discount_amount = subtotal * (discount_percent / 100)

        taxable_amount = subtotal - discount_amount

        gst = taxable_amount * 0.18

        grand_total = taxable_amount + gst

        # Update UI
        self.subtotal_var.set(f"₹{subtotal:.2f}")
        self.discount_var.set(f"₹{discount_amount:.2f}")
        self.gst_var.set(f"₹{gst:.2f}")
        self.total_var.set(f"₹{grand_total:.2f}")

    # ==========================================================
    # GENERATE COMPLETE BILL
    # ==========================================================

    def generate_bill(self):

        # ---------------- Customer Validation ----------------
        customer_name = self.customer_name_var.get().strip()
        phone = self.phone_var.get().strip()
        payment = self.payment_method_var.get()

        if customer_name == "" or phone == "":
            messagebox.showerror(
                "Missing Details",
                "Enter customer name and phone number."
            )
            return

        if len(self.cart) == 0:
            messagebox.showwarning(
                "Empty Cart",
                "Please add products to the cart."
            )
            return

        # ---------------- Calculate Totals ----------------
        subtotal = sum(item["subtotal"] for item in self.cart)

        try:
            discount_percent = float(self.discount_percent_var.get())
        except ValueError:
            discount_percent = 0

        discount = subtotal * (discount_percent / 100)

        taxable_amount = subtotal - discount

        gst = taxable_amount * 0.18

        grand_total = taxable_amount + gst
        # ---------------- Customer ----------------
        customer_id = get_or_create_customer(customer_name, phone)

        # ---------------- Create Sale ----------------
        sale_id = create_sale(
            customer_id=customer_id,
            total=grand_total,
            gst=gst,
            discount=discount,
            payment_method=payment
        )

        # ---------------- Save Sale Items ----------------
        add_sale_items(sale_id, self.cart)

        # ---------------- Update Stock ----------------
        update_stock_after_sale(self.cart)

        # ---------------- Generate Invoice PDF ----------------
        invoice_path = generate_invoice(
            sale_id=sale_id,
            customer_name=customer_name,
            phone=phone,
            payment_method=payment,
            cart=self.cart,
            subtotal=subtotal,
            gst=gst,
            discount=discount,
            grand_total=grand_total
        )

        # ---------------- Success Popup ----------------
        messagebox.showinfo(
            "Bill Generated Successfully",
            f"Invoice Saved Successfully!\n\n{invoice_path}"
        )

        # ---------------- Reset Billing Screen ----------------
        self.cart.clear()
        self.refresh_cart()

        self.phone_var.set("")
        self.customer_name_var.set("")
        self.payment_method_var.set("Cash")
        self.quantity_var.set("1")
        self.discount_percent_var.set("0")
    # ==========================================================
    # BUILD USER INTERFACE
    # ==========================================================
    def build_ui(self):

        # ---------------- Page Title ----------------
        ctk.CTkLabel(
            self,
            text="🛒 Billing / Point of Sale",
            font=("Poppins", 28, "bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=30, pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="Create customer bills, add products and generate invoices.",
            font=("Poppins", 13),
            text_color="gray40"
        ).pack(anchor="w", padx=30)

        # ======================================================
        # CUSTOMER INFORMATION
        # ======================================================

        customer_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=18,
            border_width=1,
            border_color="#D1D5DB"
        )

        customer_frame.pack(fill="x", padx=30, pady=(20, 10))

        customer_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            customer_frame,
            text="Customer Information",
            font=("Poppins", 18, "bold"),
            text_color="#065F46"
        ).grid(row=0, column=0, columnspan=3,
               sticky="w", padx=20, pady=(15, 15))

        self.phone_var = ctk.StringVar()
        self.customer_name_var = ctk.StringVar()
        self.payment_method_var = ctk.StringVar(value="Cash")
        self.points_var = ctk.StringVar(value="⭐ Loyalty Points : 0")


        # Phone
        ctk.CTkLabel(customer_frame, text="Phone Number").grid(
            row=1, column=0, sticky="w", padx=20)

        self.phone_entry = ctk.CTkEntry(
            customer_frame,
            textvariable=self.phone_var,
            placeholder_text="Enter phone number",
            height=38
        )

        self.phone_entry.grid(
            row=2, column=0, padx=20, pady=(5, 15), sticky="ew")
        self.phone_entry.bind("<KeyRelease>", self.fetch_customer)

        # Name
        ctk.CTkLabel(customer_frame, text="Customer Name").grid(
            row=1, column=1, sticky="w", padx=20)

        self.customer_entry = ctk.CTkEntry(
            customer_frame,
            textvariable=self.customer_name_var,
            placeholder_text="Customer name",
            height=38
        )

        self.customer_entry.grid(
            row=2, column=1, padx=20, pady=(5, 15), sticky="ew")

        # Loyalty Points
        self.points_label = ctk.CTkLabel(
            customer_frame,
            textvariable=self.points_var,
            font=("Poppins", 12, "bold"),
            text_color="#16A34A"
        )

        self.points_label.grid(
            row=3,
            column=1,
            padx=20,
            pady=(0,15),
            sticky="w"
        )

        # Payment Method
        ctk.CTkLabel(customer_frame, text="Payment Method").grid(
            row=1, column=2, sticky="w", padx=20)

        self.payment_combo = ctk.CTkComboBox(
            customer_frame,
            values=["Cash", "UPI", "Card"],
            variable=self.payment_method_var,
            height=38
        )

        self.payment_combo.grid(
            row=2, column=2, padx=20, pady=(5, 15), sticky="ew")

        # ======================================================
        # PRODUCT SELECTION
        # ======================================================

        product_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=18,
            border_width=1,
            border_color="#D1D5DB"
        )

        product_frame.pack(fill="x", padx=30, pady=10)

        product_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            product_frame,
            text="Add Products",
            font=("Poppins", 18, "bold"),
            text_color="#065F46"
        ).grid(row=0, column=0, columnspan=3,
               sticky="w", padx=20, pady=(15, 15))

        self.product_var = ctk.StringVar()
        self.quantity_var = ctk.StringVar(value="1")

        # Product Dropdown
        ctk.CTkLabel(product_frame, text="Product").grid(
            row=1, column=0, sticky="w", padx=20)

        self.product_combo = ctk.CTkComboBox(
            product_frame,
            values=["Loading Products..."],
            variable=self.product_var,
            height=38
        )

        self.product_combo.grid(
            row=2, column=0, padx=20, pady=(5, 15), sticky="ew")

        # Quantity
        ctk.CTkLabel(product_frame, text="Quantity").grid(
            row=1, column=1, sticky="w", padx=20)

        self.quantity_entry = ctk.CTkEntry(
            product_frame,
            textvariable=self.quantity_var,
            height=38
        )

        self.quantity_entry.grid(
            row=2, column=1, padx=20, pady=(5, 15), sticky="ew")

        # Add Button
        self.add_item_button = ctk.CTkButton(
            product_frame,
            text="+ Add Item",
            fg_color="#16A34A",
            hover_color="#15803D",
            height=40,
            command=self.add_item_to_cart
        )

        self.add_item_button.grid(
            row=2, column=2, padx=20, pady=(5, 15), sticky="ew")

        # ======================================================
        # BILLING CART
        # ======================================================

        cart_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=18,
            border_width=1,
            border_color="#D1D5DB"
        )
        cart_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(
            cart_frame,
            text="Billing Cart",
            font=("Poppins", 18, "bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=20, pady=(15, 10))

        # ---------- Main Layout ----------
        cart_body = ctk.CTkFrame(cart_frame, fg_color="transparent")
        cart_body.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        cart_body.grid_columnconfigure(0, weight=4)
        cart_body.grid_columnconfigure(1, weight=1)

        # ---------- Table ----------
        table_frame = ctk.CTkFrame(cart_body, fg_color="transparent")
        table_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        columns = ("Product", "Price", "Quantity", "Subtotal")

        self.cart_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        for col in columns:
            self.cart_table.heading(col, text=col)

        self.cart_table.column("Product", width=220)
        self.cart_table.column("Price", width=110, anchor="center")
        self.cart_table.column("Quantity", width=100, anchor="center")
        self.cart_table.column("Subtotal", width=130, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.cart_table.yview
        )

        self.cart_table.configure(yscrollcommand=scrollbar.set)

        self.cart_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ---------- Buttons ----------
        button_panel = ctk.CTkFrame(cart_body, fg_color="transparent")
        button_panel.grid(row=0, column=1, sticky="n")

        self.plus_button = ctk.CTkButton(
            button_panel,
            text="➕ Quantity",
            width=150,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.increase_quantity
        )
        self.plus_button.pack(fill="x", pady=(0, 10))

        self.minus_button = ctk.CTkButton(
            button_panel,
            text="➖ Quantity",
            width=150,
            fg_color="#F59E0B",
            hover_color="#D97706",
            command=self.decrease_quantity
        )
        self.minus_button.pack(fill="x", pady=(0, 10))

        self.remove_button = ctk.CTkButton(
            button_panel,
            text="🗑 Remove Selected",
            width=150,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.remove_selected_item
        )
        self.remove_button.pack(fill="x")
        # ======================================================
        # BILL SUMMARY
        # ======================================================

        summary_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=18,
            border_width=1,
            border_color="#D1D5DB"
        )

        summary_frame.pack(fill="x", padx=30, pady=(10, 30))

        # Three columns
        summary_frame.grid_columnconfigure(0, weight=3)  # Labels
        summary_frame.grid_columnconfigure(1, weight=1)  # Discount input
        summary_frame.grid_columnconfigure(2, weight=2)  # Amounts

        ctk.CTkLabel(
            summary_frame,
            text="Bill Summary",
            font=("Poppins", 18, "bold"),
            text_color="#065F46"
        ).grid(row=0, column=0, columnspan=2,
               sticky="w", padx=20, pady=(15, 15))

        # Variables
        self.subtotal_var = ctk.StringVar(value="₹0.00")
        self.discount_percent_var = ctk.StringVar(value="0")
        self.discount_var = ctk.StringVar(value="₹0.00")
        self.gst_var = ctk.StringVar(value="₹0.00")
        self.total_var = ctk.StringVar(value="₹0.00")

        def summary_row(title, variable, row):

            ctk.CTkLabel(
                summary_frame,
                text=title,
                font=("Poppins", 14)
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=20,
                pady=8
            )

            ctk.CTkLabel(
                summary_frame,
                textvariable=variable,
                font=("Poppins", 14, "bold"),
                text_color="#065F46"
            ).grid(
                row=row,
                column=2,
                sticky="e",
                padx=20,
                pady=8
            )
        summary_row("Subtotal", self.subtotal_var, 1)

       # ---------------- Discount Percentage ----------------

        ctk.CTkLabel(
            summary_frame,
            text="Discount (%)",
            font=("Poppins", 14)
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=8
        )

        discount_entry = ctk.CTkEntry(
            summary_frame,
            textvariable=self.discount_percent_var,
            width=60,
            height=30,
            justify="center"
        )

        discount_entry.grid(
            row=2,
            column=1,
            sticky="w",
            padx=(10, 0)
        )

        discount_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh_cart()
        )

        summary_row("Discount", self.discount_var, 2)
        summary_row("GST (18%)", self.gst_var, 3)

        ctk.CTkFrame(
            summary_frame,
            height=2,
            fg_color="#D1D5DB"
        ).grid(row=5, column=0, columnspan=2,
               sticky="ew", padx=20, pady=10)

        summary_row("Grand Total", self.total_var, 5)

        self.generate_button = ctk.CTkButton(
            summary_frame,
            text="🧾 Generate Bill",
            fg_color="#16A34A",
            hover_color="#15803D",
            height=45,
            font=("Poppins", 15, "bold"),
            command=self.generate_bill

        )

        self.generate_button.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=(15, 20)
        )

