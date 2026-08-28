import customtkinter as ctk
from tkinter import ttk, messagebox

from backend import (
    get_all_suppliers,
    search_suppliers,
    add_supplier,
    update_supplier,
    delete_supplier,
    get_supplier_summary,
    get_supplier_purchase_history
)


class SuppliersPage(ctk.CTkScrollableFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#F9FAFB",
            scrollbar_button_color="#0F766E",
            scrollbar_button_hover_color="#115E59"
        )
        self.build_ui()
        self.load_suppliers()

    # ==========================================================
    # BUILD UI
    # ==========================================================

    def build_ui(self):

        # ------------------------------------------------------
        # Title
        # ------------------------------------------------------

        ctk.CTkLabel(
            self,
            text="Suppliers",
            font=("Poppins", 28, "bold"),
            text_color="#065F46"
        ).pack(
            anchor="w",
            padx=30,
            pady=(20, 5)
        )

        self.supplier_count_label = ctk.CTkLabel(
            self,
            text="0 Suppliers Registered",
            font=("Poppins", 13),
            text_color="gray40"
        )

        self.supplier_count_label.pack(
            anchor="w",
            padx=30
        )

        # ======================================================
        # SEARCH / TOOLBAR
        # ======================================================

        toolbar = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        toolbar.pack(
            fill="x",
            padx=30,
            pady=15
        )

        self.search_var = ctk.StringVar()

        self.search_entry = ctk.CTkEntry(
            toolbar,
            textvariable=self.search_var,
            placeholder_text="Search supplier by name, phone or email...",
            width=320,
            height=38
        )

        self.search_entry.pack(
            side="left"
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.live_search
        )

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            width=90,
            height=38,
            command=self.load_suppliers
        ).pack(
            side="left",
            padx=10
        )

        self.delete_button = ctk.CTkButton(
            toolbar,
            text="🗑 Delete",
            width=110,
            height=38,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.remove_supplier
        )

        self.delete_button.pack(
            side="right",
            padx=10
        )

        self.update_button = ctk.CTkButton(
            toolbar,
            text="✏ Update",
            width=110,
            height=38,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.open_update_supplier_popup
        )

        self.update_button.pack(
            side="right",
            padx=10
        )

        self.add_button = ctk.CTkButton(
            toolbar,
            text="+ Add Supplier",
            width=140,
            height=38,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.open_add_supplier_popup
        )

        self.add_button.pack(
            side="right"
        )
        # ==========================================================
        # SUPPLIER DETAILS VARIABLES
        # ==========================================================

        self.detail_name = ctk.StringVar(value="--")
        self.detail_phone = ctk.StringVar(value="--")
        self.detail_email = ctk.StringVar(value="--")
        self.detail_address = ctk.StringVar(value="--")
        self.detail_total_spent = ctk.StringVar(value="₹0.00")
        self.detail_purchase_count = ctk.StringVar(value="0")
        self.detail_units = ctk.StringVar(value="0")
        self.detail_last_purchase = ctk.StringVar(value="--")

        # ======================================================
        # TABLE
        # ======================================================

        table_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        table_frame.pack(
            fill="x",
            padx=30,
            pady=(5, 20)
        )

        columns = (
            "ID",
            "Name",
            "Phone",
            "Email",
            "Address",
            "Notes"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=16
        )

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

        self.table.column(
            "ID",
            width=60,
            anchor="center",
            stretch=False
        )

        self.table.column(
            "Name",
            width=170,
            stretch=False
        )

        self.table.column(
            "Phone",
            width=130,
            stretch=False
        )

        self.table.column(
            "Email",
            width=190,
            stretch=False
        )

        self.table.column(
            "Address",
            width=190,
            stretch=False
        )

        self.table.column(
            "Notes",
            width=200,
            stretch=False
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.load_supplier_profile
        )


        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        horizontal_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.table.xview
        )

        self.table.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        self.table.pack(
            side="top",
            fill="both",
            expand=True
        )

        vertical_scroll.pack(
            side="right",
            fill="y"
        )

        horizontal_scroll.pack(
            side="bottom",
            fill="x"
        )   

        # ==========================================================
        # SUPPLIER DETAILS
        # ==========================================================

        details_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=18,
            border_width=1,
            border_color="#D1D5DB"
        )

        details_frame.pack(
            fill="x",
            padx=30,
            pady=(5, 25)
        )

        ctk.CTkLabel(
            details_frame,
            text="🏭 Supplier Details",
            font=("Poppins", 20, "bold"),
            text_color="#065F46"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )


        def detail_row(label, variable):

            row = ctk.CTkFrame(
                details_frame,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=20,
                pady=5
            )

            ctk.CTkLabel(
                row,
                text=label,
                font=("Poppins", 12),
                text_color="#374151"
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                row,
                textvariable=variable,
                font=("Poppins", 12, "bold"),
                text_color="#065F46"
            ).pack(
                side="right"
            )


        detail_row(
            "Supplier Name",
            self.detail_name
        )

        detail_row(
            "Phone",
            self.detail_phone
        )

        detail_row(
            "Email",
            self.detail_email
        )

        detail_row(
            "Address",
            self.detail_address
        )

        detail_row(
            "Total Purchase Value",
            self.detail_total_spent
        )

        detail_row(
            "Purchase Transactions",
            self.detail_purchase_count
        )

        detail_row(
            "Total Units Supplied",
            self.detail_units
        )

        detail_row(
            "Last Purchase",
            self.detail_last_purchase
        )

        # ==========================================================
        # SUPPLIER PURCHASE HISTORY
        # ==========================================================

        history_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=18,
            border_width=1,
            border_color="#D1D5DB"
        )

        history_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 25)
        )

        ctk.CTkLabel(
            history_frame,
            text="📦 Purchase History",
            font=("Poppins", 20, "bold"),
            text_color="#EA580C"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        history_table_frame = ctk.CTkFrame(
            history_frame,
            fg_color="transparent"
        )

        history_table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        history_columns = (
            "Purchase ID",
            "Product",
            "Qty",
            "Purchase Price",
            "Total Cost",
            "Date"
        )

        self.supplier_history_table = ttk.Treeview(
            history_table_frame,
            columns=history_columns,
            show="headings",
            height=6
        )

        for column in history_columns:
            self.supplier_history_table.heading(
                column,
                text=column
            )

        self.supplier_history_table.column(
            "Purchase ID",
            width=90,
            anchor="center"
        )

        self.supplier_history_table.column(
            "Product",
            width=200
        )

        self.supplier_history_table.column(
            "Qty",
            width=80,
            anchor="center"
        )

        self.supplier_history_table.column(
            "Purchase Price",
            width=130,
            anchor="e"
        )

        self.supplier_history_table.column(
            "Total Cost",
            width=130,
            anchor="e"
        )

        self.supplier_history_table.column(
            "Date",
            width=160,
            anchor="center"
        )

        history_scroll = ttk.Scrollbar(
            history_table_frame,
            orient="vertical",
            command=self.supplier_history_table.yview
        )

        self.supplier_history_table.configure(
            yscrollcommand=history_scroll.set
        )

        self.supplier_history_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        history_scroll.pack(
            side="right",
            fill="y"
        )

        # ------------------------------------------------------
        # Table style
        # ------------------------------------------------------

        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Supplier.Treeview",
            rowheight=34,
            font=("Poppins", 11),
            background="white",
            fieldbackground="white"
        )

        style.configure(
            "Supplier.Treeview.Heading",
            font=("Poppins", 11, "bold"),
            background="#065F46",
            foreground="white"
        )

        self.table.configure(
            style="Supplier.Treeview"
        )

    # ==========================================================
    # LOAD SUPPLIER PROFILE
    # ==========================================================

    def load_supplier_profile(
        self,
        event=None
    ):

        selected = self.table.selection()

        if not selected:

            self.clear_supplier_profile()

            return

        values = self.table.item(
            selected[0],
            "values"
        )

        supplier_id = int(
            values[0]
        )

        self.detail_name.set(
            values[1]
        )

        self.detail_phone.set(
            values[2] or "--"
        )

        self.detail_email.set(
            values[3] or "--"
        )

        self.detail_address.set(
            values[4] or "--"
        )

        try:

            self.load_supplier_purchase_history(
                supplier_id
            )

            summary = get_supplier_summary(
                supplier_id
            )

        except Exception:

            self.detail_total_spent.set(
                "₹0.00"
            )

            self.detail_purchase_count.set(
                "0"
            )

            self.detail_units.set(
                "0"
            )

            self.detail_last_purchase.set(
                "--"
            )

            return

        self.detail_total_spent.set(
            f"₹{summary['total_spent']:,.2f}"
        )

        self.detail_purchase_count.set(
            str(
                summary["purchase_count"]
            )
        )

        self.detail_units.set(
            str(
                summary["total_units"]
            )
        )

        last_purchase = summary[
            "last_purchase"
        ]

        if last_purchase:

            self.detail_last_purchase.set(
                last_purchase.strftime(
                    "%d-%b-%Y %H:%M"
                )
            )

        else:

            self.detail_last_purchase.set(
                "--"
            )

    # ==========================================================
    # CLEAR SUPPLIER PROFILE
    # ==========================================================

    def clear_supplier_profile(self):

        self.detail_name.set("--")
        self.detail_phone.set("--")
        self.detail_email.set("--")
        self.detail_address.set("--")
        self.detail_total_spent.set("₹0.00")
        self.detail_purchase_count.set("0")
        self.detail_units.set("0")
        self.detail_last_purchase.set("--")
        for row in self.supplier_history_table.get_children():
            self.supplier_history_table.delete(row)

    # ==========================================================
    # LOAD SUPPLIER PURCHASE HISTORY
    # ==========================================================

    def load_supplier_purchase_history(self, supplier_id):

        for row in self.supplier_history_table.get_children():
            self.supplier_history_table.delete(row)

        history = get_supplier_purchase_history(
            supplier_id
        )

        for (
            purchase_id,
            product,
            quantity,
            purchase_price,
            total_cost,
            purchase_date
        ) in history:

            self.supplier_history_table.insert(
                "",
                "end",
                values=(
                    purchase_id,
                    product.title(),
                    quantity,
                    f"₹{float(purchase_price):,.2f}",
                    f"₹{float(total_cost):,.2f}",
                    purchase_date.strftime(
                        "%d-%b-%Y %H:%M"
                    )
                )
            )

    # ==========================================================
    # POPULATE SUPPLIER TABLE
    # ==========================================================

    def populate_supplier_table(self, suppliers):

        for row in self.table.get_children():
            self.table.delete(row)

        for supplier in suppliers:

            (
                supplier_id,
                name,
                phone,
                email,
                address,
                notes,
                created_at
            ) = supplier

            self.table.insert(
                "",
                "end",
                values=(
                    supplier_id,
                    name.title(),
                    phone or "",
                    email or "",
                    address or "",
                    notes or ""
                )
            )
    # ==========================================================
    # LOAD SUPPLIERS
    # ==========================================================

    def load_suppliers(self):

        suppliers = get_all_suppliers()

        self.populate_supplier_table(
            suppliers
        )

        self.supplier_count_label.configure(
            text=f"{len(suppliers)} Suppliers Registered"
        )

        self.search_var.set("")


    # ==========================================================
    # LIVE SEARCH
    # ==========================================================

    def live_search(self, event=None):

        keyword = self.search_var.get().strip()

        if keyword:
            suppliers = search_suppliers(
                keyword
            )
        else:
            suppliers = get_all_suppliers()

        self.populate_supplier_table(
            suppliers
        )

        self.supplier_count_label.configure(
            text=f"{len(suppliers)} Suppliers Found"
        )

    # ==========================================================
    # SUPPLIER FORM FIELD HELPER
    # ==========================================================

    def create_supplier_field(
        self,
        parent,
        label,
        variable,
        placeholder=""
    ):

        ctk.CTkLabel(
            parent,
            text=label,
            font=("Poppins", 13, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=20,
            pady=(8, 4)
        )

        entry = ctk.CTkEntry(
            parent,
            textvariable=variable,
            height=40,
            placeholder_text=placeholder
        )

        entry.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        return entry
    
    # ==========================================================
    # ADD SUPPLIER
    # ==========================================================

    def open_add_supplier_popup(self):

        popup = ctk.CTkToplevel(
            self
        )

        popup.title(
            "Add Supplier"
        )

        popup.geometry(
            "480x620"
        )

        popup.resizable(
            False,
            False
        )

        popup.grab_set()

        popup.configure(
            fg_color="white"
        )

        ctk.CTkLabel(
            popup,
            text="➕ Add Supplier",
            font=("Poppins", 24, "bold"),
            text_color="#065F46"
        ).pack(
            pady=(20, 15)
        )

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

        name_var = ctk.StringVar()
        phone_var = ctk.StringVar()
        email_var = ctk.StringVar()
        address_var = ctk.StringVar()

        name_entry = self.create_supplier_field(
            content,
            "Supplier Name *",
            name_var,
            "ABC Distributors"
        )

        self.create_supplier_field(
            content,
            "Phone",
            phone_var,
            "9876543210"
        )

        self.create_supplier_field(
            content,
            "Email",
            email_var,
            "supplier@example.com"
        )

        self.create_supplier_field(
            content,
            "Address",
            address_var,
            "Pune"
        )
        ctk.CTkLabel(
            content,
            text="Notes",
            font=("Poppins", 13, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=20,
            pady=(8, 4)
        )

        notes_entry = ctk.CTkTextbox(
            content,
            height=100
        )

        notes_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        status_label = ctk.CTkLabel(
            content,
            text=""
        )

        status_label.pack(
            pady=(0, 10)
        )

        # ======================================================
        # SAVE
        # ======================================================

        def save_supplier():

            name = name_var.get().strip()
            phone = phone_var.get().strip()
            email = email_var.get().strip()
            address = address_var.get().strip()

            notes = notes_entry.get(
                "1.0",
                "end"
            ).strip()

            if not name:

                status_label.configure(
                    text="Supplier name is required.",
                    text_color="red"
                )

                return

            try:

                add_supplier(
                    name,
                    phone,
                    email,
                    address,
                    notes
                )

            except Exception as error:

                status_label.configure(
                    text=str(error),
                    text_color="red"
                )

                return

            popup.destroy()

            self.load_suppliers()

            messagebox.showinfo(
                "Supplier Added",
                f"{name.title()} added successfully."
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

        ctk.CTkButton(
            button_frame,
            text="Save Supplier",
            height=42,
            fg_color="#16A34A",
            hover_color="#15803D",
            font=("Poppins", 13, "bold"),
            command=save_supplier
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
            command=popup.destroy
        ).pack(
            fill="x",
            pady=3
        )

        name_entry.focus_set()

    # ==========================================================
    # UPDATE SUPPLIER
    # ==========================================================

    def open_update_supplier_popup(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Supplier Selected",
                "Please select a supplier first."
            )

            return

        values = self.table.item(
            selected[0],
            "values"
        )

        supplier_id = int(
            values[0]
        )

        popup = ctk.CTkToplevel(
            self
        )

        popup.title(
            "Update Supplier"
        )

        popup.geometry(
            "480x620"
        )

        popup.resizable(
            False,
            False
        )

        popup.grab_set()

        popup.configure(
            fg_color="white"
        )

        ctk.CTkLabel(
            popup,
            text="✏ Update Supplier",
            font=("Poppins", 24, "bold"),
            text_color="#2563EB"
        ).pack(
            pady=(20, 15)
        )

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

        name_var = ctk.StringVar(
            value=values[1]
        )

        phone_var = ctk.StringVar(
            value=values[2]
        )

        email_var = ctk.StringVar(
            value=values[3]
        )

        address_var = ctk.StringVar(
            value=values[4]
        )


        name_entry = self.create_supplier_field(
            content,
            "Supplier Name *",
            name_var
        )

        self.create_supplier_field(
            content,
            "Phone",
            phone_var
        )

        self.create_supplier_field(
            content,
            "Email",
            email_var
        )

        self.create_supplier_field(
            content,
            "Address",
            address_var
        )

        ctk.CTkLabel(
            content,
            text="Notes",
            font=("Poppins", 13, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=20,
            pady=(8, 4)
        )

        notes_entry = ctk.CTkTextbox(
            content,
            height=100
        )

        notes_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        notes_entry.insert(
            "1.0",
            values[5]
        )

        status_label = ctk.CTkLabel(
            content,
            text=""
        )

        status_label.pack(
            pady=(0, 10)
        )

        def save_update():

            name = name_var.get().strip()
            phone = phone_var.get().strip()
            email = email_var.get().strip()
            address = address_var.get().strip()

            notes = notes_entry.get(
                "1.0",
                "end"
            ).strip()

            if not name:

                status_label.configure(
                    text="Supplier name is required.",
                    text_color="red"
                )

                return

            try:

                update_supplier(
                    supplier_id,
                    name,
                    phone,
                    email,
                    address,
                    notes
                )

            except Exception as error:

                status_label.configure(
                    text=str(error),
                    text_color="red"
                )

                return

            popup.destroy()

            self.load_suppliers()

            messagebox.showinfo(
                "Supplier Updated",
                "Supplier updated successfully."
            )

        button_frame = ctk.CTkFrame(
            popup,
            fg_color="white"
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        ctk.CTkButton(
            button_frame,
            text="Save Changes",
            height=42,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=("Poppins", 13, "bold"),
            command=save_update
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
            command=popup.destroy
        ).pack(
            fill="x",
            pady=3
        )

        name_entry.focus_set()

    # ==========================================================
    # DELETE SUPPLIER
    # ==========================================================

    def remove_supplier(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Supplier Selected",
                "Please select a supplier first."
            )

            return

        values = self.table.item(
            selected[0],
            "values"
        )

        supplier_id = int(
            values[0]
        )

        supplier_name = str(
            values[1]
        )

        confirm = messagebox.askyesno(
            "Delete Supplier",
            f"Delete supplier '{supplier_name}'?",
        )

        if not confirm:
            return

        try:

            delete_supplier(
                supplier_id
            )

        except Exception as error:

            messagebox.showerror(
                "Cannot Delete Supplier",
                str(error)
            )

            return

        self.load_suppliers()

        messagebox.showinfo(
            "Supplier Deleted",
            f"{supplier_name} deleted successfully."
        )