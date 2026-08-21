import customtkinter as ctk
from PIL import Image
from gui.products import ProductsPage
from gui.billing import BillingPage
from gui.customers import CustomersPage
# -----------------------------
# Theme Configuration
# -----------------------------
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")


class ShingviSupermartApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # -----------------------------
        # WINDOW SETTINGS
        # -----------------------------
        self.title("Shingvi Supermart - Inventory Management System")
        self.geometry("1280x720")
        self.minsize(1100, 650)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # -----------------------------
        # SIDEBAR
        # -----------------------------
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            fg_color="#065F46",
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(10, weight=1)

        # -----------------------------
        # LOGO
        # -----------------------------
        self.logo_image = ctk.CTkImage(
            light_image=Image.open("assets/logo.png"),
            dark_image=Image.open("assets/logo.png"),
            size=(90, 90)
        )

        ctk.CTkLabel(
            self.sidebar,
            image=self.logo_image,
            text=""
        ).grid(row=0, column=0, pady=(25, 10))

        # -----------------------------
        # BUSINESS NAME
        # -----------------------------
        ctk.CTkLabel(
            self.sidebar,
            text="SHINGVI\nSUPERMART",
            font=("Poppins", 24, "bold"),
            text_color="white",
            justify="center"
        ).grid(row=1, column=0)

        ctk.CTkLabel(
            self.sidebar,
            text="Inventory Management",
            font=("Poppins", 13),
            text_color="#BBF7D0"
        ).grid(row=2, column=0, pady=(0, 25))

        # -----------------------------
        # NAVIGATION BUTTONS
        # -----------------------------
        self.dashboard_btn = self.create_sidebar_button(
            "🏠 Dashboard", 3, self.show_dashboard
        )

        self.products_btn = self.create_sidebar_button(
            "📦 Products", 4, self.show_products
        )

        self.billing_btn = self.create_sidebar_button(
            "🛒 Billing", 5, None
        )
        self.billing_btn.configure(command=self.show_billing)


        self.customers_btn = self.create_sidebar_button(
            "👤 Customers", 6, None
        )
        self.customers_btn.configure(command=self.show_customers)

        self.reports_btn = self.create_sidebar_button(
            "📊 Reports", 7, None
        )

        # -----------------------------
        # THEME SWITCHER
        # -----------------------------
        self.theme_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Light", "Dark", "System"],
            width=170,
            command=self.change_theme
        )

        self.theme_menu.grid(row=9, column=0, pady=20)
        self.theme_menu.set("Light")

        # Version Label
        ctk.CTkLabel(
            self.sidebar,
            text="Version 2.0 • CustomTkinter",
            font=("Poppins", 11),
            text_color="#A7F3D0"
        ).grid(row=10, column=0, pady=(0, 15))

        # -----------------------------
        # CONTENT AREA
        # -----------------------------
        self.content = ctk.CTkFrame(
            self,
            fg_color="#F9FAFB",
            corner_radius=0
        )
        self.content.grid(row=0, column=1, sticky="nsew")

        # -----------------------------
        # CREATE PAGES
        # -----------------------------
        self.dashboard_page = self.create_dashboard_page()

        self.products_page = ProductsPage(self.content)
        # Hide products initially
        self.products_page.pack_forget()


        self.billing_page = BillingPage(self.content)
        self.billing_page.pack_forget()

        self.customers_page = CustomersPage(self.content)
        self.customers_page.pack_forget()

        # Show Dashboard First
        self.show_dashboard()

    # ==========================================================
    # SIDEBAR BUTTON
    # ==========================================================
    def create_sidebar_button(self, text, row, command):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            width=180,
            height=42,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#059669",
            text_color="white",
            anchor="w",
            font=("Poppins", 14, "bold"),
            command=command
        )

        button.grid(row=row, column=0, padx=18, pady=6)

        return button

    # ==========================================================
    # DASHBOARD PAGE
    # ==========================================================
    def create_dashboard_page(self):

        page = ctk.CTkFrame(
            self.content,
            fg_color="#F9FAFB",
            corner_radius=0
        )

        page.grid_columnconfigure(0, weight=1)
        page.grid_columnconfigure(1, weight=1)
        page.grid_rowconfigure(4, weight=1)

        # Title
        ctk.CTkLabel(
            page,
            text="Dashboard",
            font=("Poppins", 30, "bold"),
            text_color="#065F46"
        ).grid(row=0, column=0, columnspan=2,
               padx=30, pady=(25, 5), sticky="w")

        # Welcome
        ctk.CTkLabel(
            page,
            text="Welcome back, Jinesh 👋\nManage your Shingvi Supermart efficiently.",
            font=("Poppins", 15),
            justify="left",
            text_color="gray40"
        ).grid(row=1, column=0, columnspan=2,
               padx=30, pady=(0, 20), sticky="w")

        # Dashboard Cards
        self.create_dashboard_card(page, "Today's Revenue", "₹0.00", 2, 0)
        self.create_dashboard_card(page, "Today's Sales", "0", 2, 1)

        self.create_dashboard_card(page, "Products", "0", 3, 0)
        self.create_dashboard_card(page, "Low Stock", "0", 3, 1)

        return page

    # ==========================================================
    # DASHBOARD CARD
    # ==========================================================
    def create_dashboard_card(self, parent, title, value, row, column):

        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=18,
            border_width=1,
            border_color="#D1D5DB",
            height=135
        )

        card.grid(
            row=row,
            column=column,
            padx=20,
            pady=15,
            sticky="nsew"
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Poppins", 14),
            text_color="#64748B"
        ).pack(anchor="w", padx=18, pady=(18, 6))

        ctk.CTkLabel(
            card,
            text=value,
            font=("Poppins", 30, "bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=18)

    # ==========================================================
    # PAGE NAVIGATION
    # ==========================================================
    def hide_all_pages(self):
        self.dashboard_page.pack_forget()
        self.products_page.pack_forget()
        self.billing_page.pack_forget()
        self.customers_page.pack_forget()

    def highlight_button(self, active_button):
        buttons = [
            self.dashboard_btn,
            self.products_btn,
            self.billing_btn,
            self.customers_btn,
            self.reports_btn
        ]

        for button in buttons:
            button.configure(fg_color="transparent")

        active_button.configure(fg_color="#047857")

    def show_dashboard(self):

        self.hide_all_pages()

        self.dashboard_page.pack(fill="both", expand=True)

        self.highlight_button(self.dashboard_btn)

    def show_products(self):

        self.hide_all_pages()

        self.products_page.pack(fill="both", expand=True)

        self.products_page.load_products()

        self.highlight_button(self.products_btn)

    def show_billing(self):

        self.hide_all_pages()

        self.billing_page.pack(fill="both", expand=True)

    def show_customers(self):

        self.hide_all_pages()

        self.customers_page.pack(fill="both", expand=True)

        self.customers_page.load_customers()

    # ==========================================================
    # THEME
    # ==========================================================
    def change_theme(self, mode):
        ctk.set_appearance_mode(mode)


# ==========================================================
# RUN APP
# ==========================================================
if __name__ == "__main__":
    app = ShingviSupermartApp()
    app.mainloop()