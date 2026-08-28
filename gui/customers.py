import customtkinter as ctk
from tkinter import ttk, messagebox
from backend import (
    get_all_customers,
    search_customers,
    add_customer,
    update_customer,
    delete_customer,
    get_customer_summary,
    get_customer_purchase_history
)


class CustomersPage(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#F9FAFB",corner_radius=0)

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

        # ==========================================================
        # MAIN CONTENT (TABLE + PROFILE)
        # ==========================================================

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # Customer table (60%)
        main_frame.grid_columnconfigure(0, weight=6)

        # Profile panel (40%)
        main_frame.grid_columnconfigure(1, weight=4, minsize=360)

        main_frame.grid_rowconfigure(0, weight=1)

        # Left Side → Customer Table
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.grid(row=0, column=0, sticky="nsew", padx=(0,15))

        columns = (
            "ID",
            "Name",
            "Phone",
            "Email",
            "Address",
            "Points"
        )

        # ==========================================================
        # CUSTOMER TABLE
        # ==========================================================

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=17
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
            width=140,
            stretch=False
        )

        self.table.column(
            "Email",
            width=220,
            stretch=False
        )

        self.table.column(
            "Address",
            width=260,
            stretch=False
        )

        self.table.column(
            "Points",
            width=90,
            anchor="center",
            stretch=False
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.load_customer_profile
        )

        # ----------------------------------------------------------
        # Configure table container
        # ----------------------------------------------------------

        table_frame.grid_rowconfigure(
            0,
            weight=1
        )

        table_frame.grid_rowconfigure(
            1,
            weight=0
        )

        table_frame.grid_columnconfigure(
            0,
            weight=1
        )

        table_frame.grid_columnconfigure(
            1,
            weight=0
        )

        # ----------------------------------------------------------
        # Scrollbars
        # ----------------------------------------------------------

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.table.xview
        )

        self.table.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        # ----------------------------------------------------------
        # Place table + scrollbars
        # ----------------------------------------------------------

        self.table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )
        # ==========================================================
        # CUSTOMER PROFILE PANEL
        # ==========================================================

        profile_frame = ctk.CTkFrame(
            main_frame,
            fg_color="white",
            corner_radius=18,
            border_width=1,
            border_color="#D1D5DB"
        )

        profile_frame.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(
            profile_frame,
            text="Customer Profile",
            font=("Poppins",20,"bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=20, pady=(20,15))

        # Variables
        self.profile_name = ctk.StringVar(value="--")
        self.profile_phone = ctk.StringVar(value="--")
        self.profile_points = ctk.StringVar(value="0")
        self.profile_orders = ctk.StringVar(value="0")
        self.profile_spent = ctk.StringVar(value="₹0.00")
        self.profile_last_purchase = ctk.StringVar(value="--")


        def profile_row(title, variable):

            row = ctk.CTkFrame(profile_frame, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=8)

            ctk.CTkLabel(
                row,
                text=title,
                font=("Poppins",13)
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                textvariable=variable,
                font=("Poppins",13,"bold"),
                text_color="#065F46"
            ).pack(side="right")


        profile_row("Name", self.profile_name)
        profile_row("Phone", self.profile_phone)
        profile_row("Loyalty Points ⭐", self.profile_points)
        profile_row("Total Orders", self.profile_orders)
        profile_row("Total Spent", self.profile_spent)
        profile_row("Last Purchase", self.profile_last_purchase)

        ctk.CTkLabel(
            profile_frame,
            text="Purchase History",
            font=("Poppins",18,"bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=20, pady=(25,10))

        history_frame = ctk.CTkFrame(profile_frame)
        history_frame.pack(fill="both", expand=True, padx=15, pady=(0,15))

        columns = ("Sale ID","Date","Payment","Total")

        self.history_table = ttk.Treeview(
            history_frame,
            columns=columns,
            show="headings",
            height=10
        )

        for col in columns:
            self.history_table.heading(col, text=col)

        self.history_table.column(
            "Sale ID",
            width=55,
            anchor="center",
            stretch=False
        )

        self.history_table.column(
            "Date",
            width=95,
            anchor="center",
            stretch=True
        )

        self.history_table.column(
            "Payment",
            width=75,
            anchor="center",
            stretch=True
        )

        self.history_table.column(
            "Total",
            width=90,
            anchor="e",
            stretch=True
        )
        history_style = ttk.Style()

        history_style.configure(
            "History.Treeview",
            rowheight=24,
            font=("Poppins", 11)
        )

        history_style.configure(
            "History.Treeview.Heading",
            font=("Poppins", 11, "bold")
        )

        self.history_table.configure(style="History.Treeview")
        
        history_scroll = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history_table.yview
        )

        self.history_table.configure(yscrollcommand=history_scroll.set)

        self.history_table.pack(side="left", fill="both", expand=True)
        history_scroll.pack(side="right", fill="y")

    def populate_customer_table(self, customers):

        for row in self.table.get_children():
            self.table.delete(row)

        for customer in customers:
            self.table.insert(
                "",
                "end",
                values=customer
            )
    # ==========================================================
    # LOAD CUSTOMERS
    # ==========================================================

    def load_customers(self):

        customers = get_all_customers()

        self.populate_customer_table(
            customers
        )

        self.customer_count_label.configure(
            text=f"{len(customers)} Customers Registered"
        )

        self.search_var.set("")

    # ==========================================================
    # LIVE SEARCH
    # ==========================================================

    def live_search(self, event=None):

        keyword = self.search_var.get().strip()

        if keyword:
            customers = search_customers(keyword)
        else:
            customers = get_all_customers()

        self.populate_customer_table(
            customers
        )

        self.customer_count_label.configure(
            text=f"{len(customers)} Customers Found"
        )

        # ==========================================================
        # LOAD CUSTOMER PROFILE
        # ==========================================================

    def load_customer_profile(self, event=None):

        selected = self.table.selection()

        if not selected:
            return

        customer_id = self.table.item(selected[0])["values"][0]

        summary = get_customer_summary(customer_id)
        history = get_customer_purchase_history(customer_id)

        # ---------- Summary ----------
        self.profile_name.set(summary["name"])
        self.profile_phone.set(summary["phone"])
        self.profile_points.set(str(summary["loyalty_points"]))
        self.profile_orders.set(str(summary["total_orders"]))
        self.profile_spent.set(f"₹{float(summary['total_spent']):.2f}")

        if summary["last_purchase"]:
            self.profile_last_purchase.set(
                summary["last_purchase"].strftime("%d %b %Y")
            )
        else:
            self.profile_last_purchase.set("No Purchases")

        # ---------- Purchase History ----------
        for row in self.history_table.get_children():
            self.history_table.delete(row)

        for sale in history:

            sale_id, sale_date, payment, discount, gst, total = sale
            self.history_table.insert(
                "",
                "end",
                values=(
                    sale_id,
                    sale_date.strftime("%d-%m-%Y"),
                    payment,
                    f"₹{float(total):.2f}"
                )
            )

    def create_customer_field(
        self,
        parent,
        title,
        variable
    ):

        ctk.CTkLabel(
            parent,
            text=title,
            font=("Poppins", 13, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(8, 3)
        )

        entry = ctk.CTkEntry(
            parent,
            textvariable=variable,
            width=420,
            height=38
        )

        entry.pack()

        return entry

    
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


        self.create_customer_field(
            popup,
            "Customer Name",
            name_var
        )

        self.create_customer_field(
            popup,
            "Phone Number",
            phone_var
        )

        self.create_customer_field(
            popup,
            "Email",
            email_var
        )

        self.create_customer_field(
            popup,
            "Address",
            address_var
        )

        status = ctk.CTkLabel(
            popup,
            text="",
            font=("Poppins",12)
        )
        status.pack(pady=8)

        def save_customer():

            name = name_var.get().strip()
            phone = phone_var.get().strip()
            email = email_var.get().strip()
            address = address_var.get().strip()

            if not name or not phone:

                status.configure(
                    text="Name and Phone are required.",
                    text_color="red"
                )

                return

            if not phone.isdigit() or len(phone) != 10:

                status.configure(
                    text="Phone number must contain 10 digits.",
                    text_color="red"
                )

                return

            try:

                add_customer(
                    name,
                    phone,
                    email,
                    address
                )

            except Exception as error:

                status.configure(
                    text=f"Unable to save customer: {error}",
                    text_color="red"
                )

                return

            popup.destroy()
            self.load_customers()
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

            messagebox.showwarning(
                "No Customer Selected",
                "Please select a customer first."
            )

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

        self.create_customer_field(
            popup,
            "Customer Name",
            name_var
        )

        self.create_customer_field(
            popup,
            "Phone Number",
            phone_var
        )

        self.create_customer_field(
            popup,
            "Email",
            email_var
        )

        self.create_customer_field(
            popup,
            "Address",
            address_var
        )

        def save_update():

            name = name_var.get().strip()
            phone = phone_var.get().strip()
            email = email_var.get().strip()
            address = address_var.get().strip()

            if not name or not phone:

                messagebox.showwarning(
                    "Invalid Customer",
                    "Name and Phone are required.",
                    parent=popup
                )

                return

            if not phone.isdigit() or len(phone) != 10:

                messagebox.showwarning(
                    "Invalid Phone",
                    "Phone number must contain 10 digits.",
                    parent=popup
                )

                return

            try:

                update_customer(
                    customer_id,
                    name,
                    phone,
                    email,
                    address
                )

            except Exception as error:

                messagebox.showerror(
                    "Update Failed",
                    f"Unable to update customer.\n\n{error}",
                    parent=popup
                )

                return

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

            messagebox.showwarning(
                "No Customer Selected",
                "Please select a customer first."
            )

            return

        values = self.table.item(
            selected[0],
            "values"
        )

        confirm = messagebox.askyesno(
            "Delete Customer",
            f"Delete customer '{values[1]}'?"
        )

        if not confirm:
            return

        try:

            delete_customer(
                values[0]
            )

        except Exception as error:

            messagebox.showerror(
                "Delete Failed",
                f"Unable to delete customer.\n\n{error}"
            )

            return

        self.load_customers()

        messagebox.showinfo(
            "Customer Deleted",
            f"Customer '{values[1]}' deleted successfully."
        )