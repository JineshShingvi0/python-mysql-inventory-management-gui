import customtkinter as ctk
from tkinter import ttk, messagebox
from backend import (
    get_all_products,
    add_product,
    update_product,
    delete_product,
    get_product_by_id,
    search_products
)


class ProductsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#F9FAFB")

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

        # ---------------- Toolbar ----------------
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=30, pady=15)

        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search product by name or category...",
            width=300,
            height=38
        )       

        self.search_entry.pack(side="left")

        # Search while typing
        self.search_entry.bind(
            "<KeyRelease>",
            self.search_products_event
            )
        self.refresh_button = ctk.CTkButton(
            toolbar,
            text="Refresh",
            width=100,
            command=self.load_products
        )
        self.refresh_button.pack(side="left", padx=10)

        right_buttons = ctk.CTkFrame(toolbar, fg_color="transparent")
        right_buttons.pack(side="right")

        # Delete Button
        self.delete_button = ctk.CTkButton(
            right_buttons,
            text="🗑 Delete",
            width=110,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.open_delete_product_popup
            )
        self.delete_button.pack(side="left", padx=5)
        self.update_button = ctk.CTkButton(
            right_buttons,
            text="✏ Update",
            width=120,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.open_update_product_popup
        )
        self.update_button.pack(side="left", padx=5)

        self.add_button = ctk.CTkButton(
            right_buttons,
            text="+ Add Product",
            width=140,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.open_add_product_popup
        )
        self.add_button.pack(side="left", padx=5)

        # ---------------- Table ----------------
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        columns = ("ID", "Name", "Category", "Price", "Stock")

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            self.table.heading(col, text=col)

        self.table.column("ID", width=70, anchor="center")
        self.table.column("Name", width=260)
        self.table.column("Category", width=180)
        self.table.column("Price", width=120, anchor="center")
        self.table.column("Stock", width=100, anchor="center")

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
    # LOAD PRODUCTS
    # ==========================================================
    def load_products(self):

        for row in self.table.get_children():
            self.table.delete(row)

        products = get_all_products()

        self.count_label.configure(
            text=f"{len(products)} Products Available"
        )

        for product in products:
            self.table.insert("", "end", values=product)

    # ==========================================================
    # ADD PRODUCT POPUP
    # ==========================================================
    def open_add_product_popup(self):

        popup = ctk.CTkToplevel(self)
        popup.title("Add Product")
        popup.geometry("500x640")
        popup.resizable(False, False)
        popup.grab_set()
        popup.configure(fg_color="white")

        ctk.CTkLabel(
            popup,
            text="Add Product",
            font=("Poppins", 24, "bold"),
            text_color="#16A34A"
        ).pack(pady=20)

        name_var = ctk.StringVar()
        category_var = ctk.StringVar(value="Oil")
        purchase_var = ctk.StringVar()
        selling_var = ctk.StringVar()
        stock_var = ctk.StringVar()
        minimum_var = ctk.StringVar()

        def field(label, variable):
            ctk.CTkLabel(
                popup,
                text=label,
                font=("Poppins", 13, "bold")
            ).pack(anchor="w", padx=35, pady=(8, 2))

            entry = ctk.CTkEntry(
                popup,
                textvariable=variable,
                width=430,
                height=38
            )
            entry.pack(padx=35)

        field("Product Name", name_var)

        ctk.CTkLabel(
            popup,
            text="Category",
            font=("Poppins", 13, "bold")
        ).pack(anchor="w", padx=35, pady=(8, 2))

        combo = ctk.CTkComboBox(
            popup,
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
            height=38
        )
        combo.pack(padx=35)

        field("Purchase Price", purchase_var)
        field("Selling Price", selling_var)
        field("Stock Quantity", stock_var)
        field("Minimum Stock", minimum_var)

        status = ctk.CTkLabel(popup, text="")
        status.pack(pady=8)

        def save_product():

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

            try:
                purchase_price = float(purchase_var.get())
                selling_price = float(selling_var.get())
                stock = int(stock_var.get())
                minimum_stock = int(minimum_var.get())

            except ValueError:
                status.configure(
                    text="Invalid numbers.",
                    text_color="red"
                )
                return

            if purchase_price <= 0 or selling_price <= 0:
                status.configure(
                    text="Prices must be greater than 0.",
                    text_color="red"
                )
                return

            if stock < 0 or minimum_stock < 0:
                status.configure(
                    text="Stock values cannot be negative.",
                    text_color="red"
                )
                return

            add_product(
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
                "Success",
                "Product added successfully!"
            )

        ctk.CTkButton(
            popup,
            text="Save Product",
            width=430,
            height=45,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=save_product
        ).pack(pady=15)

    # ==========================================================
    # UPDATE PRODUCT POPUP
    # ==========================================================
    def open_update_product_popup(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Product Selected",
                "Please select a product first."
            )
            return

        values = self.table.item(selected[0], "values")

        product_id = int(values[0])

        product = get_product_by_id(product_id)

        popup = ctk.CTkToplevel(self)
        popup.title("Update Product")
        popup.geometry("500x640")
        popup.resizable(False, False)
        popup.grab_set()
        popup.configure(fg_color="white")

        ctk.CTkLabel(
            popup,
            text="Update Product",
            font=("Poppins", 24, "bold"),
            text_color="#2563EB"
        ).pack(pady=20)

        name_var = ctk.StringVar(value=product[1])
        category_var = ctk.StringVar(value=product[2].title())
        purchase_var = ctk.StringVar(value=str(product[3]))
        selling_var = ctk.StringVar(value=str(product[4]))
        stock_var = ctk.StringVar(value=str(product[5]))
        minimum_var = ctk.StringVar(value=str(product[6]))

        def field(label, variable):
            ctk.CTkLabel(
                popup,
                text=label,
                font=("Poppins", 13, "bold")
            ).pack(anchor="w", padx=35, pady=(8, 2))

            entry = ctk.CTkEntry(
                popup,
                textvariable=variable,
                width=430,
                height=38
            )
            entry.pack(padx=35)

        field("Product Name", name_var)

        ctk.CTkLabel(
            popup,
            text="Category",
            font=("Poppins", 13, "bold")
        ).pack(anchor="w", padx=35, pady=(8, 2))

        combo = ctk.CTkComboBox(
            popup,
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
            height=38
        )
        combo.pack(padx=35)

        combo.set(product[2].title())

        field("Purchase Price", purchase_var)
        field("Selling Price", selling_var)
        field("Stock Quantity", stock_var)
        field("Minimum Stock", minimum_var)

        status = ctk.CTkLabel(popup, text="")
        status.pack(pady=8)

        def update_selected_product():

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

            try:
                purchase_price = float(purchase_var.get())
                selling_price = float(selling_var.get())
                stock = int(stock_var.get())
                minimum_stock = int(minimum_var.get())

            except ValueError:
                status.configure(
                    text="Invalid numbers.",
                    text_color="red"
                )
                return

            if purchase_price <= 0 or selling_price <= 0:
                status.configure(
                    text="Prices must be greater than 0.",
                    text_color="red"
                )
                return

            if stock < 0 or minimum_stock < 0:
                status.configure(
                    text="Stock values cannot be negative.",
                    text_color="red"
                )
                return

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
                "Success",
                "Product updated successfully!"
            )

        ctk.CTkButton(
            popup,
            text="Update Product",
            width=430,
            height=45,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=update_selected_product
        ).pack(pady=15)

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

        # Empty search -> show everything
        if keyword == "":
            self.load_products()
            return

        products = search_products(keyword)

        # Clear table
        for row in self.table.get_children():
            self.table.delete(row)

        # Update product count
        self.count_label.configure(
            text=f"{len(products)} Products Found"
        )

        # Insert filtered products
        for product in products:
            self.table.insert(
                "",
                "end",
                values=product
            )