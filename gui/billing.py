# gui/billing.py (Clean Version)


import customtkinter as ctk
from tkinter import ttk, messagebox


from backend import (
    get_products_for_billing,
    get_or_create_customer,
    get_customer_by_phone,
    create_sale,
    add_sale_items,
    update_stock_after_sale,
    add_loyalty_points,
    get_product_by_barcode
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
        self.barcode_var = ctk.StringVar()
        self.products_data = {}     # Product lookup dictionary

        self.customer_id = None

        # Build UI
        self.build_ui()

        # Load products from database
        self.load_products()    

        # ==========================================================
        # KEYBOARD POS CONTROLS
        # ==========================================================
        self.bind_all("<plus>", self._keyboard_increase)
        self.bind_all("<KP_Add>", self._keyboard_increase)
        self.bind_all("<minus>", self._keyboard_decrease)
        self.bind_all("<KP_Subtract>", self._keyboard_decrease)
        self.bind_all("<Delete>", self._keyboard_delete)
        self.bind_all("<Control-b>", self._keyboard_generate_bill)
        self.bind_all("<Escape>", self._keyboard_escape)
        self.bind_all("<F2>", self._keyboard_focus_product)
        self.bind_all("<F3>", self._keyboard_focus_barcode)
        self.bind_all("<F4>", self._keyboard_focus_quantity)
        self.bind_all("<F5>", self._keyboard_focus_phone)
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
    #FETCH CUSTOMER DETAILS
    # ==========================================================

    def fetch_customer_details(self, event=None):

        phone = self.phone_var.get().strip()

        # Incomplete phone number
        if len(phone) != 10:

            self.customer_name_var.set("")
            self.points_var.set("⭐ Loyalty Points : 0")
            self.customer_id = None

            self.update_receipt_preview()

            return

        customer = get_customer_by_phone(phone)

        if customer:

            self.customer_id = customer["customer_id"]

            self.customer_name_var.set(
                customer["name"]
            )

            self.points_var.set(
                f"⭐ Loyalty Points : {customer['loyalty_points']}"
            )

        else:

            self.customer_id = None

            self.customer_name_var.set("")

            self.points_var.set(
                "⭐ Loyalty Points : New Customer"
            )

        # Update receipt immediately
        self.update_receipt_preview()
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
    # BARCODE SCANNER
    # ==========================================================

    def scan_barcode(self, event=None):

        barcode = self.barcode_var.get().strip()

        if not barcode:
            return "break"

        product = get_product_by_barcode(barcode)

        if not product:

            messagebox.showerror(
                "Barcode Not Found",
                f"No product found for barcode:\n{barcode}"
            )

            self.barcode_var.set("")
            self.barcode_entry.focus_set()

            return "break"

        # -----------------------------
        # Stock Check
        # -----------------------------

        if product["stock"] <= 0:

            messagebox.showerror(
                "Out of Stock",
                f"{product['name'].title()} is currently out of stock."
            )

            self.barcode_var.set("")
            self.barcode_entry.focus_set()

            return "break"

        # -----------------------------
        # Add to Existing Cart
        # -----------------------------

        for item in self.cart:

            if item["id"] == product["product_id"]:

                if item["quantity"] >= product["stock"]:

                    messagebox.showerror(
                        "Stock Limit",
                        "No more stock available for this product."
                    )

                    self.barcode_var.set("")
                    self.barcode_entry.focus_set()

                    return "break"

                item["quantity"] += 1
                item["subtotal"] = (
                    item["quantity"] * item["price"]
                )

                self.refresh_cart()

                self.barcode_var.set("")
                self.barcode_entry.focus_set()

                return "break"

        # -----------------------------
        # Add New Product
        # -----------------------------

        self.cart.append({
            "id": product["product_id"],
            "name": product["name"].title(),
            "price": float(product["selling_price"]),
            "quantity": 1,
            "subtotal": float(product["selling_price"])
            })

        self.refresh_cart()

        self.barcode_var.set("")
        self.barcode_entry.focus_set()

        return "break"

    # ==========================================================
    # UPDATE LIVE RECEIPT PREVIEW
    # ==========================================================

    def update_receipt_preview(self):

        # Customer
        customer_name = (
            self.customer_name_var.get().strip()
            or "Walk-in Customer"
        )

        phone = (
            self.phone_var.get().strip()
            or "--"
        )

        payment = self.payment_method_var.get() or "Cash"

        self.receipt_customer_var.set(
            f"Customer: {customer_name}"
        )

        self.receipt_phone_var.set(
            f"Phone: {phone}"
        )

        self.receipt_payment_var.set(
            f"Payment: {payment}"
        )

        # Clear old products
        for widget in self.receipt_items_frame.winfo_children():
            widget.destroy()

        # Empty cart
        if not self.cart:

            ctk.CTkLabel(
                self.receipt_items_frame,
                text="No items added yet",
                font=("Poppins", 11),
                text_color="#94A3B8"
            ).pack(
                pady=15
            )

        else:

            for item in self.cart:

                row = ctk.CTkFrame(
                    self.receipt_items_frame,
                    fg_color="transparent"
                )

                row.pack(
                    fill="x",
                    pady=3
                )

                product_text = (
                    f"{item['name'].title()} × {item['quantity']}"
                )

                price_text = (
                    f"₹{item['subtotal']:,.2f}"
                )

                ctk.CTkLabel(
                    row,
                    text=product_text,
                    font=("Poppins", 11),
                    anchor="w"
                ).pack(
                    side="left"
                )

                ctk.CTkLabel(
                    row,
                    text=price_text,
                    font=("Poppins", 11),
                    anchor="e"
                ).pack(
                    side="right"
                )

        # Totals
        subtotal = sum(
            item["subtotal"]
            for item in self.cart
        )

        try:
            discount_percent = float(
                self.discount_percent_var.get() or 0
            )
        except ValueError:
            discount_percent = 0

        discount = subtotal * (
            discount_percent / 100
        )

        taxable_amount = subtotal - discount

        gst = taxable_amount * 0.18

        grand_total = taxable_amount + gst

        self.receipt_subtotal_var.set(
            f"₹{subtotal:,.2f}"
        )

        self.receipt_discount_var.set(
            f"₹{discount:,.2f}"
        )

        self.receipt_gst_var.set(
            f"₹{gst:,.2f}"
        )

        self.receipt_total_var.set(
            f"₹{grand_total:,.2f}"
        )
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
        self.update_receipt_preview()

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

        product_name = self.cart_table.item(
            selected[0]
        )["values"][0]

        # --------------------------------------------------
        # Find the actual cart item
        # --------------------------------------------------

        cart_item = None

        for item in self.cart:

            if item["name"].lower() == str(product_name).lower():

                cart_item = item
                break

        if cart_item is None:

            messagebox.showerror(
                "Cart Error",
                "Unable to find the selected product in the cart."
            )
            return

        # --------------------------------------------------
        # Find product stock by PRODUCT ID
        # --------------------------------------------------

        product = None

        for product_data in self.products_data.values():

            if product_data["id"] == cart_item["id"]:

                product = product_data
                break

        if product is None:

            messagebox.showerror(
                "Product Error",
                "Unable to find product stock information."
            )
            return

        # --------------------------------------------------
        # Stock validation
        # --------------------------------------------------

        if cart_item["quantity"] >= product["stock"]:

            messagebox.showerror(
                "Stock Error",
                "No more stock available."
            )
            return

        # --------------------------------------------------
        # Increase quantity
        # --------------------------------------------------

        cart_item["quantity"] += 1

        cart_item["subtotal"] = (
            cart_item["quantity"] * cart_item["price"]
        )

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

        discount_percent = float(self.discount_percent_var.get() or 0)

        discount = subtotal * discount_percent / 100

        taxable_amount = subtotal - discount

        gst = taxable_amount * 0.18

        grand_total = taxable_amount + gst

        # Save values for Generate Bill
        self.current_subtotal = subtotal
        self.current_discount = discount
        self.current_gst = gst
        self.current_total = grand_total

        self.subtotal_var.set(f"₹{subtotal:.2f}")
        self.discount_var.set(f"₹{discount:.2f}")
        self.gst_var.set(f"₹{gst:.2f}")
        self.total_var.set(f"₹{grand_total:.2f}")


    # ==========================================================
    # KEYBOARD POS CONTROLS
    # ==========================================================

    def _billing_page_active(self):
        """
        Return True only when the Billing page is currently visible.
        """

        try:
            return bool(self.winfo_ismapped())
        except Exception:
            return False

        
    def _keyboard_add_product(self, event=None):
        """Add the currently selected product."""

        self.add_item_to_cart()

        return "break"

    def _keyboard_increase(self, event=None):
        """
        + → Increase selected cart item.
        """

        try:
            widget = self.focus_get()
        except Exception:
            return "break"

        if widget is not self.cart_table:
            return "break"

        self.increase_quantity()

        return "break"

    def _keyboard_decrease(self, event=None):
        """
        - → Decrease selected cart item.
        """

        try:
            widget = self.focus_get()
        except Exception:
            return "break"

        if widget is not self.cart_table:
            return "break"

        self.decrease_quantity()

        return "break"

    def _keyboard_delete(self, event=None):
        """
        Delete → Remove selected cart item.
        """

        try:
            widget = self.focus_get()
        except Exception:
            return "break"

        if widget is not self.cart_table:
            return "break"

        self.remove_selected_item()

        return "break"

    def _keyboard_generate_bill(self, event=None):
        """
        Ctrl+B → Generate bill.
        """

        self.generate_bill()

        return "break"


    def _keyboard_escape(self, event=None):
        """
        Escape → Move focus back to the Billing page.
        """

        self.focus_set()

        return "break"

    def _keyboard_focus_product(self, event=None):
        """F2 → Focus product selector."""

        if not self._billing_page_active():
            return "break"

        self.product_combo.focus_set()

        return "break"

    def _keyboard_focus_quantity(self, event=None):

        if not self._billing_page_active():
            return "break"

        self.quantity_entry.focus_set()
        self.quantity_entry.select_range(0, "end")

        return "break"


    def _keyboard_focus_phone(self, event=None):

        if not self._billing_page_active():
            return "break"

        self.phone_entry.focus_set()
        self.phone_entry.select_range(0, "end")

        return "break"
    
    def _keyboard_focus_barcode(self, event=None):

        if not self._billing_page_active():
            return "break"

        self.barcode_entry.focus_set()
        self.barcode_entry.select_range(0, "end")

        return "break"

    
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

        # ---------------- Loyalty Points ----------------
        earned_points = add_loyalty_points(
            customer_id,
            grand_total
        )

        # Refresh loyalty label immediately
        self.fetch_customer_details()

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
            f"""Invoice Saved Successfully!

            ⭐ Loyalty Points Earned: {earned_points}

                Invoice:
                {invoice_path}"""
        )

        # ---------------- Reset Billing Screen ----------------
        self.cart.clear()
        self.refresh_cart()

        self.phone_var.set("")
        self.customer_name_var.set("")
        self.payment_method_var.set("Cash")
        self.quantity_var.set("1")
        self.discount_percent_var.set("0")
        self.points_var.set("⭐ Loyalty Points : 0")
        self.customer_id = None

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

        self.phone_entry.bind(
        "<KeyRelease>",
        self.fetch_customer_details
        )

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

        self.customer_entry.bind(
            "<KeyRelease>",
            lambda event: self.update_receipt_preview()
        )
        # Loyalty Points Display
        self.points_var = ctk.StringVar(value="⭐ Loyalty Points : 0")

        self.points_label = ctk.CTkLabel(
            customer_frame,
            textvariable=self.points_var,
            font=("Poppins", 13, "bold"),
            text_color="#F59E0B"
        )

        self.points_label.grid(
            row=3,
            column=1,
            sticky="w",
            padx=20,
            pady=(0,15)
        )

        # Payment Method
        ctk.CTkLabel(customer_frame, text="Payment Method").grid(
            row=1, column=2, sticky="w", padx=20)

        self.payment_combo = ctk.CTkComboBox(
            customer_frame,
            values=["Cash", "UPI", "Card"],
            variable=self.payment_method_var,
            height=38,
            command=lambda value: self.update_receipt_preview()
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

        product_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        # Column layout
        product_frame.grid_columnconfigure(0, weight=1)
        product_frame.grid_columnconfigure(1, weight=2)
        product_frame.grid_columnconfigure(2, weight=0)

        # Section title
        ctk.CTkLabel(
            product_frame,
            text="Add Products",
            font=("Poppins", 18, "bold"),
            text_color="#065F46"
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            padx=20,
            pady=(15, 15)
        )

        # Variables
        self.product_var = ctk.StringVar()
        self.quantity_var = ctk.StringVar(value="1")

        # ======================================================
        # BARCODE
        # ======================================================

        ctk.CTkLabel(
            product_frame,
            text="🔎 Barcode Scanner",
            font=("Poppins", 13, "bold"),
            text_color="#065F46"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 5)
        )

        self.barcode_entry = ctk.CTkEntry(
            product_frame,
            textvariable=self.barcode_var,
            placeholder_text="Scan or enter barcode...",
            height=42,
            border_width=2,
            border_color="#16A34A",
            fg_color="#F0FDF4",
            font=("Poppins", 13)
        )

        self.barcode_entry.grid(
            row=1,
            column=1,
            padx=20,
            pady=(0, 2),
            sticky="ew"
        )

        self.barcode_entry.bind(
                "<Return>",
                self.scan_barcode
            )

        self.barcode_entry.bind(
                "<KP_Enter>",
                lambda event: self.scan_barcode(event)
            )
        self.barcode_status = ctk.CTkLabel(
            product_frame,
            text="🟢 READY",
            font=("Poppins", 10, "bold"),
            text_color="#15803D",
            fg_color="#DCFCE7",
            corner_radius=12,
            padx=10,
            pady=4
        )

        self.barcode_status.grid(
            row=1,
            column=2,
            padx=(0, 20),
            sticky="e"
        )

        # Barcode keyboard hint
        ctk.CTkLabel(
            product_frame,
            text="F3 → Focus Scanner   •   Enter → Scan",
            font=("Poppins", 9),
            text_color="#64748B"
        ).grid(
            row=2,
            column=1,
            sticky="w",
            padx=20,
            pady=(0, 8)
        )

        # ======================================================
        # PRODUCT LABEL + QUANTITY LABEL
        # ======================================================

        ctk.CTkLabel(
            product_frame,
            text="Product",
            font=("Poppins", 11, "bold")
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=(2, 5)
        )

        ctk.CTkLabel(
            product_frame,
            text="Quantity",
            font=("Poppins", 11, "bold")
        ).grid(
            row=3,
            column=1,
            sticky="w",
            padx=20,
            pady=(2, 5)
        )

        # ======================================================
        # PRODUCT DROPDOWN
        # ======================================================

        self.product_combo = ctk.CTkComboBox(
            product_frame,
            values=["Loading Products..."],
            variable=self.product_var,
            height=38
        )

        self.product_combo.grid(
            row=4,
            column=0,
            padx=20,
            pady=(0, 15),
            sticky="ew"
        )

        self.product_combo.bind(
            "<Return>",
            self._keyboard_add_product
        )

        self.product_combo.bind(
            "<KP_Enter>",
            self._keyboard_add_product
        )

        combo_entry = getattr(
            self.product_combo,
            "_entry",
            None
        )

        if combo_entry is not None:

            combo_entry.bind(
                "<Return>",
                self._keyboard_add_product
            )

            combo_entry.bind(
                "<KP_Enter>",
                self._keyboard_add_product
            )

        # ======================================================
        # QUANTITY
        # ======================================================

        self.quantity_entry = ctk.CTkEntry(
            product_frame,
            textvariable=self.quantity_var,
            height=38
        )

        self.quantity_entry.grid(
            row=4,
            column=1,
            padx=20,
            pady=(0, 15),
            sticky="ew"
        )

        self.quantity_entry.bind(
            "<Return>",
            self._keyboard_add_product
        )

        self.quantity_entry.bind(
            "<KP_Enter>",
            self._keyboard_add_product
        )

        # ======================================================
        # ADD BUTTON
        # ======================================================

        self.add_item_button = ctk.CTkButton(
            product_frame,
            text="+ Add Item",
            fg_color="#16A34A",
            hover_color="#15803D",
            height=40,
            command=self.add_item_to_cart
        )

        self.add_item_button.grid(
            row=4,
            column=2,
            padx=20,
            pady=(0, 15),
            sticky="ew"
        )
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
            text="🛒 Current Cart",
            font=("Poppins", 19, "bold"),
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

        self.cart_table.bind(
            "<Double-1>",
            lambda event: self.increase_quantity()
        )

        for col in columns:
            self.cart_table.heading(col, text=col)

        self.cart_table.column(
            "Product",
            width=260,
            anchor="w"
        )

        self.cart_table.column(
            "Price",
            width=120,
            anchor="e"
        )

        self.cart_table.column(
            "Quantity",
            width=90,
            anchor="center"
        )

        self.cart_table.column(
            "Subtotal",
            width=140,
            anchor="e"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.cart_table.yview
        )

        self.cart_table.configure(yscrollcommand=scrollbar.set)

        self.cart_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ---------- Cart Controls ----------
        button_panel = ctk.CTkFrame(
            cart_body,
            fg_color="#F8FAFC",
            corner_radius=16,
            border_width=1,
            border_color="#E5E7EB"
        )

        button_panel.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(0, 5),
            pady=5
        )

        ctk.CTkLabel(
            button_panel,
            text="Cart Controls",
            font=("Poppins", 13, "bold"),
            text_color="#065F46"
        ).pack(
            padx=15,
            pady=(15, 12)
        )

        # ---------------- Quantity Controls ----------------

        quantity_frame = ctk.CTkFrame(
            button_panel,
            fg_color="transparent"
        )

        quantity_frame.pack(
            padx=12,
            pady=(0, 15)
        )

        self.minus_button = ctk.CTkButton(
            quantity_frame,
            text="−",
            width=42,
            height=42,
            corner_radius=12,
            fg_color="#F59E0B",
            hover_color="#D97706",
            font=("Poppins", 18, "bold"),
            command=self.decrease_quantity
        )

        self.minus_button.grid(
            row=0,
            column=0,
            padx=(0, 5)
        )

        ctk.CTkLabel(
            quantity_frame,
            text="Qty",
            width=45,
            font=("Poppins", 12, "bold"),
            text_color="#475569"
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        self.plus_button = ctk.CTkButton(
            quantity_frame,
            text="+",
            width=42,
            height=42,
            corner_radius=12,
            fg_color="#16A34A",
            hover_color="#15803D",
            font=("Poppins", 18, "bold"),
            command=self.increase_quantity
        )

        self.plus_button.grid(
            row=0,
            column=2,
            padx=(5, 0)
        )

        # ---------------- Remove Button ----------------

        self.remove_button = ctk.CTkButton(
            button_panel,
            text="🗑 Remove Item",
            width=150,
            height=40,
            corner_radius=12,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            font=("Poppins", 12, "bold"),
            command=self.remove_selected_item
        )

        self.remove_button.pack(
            fill="x",
            padx=12,
            pady=(0, 15)
        )

        ctk.CTkLabel(
                button_panel,
                text="⌨ Keyboard\n"
                    "F2  Product\n"
                    "F4  Quantity\n"
                    "F5  Phone\n"
                    "Enter  Add Product\n"
                    "+ / -  Change Qty\n"
                    "Delete  Remove\n"
                    "Ctrl+B  Generate Bill",
                font=("Poppins", 10),
                text_color="#64748B",
                justify="left"
            ).pack(
                padx=12,
                pady=(0, 15)
            )
        # ==========================================================
        # LIVE RECEIPT PREVIEW
        # ==========================================================

        receipt_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=18,
            border_width=1,
            border_color="#D1D5DB"
        )

        receipt_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        # Header
        receipt_header = ctk.CTkFrame(
            receipt_frame,
            fg_color="#ECFDF5",
            corner_radius=14
        )

        receipt_header.pack(
            fill="x",
            padx=12,
            pady=12
        )

        ctk.CTkLabel(
            receipt_header,
            text="🧾 Receipt Preview",
            font=("Poppins", 19, "bold"),
            text_color="#065F46"
        ).pack(
            side="left",
            padx=15,
            pady=12
        )

        ctk.CTkLabel(
            receipt_header,
            text="LIVE",
            font=("Poppins", 10, "bold"),
            text_color="#15803D",
            fg_color="#DCFCE7",
            corner_radius=12,
            padx=10,
            pady=4
        ).pack(
            side="right",
            padx=15
        )

        # Receipt body
        receipt_body = ctk.CTkFrame(
            receipt_frame,
            fg_color="#FAFAFA",
            corner_radius=12
        )

        receipt_body.pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )

        # Shop Name
        ctk.CTkLabel(
            receipt_body,
            text="SHINGVI SUPERMART",
            font=("Poppins", 20, "bold"),
            text_color="#065F46"
        ).pack(pady=(15, 2))

        ctk.CTkLabel(
            receipt_body,
            text="Inventory Management System",
            font=("Poppins", 11),
            text_color="#64748B"
        ).pack()

        # Customer / Payment information
        info_frame = ctk.CTkFrame(
            receipt_body,
            fg_color="transparent"
        )

        info_frame.pack(
            fill="x",
            padx=20,
            pady=(15, 8)
        )

        self.receipt_customer_var = ctk.StringVar(
            value="Customer: Walk-in Customer"
        )

        self.receipt_payment_var = ctk.StringVar(
            value="Payment: Cash"
        )

        self.receipt_phone_var = ctk.StringVar(
            value="Phone: --"
        )

        ctk.CTkLabel(
            info_frame,
            textvariable=self.receipt_customer_var,
            font=("Poppins", 11, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            info_frame,
            textvariable=self.receipt_payment_var,
            font=("Poppins", 11, "bold")
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        ctk.CTkLabel(
            info_frame,
            textvariable=self.receipt_phone_var,
            font=("Poppins", 10),
            text_color="#64748B"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(4, 0)
        )

        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)

        # Separator
        ctk.CTkFrame(
            receipt_body,
            height=1,
            fg_color="#D1D5DB"
        ).pack(
            fill="x",
            padx=20,
            pady=8
        )

        # Product area
        self.receipt_items_frame = ctk.CTkFrame(
            receipt_body,
            fg_color="transparent"
        )

        self.receipt_items_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Totals
        receipt_totals = ctk.CTkFrame(
            receipt_body,
            fg_color="transparent"
        )

        receipt_totals.pack(
            fill="x",
            padx=20,
            pady=(10, 15)
        )

        self.receipt_subtotal_var = ctk.StringVar(value="₹0.00")
        self.receipt_discount_var = ctk.StringVar(value="₹0.00")
        self.receipt_gst_var = ctk.StringVar(value="₹0.00")
        self.receipt_total_var = ctk.StringVar(value="₹0.00")


        def receipt_total_row(label, variable, bold=False):

            row = ctk.CTkFrame(
                receipt_totals,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                pady=2
            )

            font_style = (
                ("Poppins", 13, "bold")
                if bold
                else
                ("Poppins", 11)
            )

            ctk.CTkLabel(
                row,
                text=label,
                font=font_style
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                textvariable=variable,
                font=font_style,
                text_color="#065F46" if bold else "#374151"
            ).pack(side="right")


        receipt_total_row(
            "Subtotal",
            self.receipt_subtotal_var
        )

        receipt_total_row(
            "Discount",
            self.receipt_discount_var
        )

        receipt_total_row(
            "GST (18%)",
            self.receipt_gst_var
        )

        ctk.CTkFrame(
            receipt_totals,
            height=1,
            fg_color="#D1D5DB"
        ).pack(
            fill="x",
            pady=6
        )

        receipt_total_row(
            "GRAND TOTAL",
            self.receipt_total_var,
            bold=True
        )

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

