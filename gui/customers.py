import customtkinter as ctk
from tkinter import ttk, messagebox
from backend import (
    get_all_customers,
    search_customers,
    add_customer,
    update_customer,
    delete_customer
)


class CustomersPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#F9FAFB")

        self.build_ui()
        self.load_customers()

    # ==========================================================
    # BUILD UI
    # ==========================================================

    def build_ui(self):

        # Page Title
        ctk.CTkLabel(
            self,
            text="Customers",
            font=("Poppins", 28, "bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=30, pady=(20, 5))

        self.customer_count_label = ctk.CTkLabel(
            self,
            text="0 Customers Registered",
            font=("Poppins", 13),
            text_color="gray40"
        )

        self.customer_count_label.pack(anchor="w", padx=30)

        # ================= Search Bar =================

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=30, pady=15)

        self.search_var = ctk.StringVar()

        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search customer by name or phone...",
            width=320,
            height=38
        )

        self.search_entry.pack(side="left")

        self.search_entry.bind("<KeyRelease>", self.live_search)

        self.refresh_button = ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=90,
            command=self.load_customers
        )

        self.refresh_button.pack(side="left", padx=10)

        # Update Button
        self.update_button = ctk.CTkButton(
            search_frame,
            text="✏ Update",
            width=110,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.open_update_customer_popup
        )
        self.update_button.pack(side="right", padx=10)

        # Add Button
        self.add_button = ctk.CTkButton(
            search_frame,
            text="+ Add Customer",
            width=140,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.open_add_customer_popup
        )
        self.add_button.pack(side="right")

        # Delete Button
        self.delete_button = ctk.CTkButton(
            search_frame,
            text="🗑 Delete",
            width=110,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.remove_customer
        )
        self.delete_button.pack(side="right", padx=10)

        # ================= Customer Table =================

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)

        columns = (
            "ID",
            "Name",
            "Phone",
            "Email",
            "Address",
            "Points"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=17
        )

        for column in columns:
            self.table.heading(column, text=column)

        self.table.column("ID", width=60, anchor="center")
        self.table.column("Name", width=170)
        self.table.column("Phone", width=140)
        self.table.column("Email", width=220)
        self.table.column("Address", width=260)
        self.table.column("Points", width=90, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Table Style
        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            rowheight=34,
            font=("Poppins", 12),
            background="white",
            fieldbackground="white"
        )

        style.configure(
            "Treeview.Heading",
            font=("Poppins", 12, "bold"),
            background="#065F46",
            foreground="white"
        )

    # ==========================================================
    # LOAD CUSTOMERS
    # ==========================================================

    def load_customers(self):

        for row in self.table.get_children():
            self.table.delete(row)

        customers = get_all_customers()

        for customer in customers:
            self.table.insert("", "end", values=customer)

        self.customer_count_label.configure(
            text=f"{len(customers)} Customers Registered"
        )

        self.search_var.set("")

    # ==========================================================
    # LIVE SEARCH
    # ==========================================================

    def live_search(self, event=None):

        keyword = self.search_var.get().strip()

        for row in self.table.get_children():
            self.table.delete(row)

        if keyword == "":
            customers = get_all_customers()
        else:
            customers = search_customers(keyword)

        for customer in customers:
            self.table.insert("", "end", values=customer)

        self.customer_count_label.configure(
            text=f"{len(customers)} Customers Found"
        )

    # ==========================================================
    # ADD CUSTOMER POPUP
    # ==========================================================

    def open_add_customer_popup(self):

        popup = ctk.CTkToplevel(self)
        popup.title("Add Customer")
        popup.geometry("480x480")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text="Add Customer",
            font=("Poppins",24,"bold"),
            text_color="#065F46"
        ).pack(pady=20)

        name_var = ctk.StringVar()
        phone_var = ctk.StringVar()
        email_var = ctk.StringVar()
        address_var = ctk.StringVar()

        def field(title, variable):

            ctk.CTkLabel(
                popup,
                text=title,
                font=("Poppins",13,"bold")
            ).pack(anchor="w", padx=30, pady=(8,3))

            entry = ctk.CTkEntry(
                popup,
                textvariable=variable,
                width=420,
                height=38
            )

            entry.pack()

        field("Customer Name", name_var)
        field("Phone Number", phone_var)
        field("Email", email_var)
        field("Address", address_var)

        status = ctk.CTkLabel(
            popup,
            text="",
            font=("Poppins",12)
        )
        status.pack(pady=8)

        def save_customer():

            if name_var.get()=="" or phone_var.get()=="":
                status.configure(
                    text="Name and Phone are required.",
                    text_color="red"
                )
                return

            if len(phone_var.get()) != 10:
                status.configure(
                    text="Phone number must contain 10 digits.",
                    text_color="red"
                )
                return

            try:
                add_customer(
                    name_var.get().strip(),
                    phone_var.get().strip(),
                    email_var.get().strip(),
                    address_var.get().strip()
                )

                popup.destroy()
                self.load_customers()

            except Exception:
                status.configure(
                    text="Phone number already exists.",
                    text_color="red"
                )

        ctk.CTkButton(
            popup,
            text="Save Customer",
            height=42,
            width=420,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=save_customer
        ).pack(pady=15)

    # ==========================================================
    # UPDATE CUSTOMER POPUP
    # ==========================================================

    def open_update_customer_popup(self):

        selected = self.table.selection()

        if not selected:
            return

        values = self.table.item(selected[0])["values"]

        customer_id = values[0]

        popup = ctk.CTkToplevel(self)
        popup.title("Update Customer")
        popup.geometry("480x480")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text="Update Customer",
            font=("Poppins",24,"bold"),
            text_color="#2563EB"
        ).pack(pady=20)

        name_var = ctk.StringVar(value=values[1])
        phone_var = ctk.StringVar(value=values[2])
        email_var = ctk.StringVar(value=values[3])
        address_var = ctk.StringVar(value=values[4])

        def field(title, variable):

            ctk.CTkLabel(
                popup,
                text=title,
                font=("Poppins",13,"bold")
            ).pack(anchor="w", padx=30, pady=(8,3))

            entry = ctk.CTkEntry(
                popup,
                textvariable=variable,
                width=420,
                height=38
            )
            entry.pack()

        field("Customer Name", name_var)
        field("Phone Number", phone_var)
        field("Email", email_var)
        field("Address", address_var)

        def save_update():

            update_customer(
                customer_id,
                name_var.get(),
                phone_var.get(),
                email_var.get(),
                address_var.get()
            )

            popup.destroy()
            self.load_customers()

        ctk.CTkButton(
            popup,
            text="Update Customer",
            height=42,
            width=420,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=save_update
        ).pack(pady=20)

    # ==========================================================
    # DELETE CUSTOMER
    # ==========================================================

    def remove_customer(self):

        selected = self.table.selection()

        if not selected:
            return

        values = self.table.item(selected[0])["values"]

        confirm = messagebox.askyesno(
            "Delete Customer",
            f"Delete customer '{values[1]}'?"
        )

        if not confirm:
            return

        delete_customer(values[0])

        self.load_customers()