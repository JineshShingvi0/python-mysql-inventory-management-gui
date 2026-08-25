import customtkinter as ctk
from tkinter import ttk, messagebox
from backend import (
    get_all_products,
    add_product,
    add_product_with_barcode,
    update_product,
    add_stock,
    delete_product,
    get_product_by_id,
    search_products,
    get_products_with_barcodes,
    update_product_barcode,
    generate_product_barcode
)


class ProductsPage(ctk.CTkScrollableFrame):

    def __init__(self, parent):
        super().__init__(
            parent, 
            fg_color="#F9FAFB",
            corner_radius=0
            )

        self.build_ui()
        self.load_products()

    # ==========================================================
    # BUILD PRODUCTS PAGE
    # ==========================================================
    def build_ui(self):

        # ---------------- Title ----------------
        ctk.CTkLabel(
            self,
            text="Products",
            font=("Poppins", 28, "bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=30, pady=(20, 5))

        self.count_label = ctk.CTkLabel(
            self,
            text="0 Products Available",
            font=("Poppins", 13),
            text_color="gray40"
        )
        self.count_label.pack(anchor="w", padx=30)

        # ==========================================================
        # PRODUCTS TOOLBAR
        # ==========================================================

        toolbar = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        toolbar.pack(
            fill="x",
            padx=30,
            pady=(12, 8)
        )

        # ----------------------------------------------------------
        # Toolbar layout
        # ----------------------------------------------------------

        toolbar.grid_columnconfigure(0, weight=1)
        toolbar.grid_columnconfigure(1, weight=0)

        # ==========================================================
        # TOP ROW
        # ==========================================================

        top_row = ctk.CTkFrame(
            toolbar,
            fg_color="transparent"
        )

        top_row.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        top_row.grid_columnconfigure(0, weight=1)
        top_row.grid_columnconfigure(1, weight=0)

        # ----------------------------------------------------------
        # Search
        # ----------------------------------------------------------

        self.search_entry = ctk.CTkEntry(
            top_row,
            placeholder_text="Search product by name or category...",
            height=38
        )

        self.search_entry.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_products_event
        )

        # ----------------------------------------------------------
        # Refresh
        # ----------------------------------------------------------

        self.refresh_button = ctk.CTkButton(
            top_row,
            text="Refresh",
            width=100,
            height=38,
            command=self.load_products
        )

        self.refresh_button.grid(
            row=0,
            column=1,
            padx=(10, 10)
        )

        # ----------------------------------------------------------
        # Generate Barcode
        # ----------------------------------------------------------

        self.generate_barcode_button = ctk.CTkButton(
            top_row,
            text="🏷 Generate Barcode",
            width=155,
            height=38,
            fg_color="#7C3AED",
            hover_color="#6D28D9",
            font=("Poppins", 12, "bold"),
            command=self.generate_selected_barcode
        )

        self.generate_barcode_button.grid(
            row=0,
            column=2
        )

        # ==========================================================
        # ACTION ROW
        # ==========================================================

        action_row = ctk.CTkFrame(
            toolbar,
            fg_color="transparent"
        )

        action_row.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="e",
            pady=(8, 0)
        )

        # ----------------------------------------------------------
        # Delete
        # ----------------------------------------------------------

        self.delete_button = ctk.CTkButton(
            action_row,
            text="🗑 Delete",
            width=110,
            height=38,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.open_delete_product_popup
        )

        self.delete_button.grid(
            row=0,
            column=0,
            padx=5
        )

        # ----------------------------------------------------------
        # Update
        # ----------------------------------------------------------

        self.update_button = ctk.CTkButton(
            action_row,
            text="✏ Update",
            width=120,
            height=38,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.open_update_product_popup
        )

        self.update_button.grid(
            row=0,
            column=1,
            padx=5
        )

        # ----------------------------------------------------------
        # Add Stock
        # ----------------------------------------------------------

        self.stock_button = ctk.CTkButton(
            action_row,
            text="📦 Add Stock",
            width=130,
            height=38,
            fg_color="#EA580C",
            hover_color="#C2410C",
            command=self.open_add_stock_popup
        )

        self.stock_button.grid(
            row=0,
            column=2,
            padx=5
        )

        # ----------------------------------------------------------
        # Add Product
        # ----------------------------------------------------------

        self.add_button = ctk.CTkButton(
            action_row,
            text="+ Add Product",
            width=140,
            height=38,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.open_add_product_popup
        )

        self.add_button.grid(
            row=0,
            column=3,
            padx=(5, 0)
        )
        # ---------------- Table ----------------
        table_frame = ctk.CTkFrame(
            self,
            height=460,
            corner_radius=0
        )

        table_frame.pack(
            fill="x",
            padx=30,
            pady=(8, 20)
        )

        table_frame.pack_propagate(False)

        columns = (
                "ID",
                "Name",
                "Category",
                "Price",
                "Stock",
                "Barcode"
            )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            self.table.heading(col, text=col)

        self.table.column("ID", width=70, anchor="center")
        self.table.column("Name", width=240)
        self.table.column("Category", width=150)
        self.table.column("Price", width=110, anchor="e")
        self.table.column("Stock", width=90, anchor="center")
        self.table.column("Barcode", width=170, anchor="center")

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            rowheight=34,
            font=("Poppins", 11),
            background="white",
            fieldbackground="white"
        )

        style.configure(
            "Treeview.Heading",
            font=("Poppins", 12, "bold"),
            background="#065F46",
            foreground="white"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ==========================================================
        # TABLE MOUSE-WHEEL SCROLL
        # ==========================================================

        self.table.bind(
            "<MouseWheel>",
            lambda event: self.table.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        )

        self.table.bind(
            "<Button-4>",
            lambda event: self.table.yview_scroll(
                -1,
                "units"
            )
        )

        self.table.bind(
            "<Button-5>",
            lambda event: self.table.yview_scroll(
                1,
                "units"
            )
        )

    # ==========================================================
    # LOAD PRODUCTS
    # ==========================================================
    def load_products(self):

        # Clear old rows
        for row in self.table.get_children():
            self.table.delete(row)

        products = get_products_with_barcodes()

        # Update count
        self.count_label.configure(
            text=f"{len(products)} Products Available"
        )

        # Insert products
        for product_id, name, category, selling_price, stock, barcode in products:

            self.table.insert(
                "",
                "end",
                values=(
                    product_id,
                    name.title(),
                    category.title() if category else "",
                    f"₹{float(selling_price):,.2f}",
                    stock,
                    barcode or "—"
                )
            )
    # ==========================================================
    # ADD PRODUCT POPUP
    # ==========================================================
    def open_add_product_popup(self):

        # ======================================================
        # CREATE POPUP
        # ======================================================

        popup = ctk.CTkToplevel(self)

        popup.title("Add Product")
        popup.geometry("520x680")
        popup.minsize(520, 680)
        popup.maxsize(520, 680)
        popup.resizable(False, False)

        popup.grab_set()
        popup.configure(
            fg_color="white"
        )

        # ======================================================
        # TITLE
        # ======================================================

        ctk.CTkLabel(
            popup,
            text="Add Product",
            font=("Poppins", 24, "bold"),
            text_color="#16A34A"
        ).pack(
            pady=(15, 10)
        )

        # ======================================================
        # SCROLLABLE FORM
        # ======================================================

        form_frame = ctk.CTkScrollableFrame(
            popup,
            fg_color="transparent"
        )

        form_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 5)
        )

        # ======================================================
        # VARIABLES
        # ======================================================

        name_var = ctk.StringVar()
        category_var = ctk.StringVar(
            value="Oil"
        )
        purchase_var = ctk.StringVar()
        selling_var = ctk.StringVar()
        stock_var = ctk.StringVar()
        minimum_var = ctk.StringVar()
        barcode_var = ctk.StringVar()

        # ======================================================
        # FIELD HELPER
        # ======================================================

        def field(label, variable):

            ctk.CTkLabel(
                form_frame,
                text=label,
                font=("Poppins", 13, "bold")
            ).pack(
                anchor="w",
                padx=20,
                pady=(6, 2)
            )

            entry = ctk.CTkEntry(
                form_frame,
                textvariable=variable,
                width=430,
                height=36
            )

            entry.pack(
                padx=20
            )

            return entry

        # ======================================================
        # PRODUCT NAME
        # ======================================================

        field(
            "Product Name",
            name_var
        )

        # ======================================================
        # CATEGORY
        # ======================================================

        ctk.CTkLabel(
            form_frame,
            text="Category",
            font=("Poppins", 13, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(6, 2)
        )

        combo = ctk.CTkComboBox(
            form_frame,
            values=[
                "Oil",
                "Grocery",
                "Snacks",
                "Beverages",
                "Household",
                "Personal Care",
                "Clothing"
            ],
            variable=category_var,
            width=430,
            height=36
        )

        combo.pack(
            padx=20
        )

        # ======================================================
        # OTHER FIELDS
        # ======================================================

        field(
            "Purchase Price",
            purchase_var
        )

        field(
            "Selling Price",
            selling_var
        )

        field(
            "Stock Quantity",
            stock_var
        )

        field(
            "Minimum Stock",
            minimum_var
        )

        field(
            "Barcode",
            barcode_var
        )

        ctk.CTkLabel(
            form_frame,
            text="Leave barcode empty if the product has no barcode.",
            font=("Poppins", 10),
            text_color="#64748B"
        ).pack(
            anchor="w",
            padx=20,
            pady=(3, 12)
        )

        # ======================================================
        # FIXED BOTTOM AREA
        # ======================================================

        bottom_frame = ctk.CTkFrame(
            popup,
            fg_color="white"
        )

        bottom_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        status = ctk.CTkLabel(
            bottom_frame,
            text="",
            font=("Poppins", 11)
        )

        status.pack(
            pady=(0, 5)
        )

        # ======================================================
        # SAVE PRODUCT
        # ======================================================

        def save_product():

            # --------------------------------------------------
            # VALIDATION
            # --------------------------------------------------

            if (
                not name_var.get().strip()
                or not purchase_var.get().strip()
                or not selling_var.get().strip()
                or not stock_var.get().strip()
                or not minimum_var.get().strip()
            ):

                status.configure(
                    text="Please fill all fields.",
                    text_color="red"
                )

                return

            # --------------------------------------------------
            # NUMBER VALIDATION
            # --------------------------------------------------

            try:

                purchase_price = float(
                    purchase_var.get().strip()
                )

                selling_price = float(
                    selling_var.get().strip()
                )

                stock = int(
                    stock_var.get().strip()
                )

                minimum_stock = int(
                    minimum_var.get().strip()
                )

            except ValueError:

                status.configure(
                    text="Invalid numbers.",
                    text_color="red"
                )

                return

            # --------------------------------------------------
            # VALUE VALIDATION
            # --------------------------------------------------

            if purchase_price <= 0:

                status.configure(
                    text="Purchase price must be greater than 0.",
                    text_color="red"
                )

                return

            if selling_price <= 0:

                status.configure(
                    text="Selling price must be greater than 0.",
                    text_color="red"
                )

                return

            if stock < 0:

                status.configure(
                    text="Stock cannot be negative.",
                    text_color="red"
                )

                return

            if minimum_stock < 0:

                status.configure(
                    text="Minimum stock cannot be negative.",
                    text_color="red"
                )

                return

            # --------------------------------------------------
            # BARCODE
            # --------------------------------------------------

            barcode = barcode_var.get().strip()

            # --------------------------------------------------
            # SAVE PRODUCT WITH BARCODE
            # --------------------------------------------------

            success, result = add_product_with_barcode(
                name_var.get().strip().lower(),
                category_var.get().strip().lower(),
                purchase_price,
                selling_price,
                stock,
                minimum_stock,
                barcode
            )

            # --------------------------------------------------
            # ERROR
            # --------------------------------------------------

            if not success:

                status.configure(
                    text=str(result),
                    text_color="red"
                )

                return

            # --------------------------------------------------
            # SUCCESS
            # --------------------------------------------------

            popup.destroy()

            self.load_products()

            messagebox.showinfo(
                "Success",
                "Product added successfully!"
            )

        # ======================================================
        # FIXED SAVE BUTTON
        # ======================================================

        ctk.CTkButton(
            bottom_frame,
            text="💾 Save Product",
            width=430,
            height=42,
            fg_color="#16A34A",
            hover_color="#15803D",
            font=("Poppins", 14, "bold"),
            command=save_product
        ).pack(
            pady=(0, 2)
        )

    # ==========================================================
    # GENERATE BARCODE FOR SELECTED PRODUCT
    # ==========================================================

    def generate_selected_barcode(self):

        selected = self.table.selection()

        # ------------------------------------------------------
        # No product selected
        # ------------------------------------------------------

        if not selected:

            messagebox.showwarning(
                "No Product Selected",
                "Please select a product first."
            )

            return

        # ------------------------------------------------------
        # Get selected product
        # ------------------------------------------------------

        values = self.table.item(
            selected[0],
            "values"
        )

        product_id = int(values[0])

        product_name = str(
            values[1]
        )

        current_barcode = str(
            values[5]
        ).strip()

        # ------------------------------------------------------
        # Prevent overwriting existing barcode
        # ------------------------------------------------------

        if current_barcode and current_barcode != "—":

            messagebox.showinfo(
                "Barcode Already Exists",
                f"{product_name.title()} already has a barcode:\n\n"
                f"{current_barcode}\n\n"
                "Use Update Product if you want to replace it."
            )

            return

        # ------------------------------------------------------
        # Confirmation
        # ------------------------------------------------------

        confirm = messagebox.askyesno(
            "Generate Barcode",
            f"Generate a new internal barcode for:\n\n"
            f"{product_name.title()}?"
        )

        if not confirm:
            return

        # ------------------------------------------------------
        # Generate barcode
        # ------------------------------------------------------

        success, result = generate_product_barcode(
            product_id
        )

        if not success:

            messagebox.showerror(
                "Barcode Generation Failed",
                str(result)
            )

            return

        # ------------------------------------------------------
        # Refresh table
        # ------------------------------------------------------

        self.load_products()

        messagebox.showinfo(
            "Barcode Generated",
            f"Barcode generated successfully!\n\n"
            f"Product: {product_name.title()}\n"
            f"Barcode: {result}"
        )


    # ==========================================================
    # UPDATE PRODUCT POPUP
    # ==========================================================
    def open_update_product_popup(self):

        # ======================================================
        # CHECK PRODUCT SELECTION
        # ======================================================

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Product Selected",
                "Please select a product first."
            )
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        product_id = int(values[0])

        # ======================================================
        # FETCH PRODUCT
        # ======================================================

        product = get_product_by_id(product_id)

        if not product:
            messagebox.showerror(
                "Product Not Found",
                "Unable to load the selected product."
            )
            return

        # ======================================================
        # CREATE POPUP
        # ======================================================

        popup = ctk.CTkToplevel(self)

        popup.title("Update Product")
        popup.geometry("520x680")
        popup.minsize(520, 680)
        popup.maxsize(520, 680)
        popup.resizable(False, False)

        popup.grab_set()
        popup.configure(
            fg_color="white"
        )

        # ======================================================
        # TITLE
        # ======================================================

        ctk.CTkLabel(
            popup,
            text="Update Product",
            font=("Poppins", 24, "bold"),
            text_color="#2563EB"
        ).pack(
            pady=(15, 10)
        )

        # ======================================================
        # SCROLLABLE FORM AREA
        # ======================================================

        form_frame = ctk.CTkScrollableFrame(
            popup,
            fg_color="transparent"
        )

        form_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 5)
        )

        # ======================================================
        # VARIABLES
        # ======================================================

        # get_product_by_id() returns:
        # 0 = product_id
        # 1 = barcode
        # 2 = name
        # 3 = category
        # 4 = purchase_price
        # 5 = selling_price
        # 6 = stock
        # 7 = minimum_stock

        name_var = ctk.StringVar(
            value=str(product[2])
        )

        category_var = ctk.StringVar(
            value=str(product[3]).title()
        )

        purchase_var = ctk.StringVar(
            value=str(product[4])
        )

        selling_var = ctk.StringVar(
            value=str(product[5])
        )

        stock_var = ctk.StringVar(
            value=str(product[6])
        )

        minimum_var = ctk.StringVar(
            value=str(product[7])
        )

        barcode_var = ctk.StringVar(
            value=str(product[1] or "")
        )

        # ======================================================
        # FIELD HELPER
        # ======================================================

        def create_field(label_text, variable):

            ctk.CTkLabel(
                form_frame,
                text=label_text,
                font=("Poppins", 13, "bold")
            ).pack(
                anchor="w",
                padx=20,
                pady=(6, 2)
            )

            entry = ctk.CTkEntry(
                form_frame,
                textvariable=variable,
                width=430,
                height=36
            )

            entry.pack(
                padx=20
            )

            return entry

        # ======================================================
        # PRODUCT NAME
        # ======================================================

        create_field(
            "Product Name",
            name_var
        )

        # ======================================================
        # CATEGORY
        # ======================================================

        ctk.CTkLabel(
            form_frame,
            text="Category",
            font=("Poppins", 13, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(6, 2)
        )

        category_combo = ctk.CTkComboBox(
            form_frame,
            values=[
                "Oil",
                "Grocery",
                "Snacks",
                "Beverages",
                "Household",
                "Personal Care",
                "Clothing"
            ],
            variable=category_var,
            width=430,
            height=36
        )

        category_combo.pack(
            padx=20
        )

        # ======================================================
        # OTHER FIELDS
        # ======================================================

        create_field(
            "Purchase Price",
            purchase_var
        )

        create_field(
            "Selling Price",
            selling_var
        )

        create_field(
            "Stock Quantity",
            stock_var
        )

        create_field(
            "Minimum Stock",
            minimum_var
        )

        create_field(
            "Barcode",
            barcode_var
        )

        ctk.CTkLabel(
            form_frame,
            text="Leave barcode empty to remove it.",
            font=("Poppins", 10),
            text_color="#64748B"
        ).pack(
            anchor="w",
            padx=20,
            pady=(3, 12)
        )

        # ======================================================
        # FIXED BOTTOM AREA
        # ======================================================

        bottom_frame = ctk.CTkFrame(
            popup,
            fg_color="white"
        )

        bottom_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        status_label = ctk.CTkLabel(
            bottom_frame,
            text="",
            font=("Poppins", 11)
        )

        status_label.pack(
            pady=(0, 5)
        )

        # ======================================================
        # UPDATE PRODUCT
        # ======================================================

        def update_selected_product():

            # ---------------- Validation ----------------

            if (
                not name_var.get().strip()
                or not purchase_var.get().strip()
                or not selling_var.get().strip()
                or not stock_var.get().strip()
                or not minimum_var.get().strip()
            ):
                status_label.configure(
                    text="Please fill all required fields.",
                    text_color="red"
                )
                return

            try:

                purchase_price = float(
                    purchase_var.get()
                )

                selling_price = float(
                    selling_var.get()
                )

                stock = int(
                    stock_var.get()
                )

                minimum_stock = int(
                    minimum_var.get()
                )

            except ValueError:

                status_label.configure(
                    text="Enter valid numbers.",
                    text_color="red"
                )
                return

            if purchase_price <= 0:

                status_label.configure(
                    text="Purchase price must be greater than 0.",
                    text_color="red"
                )
                return

            if selling_price <= 0:

                status_label.configure(
                    text="Selling price must be greater than 0.",
                    text_color="red"
                )
                return

            if stock < 0 or minimum_stock < 0:

                status_label.configure(
                    text="Stock values cannot be negative.",
                    text_color="red"
                )
                return

            # ---------------- Barcode ----------------

            barcode = barcode_var.get().strip()

            barcode_updated = update_product_barcode(
                product_id,
                barcode
            )

            if not barcode_updated:

                status_label.configure(
                    text="Barcode already belongs to another product.",
                    text_color="red"
                )

                return

            # ---------------- Update Product ----------------

            update_product(
                product_id,
                name_var.get().strip().lower(),
                category_var.get().strip().lower(),
                purchase_price,
                selling_price,
                stock,
                minimum_stock
            )

            popup.destroy()

            self.load_products()

            messagebox.showinfo(
                "Updated",
                "Product updated successfully!"
            )

        # ======================================================
        # FIXED UPDATE BUTTON
        # ======================================================

        ctk.CTkButton(
            bottom_frame,
            text="💾 Update Product",
            width=430,
            height=42,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=("Poppins", 14, "bold"),
            command=update_selected_product
        ).pack(
            pady=(0, 2)
        )
    # ==========================================================
    # ADD STOCK POPUP (DAY 9)
    # ==========================================================

    def open_add_stock_popup(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Product Selected",
                "Please select a product first."
            )
            return

        values = self.table.item(selected[0], "values")

        product_id = int(values[0])
        product_name = values[1]
        current_stock = int(values[4])

        popup = ctk.CTkToplevel(self)
        popup.title("Add Stock")
        popup.geometry("420x330")
        popup.resizable(False, False)
        popup.grab_set()
        popup.configure(fg_color="white")

        ctk.CTkLabel(
            popup,
            text="📦 Add Stock",
            font=("Poppins", 22, "bold"),
            text_color="#EA580C"
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            popup,
            text=f"Product: {product_name.title()}",
            font=("Poppins", 14, "bold")
        ).pack()

        ctk.CTkLabel(
            popup,
            text=f"Current Stock: {current_stock}",
            font=("Poppins", 13),
            text_color="gray40"
        ).pack(pady=(0, 15))

        quantity_var = ctk.StringVar()

        ctk.CTkLabel(
            popup,
            text="Quantity to Add",
            font=("Poppins", 13, "bold")
        ).pack(anchor="w", padx=30)

        quantity_entry = ctk.CTkEntry(
            popup,
            textvariable=quantity_var,
            width=340,
            height=40
        )
        quantity_entry.pack(padx=30, pady=8)

        status = ctk.CTkLabel(popup, text="")
        status.pack()

        def save_stock():

            try:
                quantity_to_add = int(quantity_var.get())

                if quantity_to_add <= 0:
                    raise ValueError

            except ValueError:
                status.configure(
                    text="Enter a valid stock quantity.",
                    text_color="red"
                )
                return

            # Backend function
            add_stock(product_id, quantity_to_add)

            popup.destroy()

            self.load_products()

            messagebox.showinfo(
                "Stock Updated",
                f"{quantity_to_add} units added to {product_name.title()}."
            )

        ctk.CTkButton(
            popup,
            text="Add Stock",
            width=340,
            height=42,
            fg_color="#EA580C",
            hover_color="#C2410C",
            command=save_stock
        ).pack(pady=20)
        
    # ==========================================================
    # DELETE PRODUCT POPUP
    # ==========================================================

    def open_delete_product_popup(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Product Selected",
                "Please select a product to delete."
            )
            return

        values = self.table.item(selected[0], "values")

        product_id = int(values[0])
        product_name = values[1]

        answer = messagebox.askyesno(
            "Delete Product",
            f"Are you sure you want to delete\n\n'{product_name.title()}' ?"
        )

        if not answer:
            return

        deleted = delete_product(product_id)

        if deleted:
            self.load_products()

            messagebox.showinfo(
                "Deleted",
                f"{product_name.title()} deleted successfully!"
            )
        else:
            messagebox.showerror(
                "Error",
                "Unable to delete the selected product."
            )

    # ==========================================================
    # LIVE SEARCH PRODUCTS
    # ==========================================================

    def search_products_event(self, event=None):

        keyword = self.search_entry.get().strip().lower()

        # Empty search → show all products
        if keyword == "":
            self.load_products()
            return

        products = search_products(keyword)

        # Clear table
        for row in self.table.get_children():
            self.table.delete(row)

        self.count_label.configure(
            text=f"{len(products)} Products Found"
        )

        for product in products:

            product_id = product[0]
            name = product[1]
            category = product[2]
            selling_price = product[3]
            stock = product[4]

            # Get barcode from the full product record
            full_product = get_product_by_id(product_id)

            barcode = (
                full_product[1]
                if full_product
                else None
            )

            self.table.insert(
                "",
                "end",
                values=(
                    product_id,
                    name.title(),
                    category.title() if category else "",
                    f"₹{float(selling_price):,.2f}",
                    stock,
                    barcode or "—"
                )
            )