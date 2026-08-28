import customtkinter as ctk
import os
import barcode
import subprocess

from barcode.writer import ImageWriter
from PIL import Image
from tkinter import ttk, messagebox

from backend import (
    add_product_with_barcode,
    update_product,
    add_stock,
    get_all_suppliers,
    delete_product,
    get_product_by_id,
    search_products,
    get_products_with_barcodes,
    update_product_barcode,
    generate_product_barcode,
    get_low_stock_products_for_reorder
)

class ProductsPage(ctk.CTkScrollableFrame):

    PRODUCT_CATEGORIES = [
            "Oil",
            "Grocery",
            "Snacks",
            "Beverages",
            "Household",
            "Personal Care",
            "Clothing"
        ]
    
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    BARCODE_IMAGES_DIR = os.path.join(
        BASE_DIR,
        "barcode_images"
    )

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

        for column in range(1, 5):
            top_row.grid_columnconfigure(
                column,
                weight=0
            )

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
        # Copy Barcode
        # ----------------------------------------------------------

        self.copy_barcode_button = ctk.CTkButton(
            top_row,
            text="📋 Copy Barcode",
            width=135,
            height=38,
            fg_color="#0EA5E9",
            hover_color="#0284C7",
            font=("Poppins", 12, "bold"),
            command=self.copy_selected_barcode
        )

        self.copy_barcode_button.grid(
            row=0,
            column=2,
            padx=(0, 10)
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
            column=3
        )

        # ----------------------------------------------------------
        # Barcode Details
        # ----------------------------------------------------------

        self.barcode_details_button = ctk.CTkButton(
            top_row,
            text="🔎 Barcode Details",
            width=145,
            height=38,
            fg_color="#0F766E",
            hover_color="#115E59",
            font=("Poppins", 12, "bold"),
            command=self.open_barcode_details
        )

        self.barcode_details_button.grid(
            row=0,
            column=4,
            padx=(10, 0)
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
        # Reorder
        # ----------------------------------------------------------
        self.reorder_button = ctk.CTkButton(
            action_row,
            text="🔄 Reorder",
            width=120,
            height=38,
            fg_color="#F59E0B",
            hover_color="#D97706",
            command=self.open_reorder_popup
        )

        self.reorder_button.grid(
            row=0,
            column=3,
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
            column=4,
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

        products = get_products_with_barcodes()

        self.count_label.configure(
            text=f"{len(products)} Products Available"
        )

        self.populate_product_table(products)

    def validate_product_values(
        self,
        purchase_price,
        selling_price,
        stock,
        minimum_stock
    ):

        if purchase_price <= 0:
            return "Purchase price must be greater than 0."

        if selling_price <= 0:
            return "Selling price must be greater than 0."

        if stock < 0:
            return "Stock cannot be negative."

        if minimum_stock < 0:
            return "Minimum stock cannot be negative."

        return None

    # ==========================================================
    # PRODUCT FORM FIELD HELPER
    # ==========================================================

    def create_product_field(
        self,
        parent,
        label_text,
        variable
    ):

        ctk.CTkLabel(
            parent,
            text=label_text,
            font=("Poppins", 13, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(6, 2)
        )

        entry = ctk.CTkEntry(
            parent,
            textvariable=variable,
            width=430,
            height=36
        )

        entry.pack(
            padx=20
        )

        return entry
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
        # PRODUCT NAME
        # ======================================================

        self.create_product_field(
            form_frame,
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
            values=self.PRODUCT_CATEGORIES,
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

        self.create_product_field(
            form_frame,
            "Purchase Price",
            purchase_var
        )

        self.create_product_field(
            form_frame,
            "Selling Price",
            selling_var
        )

        self.create_product_field(
            form_frame,
            "Stock Quantity",
            stock_var
        )

        self.create_product_field(
            form_frame,
            "Minimum Stock",
            minimum_var
        )

        self.create_product_field(
            form_frame,
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

            error = self.validate_product_values(
                purchase_price,
                selling_price,
                stock,
                minimum_stock
            )

            if error:

                status.configure(
                    text=error,
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
    # COPY SELECTED PRODUCT BARCODE
    # ==========================================================

    def copy_selected_barcode(self):

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
        # Get selected row
        # ------------------------------------------------------

        values = self.table.item(
            selected[0],
            "values"
        )

        product_name = str(
            values[1]
        )

        barcode = str(
            values[5]
        ).strip()

        # ------------------------------------------------------
        # No barcode
        # ------------------------------------------------------

        if not barcode or barcode == "—":

            messagebox.showwarning(
                "No Barcode",
                f"{product_name.title()} does not have a barcode."
            )

            return

        # ------------------------------------------------------
        # Copy to clipboard
        # ------------------------------------------------------

        try:

            self.clipboard_clear()
            self.clipboard_append(barcode)
            self.update()

        except Exception as error:

            messagebox.showerror(
                "Copy Failed",
                f"Unable to copy barcode.\n\n{error}"
            )

            return

        # ------------------------------------------------------
        # Success
        # ------------------------------------------------------

        messagebox.showinfo(
            "Barcode Copied",
            f"Barcode copied successfully!\n\n"
            f"Product: {product_name.title()}\n"
            f"Barcode: {barcode}"
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
    # BARCODE DETAILS POPUP
    # ==========================================================

    def open_barcode_details(self):

        selected = self.table.selection()

        # ------------------------------------------------------
        # No selection
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
        product_name = str(values[1])
        current_barcode = str(values[5]).strip()

        # ------------------------------------------------------
        # Create popup
        # ------------------------------------------------------

        popup = ctk.CTkToplevel(self)

        popup.title("Barcode Details")
        popup.geometry("460x500")
        popup.minsize(460, 500)
        popup.maxsize(460, 500)
        popup.resizable(False, False)
        popup.grab_set()
        popup.configure(
            fg_color="white"
        )

        # ------------------------------------------------------
        # Header
        # ------------------------------------------------------

        ctk.CTkLabel(
            popup,
            text="🏷 Barcode Details",
            font=("Poppins", 24, "bold"),
            text_color="#065F46"
        ).pack(
            pady=(15, 5)
        )

        ctk.CTkLabel(
            popup,
            text=product_name.title(),
            font=("Poppins", 15, "bold"),
            text_color="#374151"
        ).pack(
            pady=(0, 10)
        )

        # ======================================================
        # SCROLLABLE CONTENT
        # ======================================================

        content_frame = ctk.CTkScrollableFrame(
            popup,
            fg_color="transparent"
        )

        content_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 5)
        )

        # ------------------------------------------------------
        # Barcode Card
        # ------------------------------------------------------

        barcode_card = ctk.CTkFrame(
            content_frame,
            fg_color="#F9FAFB",
            corner_radius=18,
            border_width=1,
            border_color="#E5E7EB"
        )

        barcode_card.pack(
            fill="x",
            padx=10,
            pady=5
        )

        ctk.CTkLabel(
            barcode_card,
            text="Barcode",
            font=("Poppins", 12, "bold"),
            text_color="#64748B"
        ).pack(
            pady=(15, 5)
        )

        barcode_display = (
            current_barcode
            if current_barcode and current_barcode != "—"
            else "No Barcode"
        )

        barcode_label = ctk.CTkLabel(
            barcode_card,
            text=barcode_display,
            font=("Poppins", 22, "bold"),
            text_color="#111827"
        )

        barcode_label.pack(
            pady=(0, 15)
        )

        # ------------------------------------------------------
        # Barcode Type
        # ------------------------------------------------------

        ctk.CTkLabel(
            barcode_card,
            text="Barcode Type",
            font=("Poppins", 10, "bold"),
            text_color="#64748B"
        ).pack(
            pady=(0, 2)
        )

        ctk.CTkLabel(
            barcode_card,
            text="Internal POS Barcode",
            font=("Poppins", 12, "bold"),
            text_color="#0F766E"
        ).pack(
            pady=(0, 15)
        )

        # ------------------------------------------------------
        # Status
        # ------------------------------------------------------

        if barcode_display == "No Barcode":

            status_text = (
                "⚠ This product does not have a barcode."
            )

            status_color = "#B45309"

        else:

            status_text = (
                "🟢 Barcode assigned and scanner-ready."
            )

            status_color = "#15803D"

        ctk.CTkLabel(
            content_frame,
            text=status_text,
            font=("Poppins", 11, "bold"),
            text_color=status_color
        ).pack(
            pady=(10, 15)
        )

        # ======================================================
        # FIXED BUTTON AREA
        # ======================================================

        button_frame = ctk.CTkFrame(
            popup,
            fg_color="white"
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        # ------------------------------------------------------
        # Copy Barcode
        # ------------------------------------------------------

        def copy_barcode():

            if (
                not current_barcode
                or current_barcode == "—"
            ):

                messagebox.showwarning(
                    "No Barcode",
                    "There is no barcode to copy.",
                    parent=popup
                )

                return

            self.clipboard_clear()
            self.clipboard_append(
                current_barcode
            )
            self.update()

            messagebox.showinfo(
                "Copied",
                f"Barcode copied:\n\n{current_barcode}",
                parent=popup
            )

        ctk.CTkButton(
            button_frame,
            text="📋 Copy Barcode",
            height=38,
            fg_color="#0EA5E9",
            hover_color="#0284C7",
            command=copy_barcode
        ).pack(
            fill="x",
            pady=3
        )


        # ------------------------------------------------------
        # Generate PNG
        # ------------------------------------------------------

        def generate_png():

            if (
                not current_barcode
                or current_barcode == "—"
            ):

                messagebox.showwarning(
                    "No Barcode",
                    "Generate or assign a barcode first.",
                    parent=popup
                )

                return

            popup.destroy()

            self.preview_barcode_png(
                product_id,
                product_name,
                current_barcode
            )


        ctk.CTkButton(
            button_frame,
            text="🖼 Generate PNG",
            height=38,
            fg_color="#0F766E",
            hover_color="#115E59",
            command=generate_png
        ).pack(
            fill="x",
            pady=3
        )
        # ------------------------------------------------------
        # Generate Barcode
        # ------------------------------------------------------

        def generate_barcode():

            if (
                current_barcode
                and current_barcode != "—"
            ):

                messagebox.showinfo(
                    "Barcode Already Exists",
                    "This product already has a barcode.",
                    parent=popup
                )

                return

            success, result = generate_product_barcode(
                product_id
            )

            if not success:

                messagebox.showerror(
                    "Generation Failed",
                    str(result),
                    parent=popup
                )

                return

            popup.destroy()

            self.load_products()

            messagebox.showinfo(
                "Barcode Generated",
                f"Barcode generated successfully:\n\n{result}"
            )

        ctk.CTkButton(
            button_frame,
            text="🏷 Generate Barcode",
            height=38,
            fg_color="#7C3AED",
            hover_color="#6D28D9",
            command=generate_barcode
        ).pack(
            fill="x",
            pady=3
        )

        # ------------------------------------------------------
        # Close
        # ------------------------------------------------------

        ctk.CTkButton(
            button_frame,
            text="Close",
            height=38,
            fg_color="#6B7280",
            hover_color="#4B5563",
            command=popup.destroy
        ).pack(
            fill="x",
            pady=3
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
        # PRODUCT NAME
        # ======================================================

        self.create_product_field(
            form_frame,
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
            values=self.PRODUCT_CATEGORIES,
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

        self.create_product_field(
            form_frame,
            "Purchase Price",
            purchase_var
        )

        self.create_product_field(
            form_frame,
            "Selling Price",
            selling_var
        )

        self.create_product_field(
            form_frame,
            "Stock Quantity",
            stock_var
        )

        self.create_product_field(
            form_frame,
            "Minimum Stock",
            minimum_var
        )

        self.create_product_field(
            form_frame,
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

            error = self.validate_product_values(
                purchase_price,
                selling_price,
                stock,
                minimum_stock
            )

            if error:

                status_label.configure(
                    text=error,
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
    # ADD STOCK / PURCHASE POPUP
    # ==========================================================

    def open_add_stock_popup(
            self,
            preset_quantity=None,
            preset_purchase_price=None
    ):

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

        product_id = int(
            values[0]
        )

        product_name = str(
            values[1]
        )

        current_stock = int(
            values[4]
        )

        popup = ctk.CTkToplevel(
            self
        )

        popup.title(
            "Stock In / Purchase"
        )

        popup.geometry(
            "470x600"
        )

        popup.minsize(
            470,
            600
        )

        popup.maxsize(
            470,
            600
        )

        popup.resizable(
            False,
            False
        )

        popup.grab_set()

        popup.configure(
            fg_color="white"
        )

        # ======================================================
        # HEADER
        # ======================================================

        ctk.CTkLabel(
            popup,
            text="📦 Stock In / Purchase",
            font=("Poppins", 23, "bold"),
            text_color="#EA580C"
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            popup,
            text=product_name.title(),
            font=("Poppins", 15, "bold"),
            text_color="#374151"
        ).pack(
            pady=(0, 3)
        )

        ctk.CTkLabel(
            popup,
            text=f"Current Stock: {current_stock}",
            font=("Poppins", 12),
            text_color="#64748B"
        ).pack(
            pady=(0, 15)
        )

        # ======================================================
        # SCROLLABLE FORM
        # ======================================================

        content = ctk.CTkScrollableFrame(
            popup,
            fg_color="transparent"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 5)
        )

        # ======================================================
        # SUPPLIER
        # ======================================================

        ctk.CTkLabel(
            content,
            text="Supplier",
            font=("Poppins", 13, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=20,
            pady=(8, 4)
        )

        suppliers = get_all_suppliers()

        supplier_map = {
            f"{supplier[0]} - {supplier[1]}": supplier[0]
            for supplier in suppliers
        }

        supplier_names = list(
            supplier_map.keys()
        )

        supplier_var = ctk.StringVar()

        supplier_combo = ctk.CTkComboBox(
            content,
            values=supplier_names
            if supplier_names
            else ["No suppliers available"],
            variable=supplier_var,
            height=40,
            state="readonly"
        )

        supplier_combo.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        if supplier_names:
            supplier_combo.set(
                supplier_names[0]
            )

        # ======================================================
        # QUANTITY
        # ======================================================

        ctk.CTkLabel(
            content,
            text="Quantity Received",
            font=("Poppins", 13, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 4)
        )

        quantity_var = ctk.StringVar(
            value=(
                str(preset_quantity)
                if preset_quantity is not None
                else ""
            )
        )

        quantity_entry = ctk.CTkEntry(
            content,
            textvariable=quantity_var,
            height=40,
            placeholder_text="Enter quantity"
        )

        quantity_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        # ======================================================
        # PURCHASE PRICE
        # ======================================================

        ctk.CTkLabel(
            content,
            text="Purchase Price / Unit",
            font=("Poppins", 13, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 4)
        )

        purchase_price_var = ctk.StringVar(
            value=(
                f"{preset_purchase_price:.2f}"
                if preset_purchase_price is not None
                else ""
            )
        )

        purchase_price_entry = ctk.CTkEntry(
            content,
            textvariable=purchase_price_var,
            height=40,
            placeholder_text="Example: 150.00"
        )

        purchase_price_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        # ======================================================
        # TOTAL COST
        # ======================================================

        total_var = ctk.StringVar(
            value="Total Purchase Cost: ₹0.00"
        )

        ctk.CTkLabel(
            content,
            textvariable=total_var,
            font=("Poppins", 16, "bold"),
            text_color="#EA580C"
        ).pack(
            anchor="w",
            padx=20,
            pady=(12, 8)
        )

        # ======================================================
        # STATUS
        # ======================================================

        status_var = ctk.StringVar()

        ctk.CTkLabel(
            content,
            textvariable=status_var,
            font=("Poppins", 10, "bold"),
            text_color="#B45309"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # ======================================================
        # LIVE TOTAL
        # ======================================================

        def update_total(event=None):

            try:

                quantity = int(
                    quantity_var.get().strip()
                )

                purchase_price = float(
                    purchase_price_var.get().strip()
                )

                if quantity <= 0 or purchase_price < 0:
                    raise ValueError

                total = (
                    quantity
                    * purchase_price
                )

                total_var.set(
                    f"Total Purchase Cost: "
                    f"₹{total:,.2f}"
                )

                status_var.set("")

            except ValueError:

                total_var.set(
                    "Total Purchase Cost: ₹0.00"
                )

        quantity_entry.bind(
            "<KeyRelease>",
            update_total
        )

        purchase_price_entry.bind(
            "<KeyRelease>",
            update_total
        )

        if (
            preset_quantity is not None
            and preset_purchase_price is not None
        ):
            update_total()
            
        # ======================================================
        # FIXED BUTTON AREA
        # ======================================================

        button_frame = ctk.CTkFrame(
            popup,
            fg_color="white"
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        # ======================================================
        # SAVE STOCK
        # ======================================================

        def save_stock():

            selected_supplier = (
                supplier_var.get()
                .strip()
            )

            if (
                not supplier_names
                or selected_supplier
                not in supplier_map
            ):

                status_var.set(
                    "Please select a supplier."
                )

                return

            supplier_id = supplier_map[
                selected_supplier
            ]

            try:

                quantity_to_add = int(
                    quantity_var.get().strip()
                )

                purchase_price = float(
                    purchase_price_var.get().strip()
                )

            except ValueError:

                status_var.set(
                    "Enter valid quantity and purchase price."
                )

                return

            if quantity_to_add <= 0:

                status_var.set(
                    "Quantity must be greater than zero."
                )

                return

            if purchase_price < 0:

                status_var.set(
                    "Purchase price cannot be negative."
                )

                return

            try:

                result = add_stock(
                    product_id,
                    quantity_to_add,
                    supplier_id,
                    purchase_price
                )

            except Exception as error:

                status_var.set(
                    f"Stock update failed: {error}"
                )

                return

            if not result.get(
                "success"
            ):

                status_var.set(
                    "Unable to update stock."
                )

                return

            new_stock = result[
                "new_stock"
            ]

            total_cost = result[
                "total_cost"
            ]

            popup.destroy()

            self.load_products()

            messagebox.showinfo(
                "Stock Updated",
                f"Product: {product_name.title()}\n"
                f"Quantity Added: {quantity_to_add}\n"
                f"New Stock: {new_stock}\n"
                f"Purchase Cost: ₹{total_cost:,.2f}"
            )

        ctk.CTkButton(
            button_frame,
            text="📦 Add Stock",
            height=42,
            fg_color="#EA580C",
            hover_color="#C2410C",
            font=("Poppins", 13, "bold"),
            command=save_stock
        ).pack(
            fill="x",
            pady=3
        )

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            height=42,
            fg_color="#6B7280",
            hover_color="#4B5563",
            font=("Poppins", 13, "bold"),
            command=popup.destroy
        ).pack(
            fill="x",
            pady=3
        )

        if supplier_names:
            supplier_combo.focus_set()

    # ==========================================================
    # REORDER LOW STOCK PRODUCT
    # ==========================================================

    def open_reorder_popup(self):

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

        product_id = int(
            values[0]
        )

        product_name = str(
            values[1]
        )

        current_stock = int(
            values[4]
        )

        # ------------------------------------------------------
        # Find product in low-stock list
        # ------------------------------------------------------

        low_stock_products = (
            get_low_stock_products_for_reorder()
        )

        product_info = next(
            (
                product
                for product in low_stock_products
                if int(product[0]) == product_id
            ),
            None
        )

        if not product_info:

            messagebox.showinfo(
                "Stock Level Healthy",
                f"{product_name.title()} is not currently "
                f"at or below its minimum stock level."
            )

            return

        (
            _product_id,
            _name,
            _stock,
            minimum_stock,
            purchase_price
        ) = product_info

        minimum_stock = int(
            minimum_stock
        )

        purchase_price = float(
            purchase_price
        )

        # ------------------------------------------------------
        # Suggested reorder quantity
        # ------------------------------------------------------

        suggested_quantity = max(
            (minimum_stock * 2) - current_stock,
            1
        )

        # ------------------------------------------------------
        # Open the existing Stock In / Purchase workflow
        # ------------------------------------------------------

        self.open_add_stock_popup(
            preset_quantity=suggested_quantity,
            preset_purchase_price=purchase_price
        )
        
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

        try:

            deleted = delete_product(
                product_id
            )

        except Exception as error:

            messagebox.showerror(
                "Cannot Delete Product",
                str(error)
            )

            return

        if deleted:

            self.load_products()

            messagebox.showinfo(
                "Deleted",
                f"{product_name.title()} deleted successfully!"
            )

    # ==========================================================
    # LIVE SEARCH PRODUCTS
    # ==========================================================

    def search_products_event(self, event=None):

        keyword = self.search_entry.get().strip().lower()

        if not keyword:
            self.load_products()
            return

        products = search_products(keyword)

        self.count_label.configure(
            text=f"{len(products)} Products Found"
        )

        self.populate_product_table(products)

        # ==========================================================
        # GENERATE BARCODE PNG
        # ==========================================================

    def generate_barcode_png(
            self,
            product_id,
            barcode_value
        ):

            if (
                not barcode_value
                or barcode_value == "—"
            ):
                messagebox.showwarning(
                    "No Barcode",
                    "This product does not have a barcode."
                )
                return None

            # ------------------------------------------------------
            # Output directory
            # ------------------------------------------------------

            OUTPUT_DIR = self.BARCODE_IMAGES_DIR

            os.makedirs(
                OUTPUT_DIR,
                exist_ok=True
            )

            output_base = os.path.join(
                OUTPUT_DIR,
                f"barcode_{product_id}"
            )

            # ------------------------------------------------------
            # Generate real Code 128 PNG
            # ------------------------------------------------------

            code = barcode.get(
                "code128",
                str(barcode_value),
                writer=ImageWriter()
            )

            code.save(
                output_base,
                options={
                    "write_text": True,
                    "font_size": 20,
                    "text_distance": 16,
                    "module_width": 0.40,
                    "module_height": 30,
                    "quiet_zone": 10,
                    "dpi": 300
                }
            )

            png_path = f"{output_base}.png"

            return png_path


        # ==========================================================
        # PREVIEW BARCODE PNG
        # ==========================================================

    def preview_barcode_png(
            self,
            product_id,
            product_name,
            barcode_value
        ):

            png_path = self.generate_barcode_png(
                product_id,
                barcode_value
            )

            if not png_path:
                return

            preview = ctk.CTkToplevel(self)

            preview.title(
                "Barcode Image"
            )

            preview.geometry(
                "620x430"
            )

            preview.minsize(
                620,
                430
            )

            preview.maxsize(
                620,
                430
            )

            preview.resizable(
                False,
                False
            )

            preview.grab_set()

            preview.configure(
                fg_color="#F9FAFB"
            )

            # ------------------------------------------------------
            # Header
            # ------------------------------------------------------

            ctk.CTkLabel(
                preview,
                text="🖼 Barcode Image",
                font=("Poppins", 22, "bold"),
                text_color="#065F46"
            ).pack(
                pady=(20, 5)
            )

            ctk.CTkLabel(
                preview,
                text=product_name.title(),
                font=("Poppins", 14, "bold"),
                text_color="#374151"
            ).pack(
                pady=(0, 10)
            )

            # ------------------------------------------------------
            # Load generated PNG
            # ------------------------------------------------------

            image = Image.open(
                png_path
            ).convert("RGB")

            # Keep the saved PNG unchanged.
            # Only resize the DISPLAY copy.
            preview_image = image.copy()

            preview_image.thumbnail(
                (520, 220),
                Image.Resampling.LANCZOS
            )

            ctk_image = ctk.CTkImage(
                light_image=preview_image,
                dark_image=preview_image,
                size=(
                    preview_image.width,
                    preview_image.height
                )
            )

            image_label = ctk.CTkLabel(
                preview,
                text="",
                image=ctk_image
            )

            image_label.pack(
                pady=8
            )

            # ------------------------------------------------------
            # Saved path
            # ------------------------------------------------------

            ctk.CTkLabel(
                preview,
                text=f"Saved: {png_path}",
                font=("Poppins", 9),
                text_color="#64748B"
            ).pack(
                pady=(2, 8)
            )

            # ------------------------------------------------------
            # Buttons
            # ------------------------------------------------------

            button_frame = ctk.CTkFrame(
                preview,
                fg_color="transparent"
            )

            button_frame.pack(
                fill="x",
                padx=25,
                pady=8
            )

            def open_folder():

                folder = self.BARCODE_IMAGES_DIR

                os.makedirs(
                    folder,
                    exist_ok=True
                )

                subprocess.Popen(
                    ["xdg-open", folder]
                )

            ctk.CTkButton(
                button_frame,
                text="📁 Open Barcode Folder",
                height=40,
                fg_color="#2563EB",
                hover_color="#1D4ED8",
                command=open_folder
            ).pack(
                side="left",
                expand=True,
                padx=5
            )

            ctk.CTkButton(
                button_frame,
                text="Close",
                height=40,
                fg_color="#6B7280",
                hover_color="#4B5563",
                command=preview.destroy
            ).pack(
                side="left",
                expand=True,
                padx=5
            )

    def populate_product_table(self, products):

        for row in self.table.get_children():
            self.table.delete(row)

        for (
            product_id,
            name,
            category,
            selling_price,
            stock,
            barcode
        ) in products:

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