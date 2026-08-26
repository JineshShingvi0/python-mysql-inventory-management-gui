import customtkinter as ctk
import os
import barcode

from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
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
    # GENERATE BARCODE LABEL
    # ==========================================================

    def generate_barcode_label(
        self,
        product_id,
        product_name,
        selling_price,
        product_barcode
        ):

        # ------------------------------------------------------
        # Validate barcode
        # ------------------------------------------------------

        if (
            not product_barcode
            or product_barcode == "—"
        ):

            messagebox.showwarning(
                "No Barcode",
                "This product does not have a barcode."
            )

            return

        # ------------------------------------------------------
        # Create output directory
        # ------------------------------------------------------

        labels_dir = "barcode_labels"

        os.makedirs(
            labels_dir,
            exist_ok=True
        )

        # ------------------------------------------------------
        # Temporary barcode filename
        # ------------------------------------------------------

        barcode_base = os.path.join(
            labels_dir,
            f"barcode_{product_id}"
        )

        # ------------------------------------------------------
        # Generate Code 128 barcode
        # ------------------------------------------------------

        code = barcode.get(
            "code128",
            str(product_barcode),
            writer=ImageWriter()
        )

        barcode_file = code.save(
            barcode_base
        )

        # python-barcode returns the actual PNG path
        barcode_file = f"{barcode_base}.png"

        # ------------------------------------------------------
        # Open barcode image
        # ------------------------------------------------------

        barcode_image = Image.open(
            barcode_file
        ).convert("RGB")

        # ------------------------------------------------------
        # Label dimensions
        # ------------------------------------------------------

        label_width = 700
        label_height = 430

        label = Image.new(
            "RGB",
            (
                label_width,
                label_height
            ),
            "white"
        )

        draw = ImageDraw.Draw(
            label
        )

        # ------------------------------------------------------
        # Fonts
        # ------------------------------------------------------

        try:

            title_font = ImageFont.truetype(
                "DejaVuSans-Bold.ttf",
                34
            )

            product_font = ImageFont.truetype(
                "DejaVuSans-Bold.ttf",
                30
            )

            price_font = ImageFont.truetype(
                "DejaVuSans-Bold.ttf",
                28
            )

            barcode_font = ImageFont.truetype(
                "DejaVuSans.ttf",
                22
            )

        except Exception:

            title_font = ImageFont.load_default()
            product_font = ImageFont.load_default()
            price_font = ImageFont.load_default()
            barcode_font = ImageFont.load_default()

        # ------------------------------------------------------
        # Border
        # ------------------------------------------------------

        draw.rounded_rectangle(
            (5, 5, label_width - 5, label_height - 5),
            radius=20,
            outline="#065F46",
            width=4
        )

        # ------------------------------------------------------
        # Store Name
        # ------------------------------------------------------

        store_text = "SHINGVI SUPERMART"

        store_box = draw.textbbox(
            (0, 0),
            store_text,
            font=title_font
        )

        store_width = (
            store_box[2] - store_box[0]
        )

        draw.text(
            (
                (label_width - store_width) / 2,
                25
            ),
            store_text,
            font=title_font,
            fill="#065F46"
        )

        # ------------------------------------------------------
        # Product Name
        # ------------------------------------------------------

        product_text = product_name.title()

        product_box = draw.textbbox(
            (0, 0),
            product_text,
            font=product_font
        )

        product_width = (
            product_box[2] - product_box[0]
        )

        draw.text(
            (
                (label_width - product_width) / 2,
                85
            ),
            product_text,
            font=product_font,
            fill="#111827"
        )

        # ------------------------------------------------------
        # Price
        # ------------------------------------------------------

        price_text = f"₹{float(selling_price):,.2f}"

        price_box = draw.textbbox(
            (0, 0),
            price_text,
            font=price_font
        )

        price_width = (
            price_box[2] - price_box[0]
        )

        draw.text(
            (
                (label_width - price_width) / 2,
                135
            ),
            price_text,
            font=price_font,
            fill="#16A34A"
        )

        # ------------------------------------------------------
        # Resize barcode
        # ------------------------------------------------------

        barcode_image.thumbnail(
            (
                600,
                150
            )
        )

        barcode_x = (
            label_width - barcode_image.width
        ) // 2

        barcode_y = 190

        label.paste(
            barcode_image,
            (
                barcode_x,
                barcode_y
            )
        )

        # ------------------------------------------------------
        # Barcode Number
        # ------------------------------------------------------

        barcode_text = str(
            product_barcode
        )

        barcode_box = draw.textbbox(
            (0, 0),
            barcode_text,
            font=barcode_font
        )

        barcode_width = (
            barcode_box[2] - barcode_box[0]
        )

        draw.text(
            (
                (label_width - barcode_width) / 2,
                355
            ),
            barcode_text,
            font=barcode_font,
            fill="#111827"
        )

        # ------------------------------------------------------
        # Footer
        # ------------------------------------------------------

        footer_text = "Internal POS Barcode"

        footer_box = draw.textbbox(
            (0, 0),
            footer_text,
            font=barcode_font
        )

        footer_width = (
            footer_box[2] - footer_box[0]
        )

        draw.text(
            (
                (label_width - footer_width) / 2,
                390
            ),
            footer_text,
            font=barcode_font,
            fill="#64748B"
        )

        # ------------------------------------------------------
        # Save final label
        # ------------------------------------------------------

        label_path = os.path.join(
            labels_dir,
            f"label_{product_id}.png"
        )

        label.save(
            label_path,
            "PNG"
        )

        return label_path


    # ==========================================================
    # GENERATE BARCODE LABEL PDF
    # ==========================================================

    def generate_barcode_label_pdf(
        self,
        product_id,
        product_name,
        selling_price,
        product_barcode
    ):

        if (
            not product_barcode
            or product_barcode == "—"
        ):

            messagebox.showwarning(
                "No Barcode",
                "This product does not have a barcode."
            )

            return None

        # ------------------------------------------------------
        # Generate PNG label first
        # ------------------------------------------------------

        label_path = self.generate_barcode_label(
            product_id,
            product_name,
            selling_price,
            product_barcode
        )

        if not label_path:
            return None

        # ------------------------------------------------------
        # PDF output directory
        # ------------------------------------------------------

        labels_dir = "barcode_labels"

        os.makedirs(
            labels_dir,
            exist_ok=True
        )

        pdf_path = os.path.join(
            labels_dir,
            f"label_{product_id}.pdf"
        )

        # ------------------------------------------------------
        # Create A4 PDF
        # ------------------------------------------------------

        pdf = canvas.Canvas(
            pdf_path,
            pagesize=A4
        )

        page_width, page_height = A4

        # ------------------------------------------------------
        # Label dimensions on PDF
        # ------------------------------------------------------

        label_width = 500
        label_height = 310

        x = (
            page_width - label_width
        ) / 2

        y = (
            page_height - label_height
        ) / 2

        # ------------------------------------------------------
        # Draw label image
        # ------------------------------------------------------

        pdf.drawImage(
            ImageReader(label_path),
            x,
            y,
            width=label_width,
            height=label_height,
            preserveAspectRatio=True,
            mask="auto"
        )

        pdf.showPage()
        pdf.save()

        return pdf_path
    # ==========================================================
    # PREVIEW BARCODE LABEL
    # ==========================================================

    def preview_barcode_label(
        self,
        product_id,
        product_name,
        selling_price,
        barcode_value
    ):

        label_path = self.generate_barcode_label(
            product_id,
            product_name,
            selling_price,
            barcode_value
        )

        if not label_path:
            return

        preview = ctk.CTkToplevel(self)

        preview.title(
            "Barcode Label Preview"
        )

        preview.geometry(
            "820x650"
        )

        preview.minsize(
            820,
            650
        )

        preview.grab_set()

        preview.configure(
            fg_color="#F9FAFB"
        )

        # ------------------------------------------------------
        # Title
        # ------------------------------------------------------

        ctk.CTkLabel(
            preview,
            text="🖨 Barcode Label Preview",
            font=("Poppins", 24, "bold"),
            text_color="#065F46"
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            preview,
            text=product_name.title(),
            font=("Poppins", 14),
            text_color="#64748B"
        ).pack(
            pady=(0, 15)
        )

        # ------------------------------------------------------
        # Load image
        # ------------------------------------------------------

        preview_image = Image.open(
            label_path
        )

        preview_image.thumbnail(
            (
                700,
                430
            )
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
            pady=10
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
            padx=30,
            pady=15
        )


        ctk.CTkButton(
            button_frame,
            text="📄 Save PDF",
            height=42,
            fg_color="#0F766E",
            hover_color="#115E59",
            command=lambda: self._save_label_pdf_from_preview(
                product_id,
                product_name,
                selling_price,
                barcode_value,
                preview
            )
        ).pack(
            side="left",
            expand=True,
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="📁 Open Label Folder",
            height=42,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=lambda: os.system(
                f'xdg-open "{os.path.dirname(label_path)}"'
            )
        ).pack(
            side="left",
            expand=True,
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Close",
            height=42,
            fg_color="#6B7280",
            hover_color="#4B5563",
            command=preview.destroy
        ).pack(
            side="left",
            expand=True,
            padx=5
        )


    # ==========================================================
    # SAVE LABEL PDF FROM PREVIEW
    # ==========================================================

    def _save_label_pdf_from_preview(
        self,
        product_id,
        product_name,
        selling_price,
        barcode_value,
        preview
    ):

        pdf_path = self.generate_barcode_label_pdf(
            product_id,
            product_name,
            selling_price,
            barcode_value
        )

        if not pdf_path:
            return

        messagebox.showinfo(
            "PDF Created",
            f"Barcode label PDF created successfully!\n\n"
            f"{pdf_path}",
            parent=preview
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
    # ADD STOCK / PURCHASE POPUP
    # ==========================================================

    def open_add_stock_popup(self):

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

        supplier_var = ctk.StringVar()

        supplier_entry = ctk.CTkEntry(
            content,
            textvariable=supplier_var,
            height=40,
            placeholder_text="Enter supplier name"
        )

        supplier_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
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

        quantity_var = ctk.StringVar()

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

        purchase_price_var = ctk.StringVar()

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

            supplier = (
                supplier_var.get()
                .strip()
            )

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
                    supplier,
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

        supplier_entry.focus_set()
        
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

        # --------------------------------------------------
        # Empty search → restore all products
        # --------------------------------------------------

        if keyword == "":
            self.load_products()
            return

        # --------------------------------------------------
        # Search backend
        # --------------------------------------------------

        products = search_products(keyword)

        # --------------------------------------------------
        # Clear current table
        # --------------------------------------------------

        for row in self.table.get_children():
            self.table.delete(row)

        # --------------------------------------------------
        # Update result count
        # --------------------------------------------------

        self.count_label.configure(
            text=f"{len(products)} Products Found"
        )

        # --------------------------------------------------
        # Insert search results
        # --------------------------------------------------

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

    # ==========================================================
    # LABEL GENERATOR POPUP
    # ==========================================================

    def open_label_generator(
        self,
        product_id,
        product_name,
        selling_price,
        barcode_value
    ):

        if (
            not barcode_value
            or barcode_value == "—"
        ):

            messagebox.showwarning(
                "No Barcode",
                "Generate or assign a barcode first."
            )

            return

        popup = ctk.CTkToplevel(self)

        popup.title(
            "Barcode Label Generator"
        )

        popup.geometry(
            "460x560"
        )

        popup.minsize(
            460,
            560
        )

        popup.maxsize(
            460,
            560
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
            text="🖨 Barcode Label Generator",
            font=("Poppins", 22, "bold"),
            text_color="#065F46"
        ).pack(
            pady=(15, 5)
        )

        ctk.CTkLabel(
            popup,
            text=product_name.title(),
            font=("Poppins", 14, "bold"),
            text_color="#374151"
        ).pack(
            pady=(0, 8)
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

        # ======================================================
        # PRODUCT INFORMATION CARD
        # ======================================================

        info_frame = ctk.CTkFrame(
            content_frame,
            fg_color="#F9FAFB",
            corner_radius=16,
            border_width=1,
            border_color="#E5E7EB"
        )

        info_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        ctk.CTkLabel(
            info_frame,
            text=f"Barcode: {barcode_value}",
            font=("Poppins", 12, "bold"),
            text_color="#111827"
        ).pack(
            pady=(14, 5)
        )

        ctk.CTkLabel(
            info_frame,
            text=(
                f"Selling Price: "
                f"₹{float(selling_price):,.2f}"
            ),
            font=("Poppins", 11),
            text_color="#64748B"
        ).pack(
            pady=(0, 5)
        )

        ctk.CTkLabel(
            info_frame,
            text="Barcode Type: Internal POS Barcode",
            font=("Poppins", 10, "bold"),
            text_color="#0F766E"
        ).pack(
            pady=(0, 14)
        )

        # ======================================================
        # NUMBER OF LABELS
        # ======================================================

        ctk.CTkLabel(
            content_frame,
            text="Number of Labels",
            font=("Poppins", 13, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        label_count_var = ctk.StringVar(
            value="1"
        )

        label_count_entry = ctk.CTkEntry(
            content_frame,
            textvariable=label_count_var,
            width=140,
            height=40,
            justify="center",
            font=("Poppins", 14, "bold")
        )

        label_count_entry.pack()

        label_count_entry.select_range(
            0,
            "end"
        )

        # ======================================================
        # OPTIONAL NOTE
        # ======================================================

        ctk.CTkLabel(
            content_frame,
            text=(
                "Tip: You can generate up to "
                "500 labels at once."
            ),
            font=("Poppins", 10),
            text_color="#64748B"
        ).pack(
            pady=(10, 20)
        )

        # ======================================================
        # STATUS
        # ======================================================

        status_label = ctk.CTkLabel(
            popup,
            text="",
            font=("Poppins", 10, "bold")
        )

        status_label.pack(
            pady=(0, 5)
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

        # ======================================================
        # GENERATE MULTIPLE LABELS
        # ======================================================

        def generate_multiple_labels():

            try:

                count = int(
                    label_count_var.get().strip()
                )

            except ValueError:

                status_label.configure(
                    text="Enter a valid whole number.",
                    text_color="red"
                )

                return

            if count <= 0:

                status_label.configure(
                    text="Number of labels must be at least 1.",
                    text_color="red"
                )

                return

            if count > 500:

                status_label.configure(
                    text="Maximum 500 labels at once.",
                    text_color="red"
                )

                return

            try:

                pdf_path = (
                    self.generate_multiple_barcode_labels(
                        product_id,
                        product_name,
                        selling_price,
                        barcode_value,
                        count
                    )
                )

            except Exception as error:

                status_label.configure(
                    text=f"Generation failed: {error}",
                    text_color="red"
                )

                return

            if not pdf_path:

                status_label.configure(
                    text="Unable to create the PDF.",
                    text_color="red"
                )

                return

            status_label.configure(
                text=f"✅ {count} label(s) created successfully.",
                text_color="#15803D"
            )

            messagebox.showinfo(
                "Labels Generated",
                f"{count} barcode label(s) generated successfully!\n\n"
                f"{pdf_path}",
                parent=popup
            )


        # ======================================================
        # OPEN FOLDER
        # ======================================================

        def open_label_folder():

            labels_dir = os.path.abspath(
                "barcode_labels"
            )

            os.makedirs(
                labels_dir,
                exist_ok=True
            )

            try:

                os.system(
                    f'xdg-open "{labels_dir}"'
                )

            except Exception as error:

                messagebox.showerror(
                    "Unable to Open Folder",
                    str(error),
                    parent=popup
                )

        # ======================================================
        # GENERATE PDF BUTTON
        # ======================================================

        ctk.CTkButton(
            button_frame,
            text="📄 Generate PDF",
            height=40,
            fg_color="#0F766E",
            hover_color="#115E59",
            font=("Poppins", 13, "bold"),
            command=generate_multiple_labels
        ).pack(
            fill="x",
            pady=3
        )

        # ======================================================
        # OPEN FOLDER BUTTON
        # ======================================================

        ctk.CTkButton(
            button_frame,
            text="📁 Open Label Folder",
            height=40,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=("Poppins", 13, "bold"),
            command=open_label_folder
        ).pack(
            fill="x",
            pady=3
        )

        # ======================================================
        # CANCEL
        # ======================================================

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            height=40,
            fg_color="#6B7280",
            hover_color="#4B5563",
            font=("Poppins", 13, "bold"),
            command=popup.destroy
        ).pack(
            fill="x",
            pady=3
        )

        label_count_entry.focus_set()


        # ==========================================================
        # GENERATE BARCODE PNG
        # ==========================================================

    def generate_barcode_png(
            self,
            product_id,
            product_name,
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

            output_dir = "barcode_images"

            os.makedirs(
                output_dir,
                exist_ok=True
            )

            output_base = os.path.join(
                output_dir,
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
                product_name,
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

                folder = os.path.abspath(
                    "barcode_images"
                )

                os.makedirs(
                    folder,
                    exist_ok=True
                )

                os.system(
                    f'xdg-open "{folder}"'
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
    # ==========================================================
    # GENERATE MULTIPLE BARCODE LABELS
    # ==========================================================

    def generate_multiple_barcode_labels(
        self,
        product_id,
        product_name,
        selling_price,
        barcode_value,
        label_count
    ):

        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.graphics.barcode import code128
        from reportlab.graphics import renderPDF

        if not barcode_value or barcode_value == "—":
            return None

        # ------------------------------------------------------
        # Output directory
        # ------------------------------------------------------

        labels_dir = "barcode_labels"

        os.makedirs(
            labels_dir,
            exist_ok=True
        )

        # ------------------------------------------------------
        # PDF path
        # ------------------------------------------------------

        pdf_path = os.path.join(
            labels_dir,
            f"labels_{product_id}_{label_count}.pdf"
        )

        pdf = canvas.Canvas(
            pdf_path,
            pagesize=A4
        )

        page_width, page_height = A4

        # ======================================================
        # LABEL GRID
        # ======================================================

        margin_x = 25
        margin_y = 28

        label_width = 270
        label_height = 175

        gap_x = 12
        gap_y = 12

        columns = 2
        rows = 4

        labels_per_page = columns * rows

        # ======================================================
        # BARCODE SETTINGS
        # ======================================================

        barcode_width = 220
        barcode_height = 48

        # ======================================================
        # CREATE LABELS
        # ======================================================

        for index in range(label_count):

            position = index % labels_per_page

            if position == 0 and index != 0:
                pdf.showPage()

            row = position // columns
            column = position % columns

            x = (
                margin_x
                + column * (
                    label_width + gap_x
                )
            )

            y = (
                page_height
                - margin_y
                - (row + 1) * label_height
                - row * gap_y
            )

            # ==================================================
            # BORDER
            # ==================================================

            pdf.setLineWidth(1.2)

            pdf.setStrokeColorRGB(
                0.025,
                0.373,
                0.275
            )

            pdf.roundRect(
                x,
                y,
                label_width,
                label_height,
                8,
                stroke=1,
                fill=0
            )

            # ==================================================
            # STORE NAME
            # ==================================================

            pdf.setFillColorRGB(
                0.025,
                0.373,
                0.275
            )

            pdf.setFont(
                "Helvetica-Bold",
                11
            )

            pdf.drawCentredString(
                x + label_width / 2,
                y + label_height - 20,
                "SHINGVI SUPERMART"
            )

            # ==================================================
            # PRODUCT NAME
            # ==================================================

            pdf.setFillColorRGB(
                0.067,
                0.094,
                0.153
            )

            pdf.setFont(
                "Helvetica-Bold",
                10
            )

            product_display = product_name.title()

            if len(product_display) > 28:

                product_display = (
                    product_display[:25] + "..."
                )

            pdf.drawCentredString(
                x + label_width / 2,
                y + label_height - 38,
                product_display
            )

            # ==================================================
            # PRICE
            # ==================================================

            pdf.setFillColorRGB(
                0.086,
                0.639,
                0.290
            )

            pdf.setFont(
                "Helvetica-Bold",
                10
            )

            pdf.drawCentredString(
                x + label_width / 2,
                y + label_height - 55,
                f"₹{float(selling_price):,.2f}"
            )

            # ==================================================
            # REAL VECTOR CODE 128 BARCODE
            # ==================================================

            barcode_value = str(barcode_value)

            barcode_drawing = createBarcodeDrawing(
                "Code128",
                value=barcode_value,
                barHeight=48,
                barWidth=0.8,
                humanReadable=False
            )

            # Center the vector barcode inside the label
            barcode_x = (
                x
                + (label_width - barcode_drawing.width) / 2
            )

            barcode_y = y + 48

            renderPDF.draw(
                barcode_drawing,
                pdf,
                barcode_x,
                barcode_y
            )
            # ==================================================
            # BARCODE NUMBER
            # ==================================================

            pdf.setFillColorRGB(
                0.067,
                0.094,
                0.153
            )

            pdf.setFont(
                "Helvetica",
                8
            )

            pdf.drawCentredString(
                x + label_width / 2,
                y + 27,
                barcode_value
            )

            # ==================================================
            # BARCODE TYPE
            # ==================================================

            pdf.setFillColorRGB(
                0.39,
                0.45,
                0.50
            )

            pdf.setFont(
                "Helvetica",
                6.5
            )

            pdf.drawCentredString(
                x + label_width / 2,
                y + 12,
                "Internal POS Barcode"
            )

        # ------------------------------------------------------
        # Save
        # ------------------------------------------------------

        pdf.showPage()
        pdf.save()

        return pdf_path