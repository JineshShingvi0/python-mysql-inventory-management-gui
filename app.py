import customtkinter as ctk
from PIL import Image
from tkinter import ttk
from gui.products import ProductsPage
from gui.billing import BillingPage
from gui.customers import CustomersPage
from datetime import datetime
from gui.reports import ReportsPage

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from backend import (
    get_today_revenue,
    get_today_orders,
    get_inventory_value,
    get_low_stock_products,
    get_recent_sales,
    get_dashboard_inventory_alerts,
    get_weekly_sales,
    get_dashboard_insights,
    get_dashboard_top_products
)


# -----------------------------
# Theme Configuration
# -----------------------------
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")


class ShingviSupermartApp(ctk.CTk):

    def __init__(self):
        super().__init__()


        self.dashboard_revenue_var = ctk.StringVar(value="₹0")
        self.dashboard_orders_var = ctk.StringVar(value="0")
        self.dashboard_inventory_var = ctk.StringVar(value="₹0")
        self.dashboard_profit_var = ctk.StringVar(value="₹0")
        self.dashboard_healthy_var = ctk.StringVar(value="0")
        self.dashboard_low_var = ctk.StringVar(value="0")
        self.dashboard_out_var = ctk.StringVar(value="0")
        self.dashboard_health_var = ctk.StringVar(value="100%")
        self.dashboard_greeting_var = ctk.StringVar()
        self.notification_count_var = ctk.StringVar(value="0")

        self.snapshot_gst_var = ctk.StringVar(value="₹0")
        self.snapshot_discount_var = ctk.StringVar(value="₹0")
        self.snapshot_customer_var = ctk.StringVar(value="0")
        self.snapshot_loyalty_var = ctk.StringVar(value="0")

        # ==========================================
        # Smooth Mouse Wheel Scrolling
        # ==========================================
        
        self.bind_all("<MouseWheel>", self._smooth_scroll)      # Windows
        self.bind_all("<Button-4>", self._smooth_scroll)        # Linux Scroll Up
        self.bind_all("<Button-5>", self._smooth_scroll)        # Linux Scroll Down
        # -----------------------------
        # WINDOW SETTINGS
        # -----------------------------
        self.title("Shingvi Supermart - Inventory Management System")
        self.geometry("1280x720")
        self.minsize(1100, 650)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================================
        # GLOBAL TREEVIEW STYLE (Professional Tables)
        # ==========================================================

        style = ttk.Style()

        style.theme_use("default")

        # Main table style
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#111827",
            fieldbackground="#FFFFFF",
            rowheight=34,
            borderwidth=0,
            font=("Poppins", 12)
        )

        # Table headings
        style.configure(
            "Treeview.Heading",
            background="#065F46",
            foreground="white",
            font=("Poppins", 13, "bold"),
            relief="flat",
            padding=8
        )

        style.map(
            "Treeview.Heading",
            background=[("active", "#047857")]
        )

        # Selected row style
        style.map(
            "Treeview",
            background=[("selected", "#16A34A")],
            foreground=[("selected", "white")]
        )

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
        self.reports_btn.configure(command=self.show_reports)

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



        self.dashboard_date_var = ctk.StringVar()
        self.dashboard_time_var = ctk.StringVar()



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

        self.reports_page = ReportsPage(self.content)
        self.reports_page.pack_forget()

        # Show Dashboard First
        self.show_dashboard()
        self.update_dashboard_clock()

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

        page = ctk.CTkScrollableFrame(
            self.content,
            fg_color="#F9FAFB",
            corner_radius=0
        )
        page.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=0)
        page.grid_columnconfigure(0, weight=1)
        page.grid_columnconfigure(1, weight=1)
        page.grid_rowconfigure(4, weight=1)

        # =====================================================
        # PREMIUM DASHBOARD HEADER
        # =====================================================

        header = ctk.CTkFrame(
            page,
            fg_color="#ECFDF5",
            corner_radius=20,
            border_width=1,
            border_color="#BBF7D0"
        )

        header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=30,
            pady=(25,20)
        )

        header.grid_columnconfigure(0, weight=1)

        # Left
        left = ctk.CTkFrame(header, fg_color="transparent")
        left.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        ctk.CTkLabel(
            left,
            textvariable=self.dashboard_greeting_var,
            font=("Poppins",15)
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Jinesh",
            font=("Poppins",32,"bold"),
            text_color="#065F46"
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Shingvi Supermart Business Dashboard",
            font=("Poppins",14),
            text_color="gray40"
        ).pack(anchor="w")

        # Right
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.grid(row=0, column=1, padx=20)

        ctk.CTkLabel(
            right,
            textvariable=self.dashboard_date_var,
            font=("Poppins",13,"bold")
        ).pack(anchor="e")

        ctk.CTkLabel(
            right,
            textvariable=self.dashboard_time_var,
            font=("Poppins",24,"bold"),
            text_color="#16A34A"
        ).pack(anchor="e")

        status = ctk.CTkLabel(
            right,
            text="🟢 Store Status : OPEN",
            font=("Poppins",12,"bold"),
            text_color="#15803D",
            fg_color="#DCFCE7",
            corner_radius=15,
            padx=12,
            pady=5
        )
        status.pack(anchor="e", pady=(10,0))
        # Dashboard Cards
        self.create_dashboard_card(
            page,
            "💰 Today's Revenue",
            self.dashboard_revenue_var,
            3,
            0,
            "#DCFCE7"
        )

        self.create_dashboard_card(
            page,
            "🛒 Orders Today",
            self.dashboard_orders_var,
            3,
            1,
            "#DBEAFE"
        )

        self.create_dashboard_card(
            page,
            "📦 Inventory Value",
            self.dashboard_inventory_var,
            4,
            0,
            "#FEF3C7"
        )

        self.create_dashboard_card(
            page,
            "📈 Expected Profit",
            self.dashboard_profit_var,
            4,
            1,
            "#F3E8FF"
        )

        notification = ctk.CTkFrame(
            right,
            fg_color="#F9FAFB",
            corner_radius=15
        )
        notification.pack(anchor="e", pady=(12,0))

        ctk.CTkLabel(
            notification,
            text="🔔 Notifications",
            font=("Poppins",11,"bold"),
            text_color="#374151"
        ).pack(side="left", padx=(10,5), pady=6)

        badge = ctk.CTkLabel(
            notification,
            textvariable=self.notification_count_var,
            fg_color="#DC2626",
            text_color="white",
            width=24,
            height=24,
            corner_radius=12,
            font=("Poppins",11,"bold")
        )

        badge.pack(side="right", padx=(0,8), pady=6)
        # =====================================================
        # BUSINESS SNAPSHOT STRIP
        # =====================================================

        snapshot = ctk.CTkFrame(
            page,
            fg_color="#FFFFFF",
            corner_radius=18,
            border_width=1,
            border_color="#E5E7EB"
        )

        snapshot.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=30,
            pady=(0,18)
        )

        snapshot.grid_columnconfigure((0,1,2,3,4), weight=1)

        items = [
            ("💰 Revenue", self.dashboard_revenue_var, "#16A34A"),
            ("🧾 GST", self.snapshot_gst_var, "#2563EB"),
            ("🏷 Discount", self.snapshot_discount_var, "#EA580C"),
            ("👤 New Customers", self.snapshot_customer_var, "#9333EA"),
            ("⭐ Loyalty", self.snapshot_loyalty_var, "#CA8A04")
        ]

        for i, (title, variable, color) in enumerate(items):

            box = ctk.CTkFrame(snapshot, fg_color="transparent")
            box.grid(row=0, column=i, padx=8, pady=14)

            ctk.CTkLabel(
                box,
                text=title,
                font=("Poppins",11),
                text_color="gray50"
            ).pack()

            ctk.CTkLabel(
                box,
                textvariable=variable,
                font=("Poppins",17,"bold"),
                text_color=color
            ).pack(pady=(2,0))

        # =====================================================
        # SALES TARGET CARD
        # =====================================================

        target_frame = ctk.CTkFrame(
            page,
            fg_color="white",
            corner_radius=20,
            border_width=1,
            border_color="#E5E7EB"
        )

        target_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=30,
            pady=(0,20)
        )

        top = ctk.CTkFrame(target_frame, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(15,10))

        ctk.CTkLabel(
            top,
            text="🎯 Today's Sales Target",
            font=("Poppins",18,"bold"),
            text_color="#065F46"
        ).pack(side="left")

        self.sales_target_var = ctk.StringVar(value="0%")
        self.sales_remaining_var = ctk.StringVar(value="₹0 Remaining")

        ctk.CTkLabel(
            target_frame,
            textvariable=self.sales_target_var,
            font=("Poppins",34,"bold"),
            text_color="#16A34A"
        ).pack()

        self.sales_progress = ctk.CTkProgressBar(
            target_frame,
            height=18
        )

        self.sales_progress.pack(fill="x", padx=25, pady=10)

        ctk.CTkLabel(
            target_frame,
            textvariable=self.sales_remaining_var,
            font=("Poppins",12),
            text_color="gray45"
        ).pack(pady=(0,15))
        
        # =====================================================
        # QUICK ACTION CENTER
        # =====================================================

        action_frame = ctk.CTkFrame(
            page,
            fg_color="transparent"
        )

        action_frame.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=(10,20)
        )

        ctk.CTkLabel(
            action_frame,
            text="⚡ Quick Actions",
            font=("Poppins",22,"bold"),
            text_color="#064E3B"
        ).pack(anchor="w", pady=(0,10))

        buttons = ctk.CTkFrame(action_frame, fg_color="transparent")
        buttons.pack(fill="x")

        buttons.grid_columnconfigure((0,1,2,3), weight=1)

        actions = [
            ("🛒","New Bill","Create Invoice Instantly","#DCFCE7",self.show_billing),
            ("📦","Products","Add New Inventory","#DBEAFE",self.show_products),
            ("👤","Customers","Manage Loyalty","#FEF3C7",self.show_customers),
            ("📊","Reports","View Analytics","#F3E8FF",self.show_reports)
        ]

        for i, (icon,title,subtitle,bg,command) in enumerate(actions):

            card = ctk.CTkFrame(
                buttons,
                fg_color=bg,
                corner_radius=20,
                border_width=1,
                border_color="#E5E7EB",
                cursor="hand2"
            )

            card.grid(row=0,column=i,padx=10,sticky="nsew")

            ctk.CTkLabel(
                card,
                text=icon,
                font=("Poppins",28)
            ).pack(anchor="w", padx=18, pady=(16,8))

            ctk.CTkLabel(
                card,
                text=title,
                font=("Poppins",15,"bold"),
                text_color="#065F46"
            ).pack(anchor="w", padx=18)

            ctk.CTkLabel(
                card,
                text=subtitle,
                font=("Poppins",11),
                text_color="gray45"
            ).pack(anchor="w", padx=18, pady=(0,15))

            card.bind("<Button-1>", lambda e, cmd=command: cmd())

    # =====================================================
    # RECENT SALES SECTION
    # =====================================================

        recent_frame = ctk.CTkFrame(
            page,
            fg_color="white",
            corner_radius=20,
            border_width=1,
            border_color="#E5E7EB"
        )

        recent_frame.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=20,
            pady=(25,20)
        )

        # Header
        top = ctk.CTkFrame(recent_frame, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(18,10))

        ctk.CTkLabel(
            top,
            text="🧾 Recent Sales",
            font=("Poppins",18,"bold"),
            text_color="#065F46"
        ).pack(side="left")

        badge = ctk.CTkLabel(
            top,
            text="LIVE",
            fg_color="#DCFCE7",
            text_color="#15803D",
            corner_radius=15,
            padx=10,
            pady=4,
            font=("Poppins",10,"bold")
        )
        badge.pack(side="right")

        # Table
        columns = ("Invoice","Customer","Payment","Total")

        self.dashboard_sales_table = ttk.Treeview(
            recent_frame,
            columns=columns,
            show="headings",
            height=5
        )

        for col in columns:
            self.dashboard_sales_table.heading(col, text=col)

        self.dashboard_sales_table.column("Invoice", width=90, anchor="center")
        self.dashboard_sales_table.column("Customer", width=220)
        self.dashboard_sales_table.column("Payment", width=120, anchor="center")
        self.dashboard_sales_table.column("Total", width=120, anchor="e")

        self.dashboard_sales_table.pack(
            fill="x",
            padx=20,
            pady=(0,20)
        )


        # =====================================================
        # INVENTORY ALERT CENTER
        # =====================================================

        alert_frame = ctk.CTkFrame(
            page,
            fg_color="transparent"
        )

        alert_frame.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=(15,20)
        )

        ctk.CTkLabel(
            alert_frame,
            text="📦 Inventory Alert Center",
            font=("Poppins",20,"bold"),
            text_color="#065F46"
        ).pack(anchor="w", pady=(0,12))

        cards = ctk.CTkFrame(alert_frame, fg_color="transparent")
        cards.pack(fill="x")

        cards.grid_columnconfigure((0,1,2,3), weight=1)

        self.create_dashboard_card(
            cards,
            "🟢 Healthy Products",
            self.dashboard_healthy_var,
            0,0,
            "#DCFCE7"
        )

        self.create_dashboard_card(
            cards,
            "🟡 Low Stock",
            self.dashboard_low_var,
            0,1,
            "#FEF3C7"
        )

        self.create_dashboard_card(
            cards,
            "🔴 Out of Stock",
            self.dashboard_out_var,
            0,2,
            "#FEE2E2"
        )

        self.create_dashboard_card(
            cards,
            "💯 Inventory Health",
            self.dashboard_health_var,
            0,3,
            "#DBEAFE"
        )
        # =====================================================
        # INVENTORY HEALTH PROGRESS BAR
        # =====================================================

        health_bar_frame = ctk.CTkFrame(
            alert_frame,
            fg_color="white",
            corner_radius=20,
            border_width=1,
            border_color="#E5E7EB"
        )

        health_bar_frame.pack(fill="x", pady=(15,0))

        ctk.CTkLabel(
            health_bar_frame,
            text="Overall Inventory Health",
            font=("Poppins",15,"bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=20, pady=(15,5))

        self.inventory_health_progress = ctk.CTkProgressBar(
            health_bar_frame,
            height=18,
            progress_color="#16A34A"
        )

        self.inventory_health_progress.pack(fill="x", padx=20)

        self.inventory_health_text = ctk.StringVar(value="Loading...")

        ctk.CTkLabel(
            health_bar_frame,
            textvariable=self.inventory_health_text,
            font=("Poppins",12),
            text_color="gray45"
        ).pack(anchor="w", padx=20, pady=(8,15))

        # =====================================================
        # WEEKLY SALES ANALYTICS CARD
        # =====================================================

        weekly_frame = ctk.CTkFrame(
            page,
            fg_color="white",
            corner_radius=20,
            border_width=1,
            border_color="#E5E7EB"
        )

        weekly_frame.grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=(20,20)
        )

        weekly_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(
            weekly_frame,
            fg_color="transparent"
        )
        header.pack(fill="x", padx=20, pady=(15,10))

        ctk.CTkLabel(
            header,
            text="📈 Weekly Revenue Analytics",
            font=("Poppins",18,"bold"),
            text_color="#065F46"
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="Last 7 Days",
            font=("Poppins",12),
            text_color="gray50"
        ).pack(side="right")

        # Chart Container
        self.weekly_chart_frame = ctk.CTkFrame(
            weekly_frame,
            fg_color="white"
        )

        self.weekly_chart_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0,20)
        )


        # =====================================================
        # TOP PRODUCTS LEADERBOARD
        # =====================================================

        leader_frame = ctk.CTkFrame(
            page,
            fg_color="white",
            corner_radius=20,
            border_width=1,
            border_color="#E5E7EB"
        )

        leader_frame.grid(
            row=9,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=(20,20)
        )

        top = ctk.CTkFrame(leader_frame, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(15,10))

        ctk.CTkLabel(
            top,
            text="🏆 Today's Best Selling Products",
            font=("Poppins",18,"bold"),
            text_color="#065F46"
        ).pack(side="left")

        badge = ctk.CTkLabel(
            top,
            text="LIVE",
            fg_color="#DCFCE7",
            text_color="#16A34A",
            corner_radius=20,
            padx=10,
            pady=4,
            font=("Poppins",10,"bold")
        )

        badge.pack(side="right")

        self.top_products_container = ctk.CTkFrame(
            leader_frame,
            fg_color="transparent"
        )

        self.top_products_container.pack(
            fill="x",
            padx=20,
            pady=(0,15)
        )
        # =====================================================
        # SMART BUSINESS INSIGHTS
        # =====================================================

        insight_frame = ctk.CTkFrame(
            page,
            fg_color="white",
            corner_radius=20,
            border_width=1,
            border_color="#E5E7EB"
        )

        insight_frame.grid(
            row=10,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=(0,25)
        )

        ctk.CTkLabel(
            insight_frame,
            text="💡 Smart Business Insights",
            font=("Poppins",20,"bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=20, pady=(15,12))

        self.insight_container = ctk.CTkFrame(
            insight_frame,
            fg_color="transparent"
        )

        self.insight_container.pack(fill="x", padx=20, pady=(0,15))

        footer = ctk.CTkFrame(
                page,
                fg_color="transparent"
            )

        footer.grid(
                row=11,
                column=0,
                columnspan=2,
                pady=(15,30)
            )

        ctk.CTkLabel(
                footer,
                text="Shingvi Supermart POS v2.5 • Developed by Jinesh Shingvi",
                font=("Poppins",11),
                text_color="gray55"
            ).pack()

        ctk.CTkLabel(
                footer,
                text="Inventory • Billing • Reports • Loyalty • Analytics",
                font=("Poppins",10),
                text_color="gray45"
            ).pack()


        return page

    # ==========================================================
    # DASHBOARD CARD
    # ==========================================================
    def create_dashboard_card(self, parent, title, variable,
                          row, column,
                          color="#FFFFFF"):

        card = ctk.CTkFrame(
            parent,
            fg_color=color,
            corner_radius=22,
            border_width=1,
            border_color="#E5E7EB",
            height=160
        )

        card.grid(
            row=row,
            column=column,
            padx=18,
            pady=15,
            sticky="nsew"
        )

        # Icon Mapping
        icons = {
            "Today's Revenue": "💰",
            "Orders Today": "🛒",
            "Inventory Value": "📦",
            "Expected Profit": "📈",
            "Healthy Products": "🟢",
            "Low Stock": "🟡",
            "Out of Stock": "🔴",
            "Inventory Health": "💯"
        }

        icon = "⭐"

        for key, value in icons.items():
            if key in title:
                icon = value

        # Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(12,8))

        bubble = ctk.CTkLabel(
            header,
            text=icon,
            width=38,
            height=38,
            corner_radius=19,
            fg_color="#FFFFFF",
            text_color="#15803D",
            font=("Poppins",18)
        )
        bubble.pack(side="left")

        live = ctk.CTkLabel(
            header,
            text="LIVE",
            fg_color="#DCFCE7",
            text_color="#16A34A",
            corner_radius=20,
            padx=10,
            pady=3,
            font=("Poppins",10,"bold")
        )
        live.pack(side="right")

        # Title
        ctk.CTkLabel(
            card,
            text=title,
            font=("Poppins",12),
            text_color="#64748B"
        ).pack(anchor="w", padx=16)

        # Value
        ctk.CTkLabel(
            card,
            textvariable=variable,
            font=("Poppins",28,"bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=16, pady=(2,4))

        # Footer
        footer = ctk.CTkFrame(card, fg_color="transparent")
        footer.pack(fill="x", padx=16, pady=(4,10))

        ctk.CTkLabel(
            footer,
            text="▲ Updated Live",
            font=("Poppins",10,"bold"),
            text_color="#16A34A"
        ).pack(anchor="w")
    # ==========================================================
    # PAGE NAVIGATION
    # ==========================================================
    def hide_all_pages(self):
        self.dashboard_page.pack_forget()
        self.products_page.pack_forget()
        self.billing_page.pack_forget()
        self.customers_page.pack_forget()
        self.reports_page.pack_forget()

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

        self.load_dashboard()      # Keep this

        self.update_dashboard_clock()

    def show_products(self):

        self.hide_all_pages()

        self.products_page.pack(fill="both", expand=True)

        self.products_page.load_products()

        self.highlight_button(self.products_btn)

    def show_billing(self):

        self.hide_all_pages()

        self.billing_page.pack(fill="both", expand=True)

        self.highlight_button(self.billing_btn)

    def show_customers(self):

        self.hide_all_pages()

        self.customers_page.pack(fill="both", expand=True)

        self.customers_page.load_customers()

        self.highlight_button(self.customers_btn)

    def show_reports(self):
        self.hide_all_pages()
        self.reports_page.pack(fill="both", expand=True)
        self.reports_page.load_reports()
        self.highlight_button(self.reports_btn)
    # ==========================================================
    # THEME
    # ==========================================================
    def change_theme(self, mode):
        ctk.set_appearance_mode(mode)

    # ==========================================================
    # DASHBOARD LIVE CLOCK
    # ==========================================================
    def update_dashboard_clock(self):

        now = datetime.now()

        hour = now.hour

        if hour < 12:
            greeting = "☀ Good Morning,"
        elif hour < 17:
            greeting = "🌤 Good Afternoon,"
        elif hour < 21:
            greeting = "🌇 Good Evening,"
        else:
            greeting = "🌙 Good Night,"

        self.dashboard_greeting_var.set(greeting)

        self.dashboard_date_var.set(
            now.strftime("%A • %d %B %Y")
        )

        self.dashboard_time_var.set(
            now.strftime("%I:%M:%S %p")
        )

        self.after(1000, self.update_dashboard_clock)
    # ==========================================================
    # SMOOTH SCROLL (Works for all pages)
    # ==========================================================
    def _smooth_scroll(self, event):
        try:
            # Linux
            if hasattr(event, "num"):
                if event.num == 4:
                    delta = -1
                elif event.num == 5:
                    delta = 1
                else:
                    delta = 0
            else:
                # Windows / macOS
                delta = int(-event.delta / 120)

            widget = self.focus_get()

            while widget:
                    # Skip drawing canvases (charts, graphs, etc.)
                    if widget.winfo_class() == "Canvas":
                        widget = widget.master
                        continue

                    # Scroll only real scrollable widgets
                    if hasattr(widget, "yview_scroll"):
                        widget.yview_scroll(delta, "units")
                        break

                    widget = widget.master

        except Exception:
            pass

    # ==========================================================
    # LOAD DASHBOARD DATA
    # ==========================================================
    def load_dashboard(self):

        revenue = get_today_revenue()
        orders = get_today_orders()

        # Inventory values come as a dictionary
        inventory = get_inventory_value()

        purchase = float(inventory["purchase_value"] or 0)
        selling = float(inventory["selling_value"] or 0)
        profit = float(inventory["expected_profit"] or 0)

        self.dashboard_revenue_var.set(f"₹{float(revenue):,.2f}")
        self.dashboard_orders_var.set(str(orders))
        self.dashboard_inventory_var.set(f"₹{selling:,.2f}")
        self.dashboard_profit_var.set(f"₹{profit:,.2f}")

        # =====================================================
        # LOAD RECENT SALES
        # =====================================================

        if hasattr(self, "dashboard_sales_table"):

            # Clear previous rows
            self.dashboard_sales_table.delete(
                *self.dashboard_sales_table.get_children()
            )

            sales = get_recent_sales()

            for sale in sales:

                sale_id, customer, payment, total, sale_date = sale

                payment_icons = {
                    "Cash": "💵 Cash",
                    "UPI": "📱 UPI",
                    "Card": "💳 Card"
                }

                self.dashboard_sales_table.insert(
                    "",
                    "end",
                    values=(
                        f"INV{sale_id:04}",
                        customer.title(),
                        payment_icons.get(payment, payment),
                        f"₹{float(total):,.2f}"
                    )
                )

        # =====================================================
        # TOP PRODUCTS LEADERBOARD
        # =====================================================

        for widget in self.top_products_container.winfo_children():
            widget.destroy()

        products = get_dashboard_top_products()

        if products:

            max_qty = max(qty for _, qty in products)

            medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]

            colors = [
                "#16A34A",
                "#2563EB",
                "#CA8A04",
                "#9333EA",
                "#EA580C"
            ]

            for index, (name, qty) in enumerate(products):

                card = ctk.CTkFrame(
                    self.top_products_container,
                    fg_color="#F9FAFB",
                    corner_radius=15
                )

                card.pack(fill="x", pady=6)

                row = ctk.CTkFrame(card, fg_color="transparent")
                row.pack(fill="x", padx=12, pady=(10,6))

                left = ctk.CTkFrame(row, fg_color="transparent")
                left.pack(side="left")

                ctk.CTkLabel(
                    left,
                    text=f"{medals[index]} {name.title()}",
                    font=("Poppins",13,"bold")
                ).pack(anchor="w")

                ctk.CTkLabel(
                    left,
                    text=f"{qty} units sold today",
                    font=("Poppins",11),
                    text_color="gray45"
                ).pack(anchor="w")

                ctk.CTkLabel(
                    row,
                    text=str(qty),
                    font=("Poppins",14,"bold"),
                    text_color=colors[index]
                ).pack(side="right")

                progress = ctk.CTkProgressBar(card, height=8)

                progress.pack(fill="x", padx=12, pady=(0,12))

                progress.set(qty/max_qty)
        # Snapshot Values

        gst_today = revenue * 0.18

        discount_today = revenue * 0.03

        self.snapshot_gst_var.set(f"₹{gst_today:,.0f}")
        self.snapshot_discount_var.set(f"₹{discount_today:,.0f}")

        self.snapshot_customer_var.set(str(orders))
        self.snapshot_loyalty_var.set(str(orders * 4))

        # =====================================================
        # SALES TARGET
        # =====================================================

        daily_target = 10000

        progress = min(revenue / daily_target, 1)

        remaining = max(daily_target - revenue, 0)

        self.sales_progress.set(progress)

        self.sales_target_var.set(f"{progress*100:.0f}%")

        self.sales_remaining_var.set(
            f"₹{remaining:,.0f} Remaining to Reach ₹10,000 Target"
        )
        # =====================================================
        # INVENTORY ALERT CENTER
        # =====================================================

        alerts = get_dashboard_inventory_alerts()

        healthy = alerts["healthy"]
        low_stock = alerts["low_stock"]
        out_stock = alerts["out_stock"]

        total_products = healthy + low_stock + out_stock

        if total_products == 0:
            score = 100
        else:
            score = int((healthy / total_products) * 100)

        self.dashboard_healthy_var.set(str(healthy))
        self.dashboard_low_var.set(str(low_stock))
        self.dashboard_out_var.set(str(out_stock))
        self.dashboard_health_var.set(f"{score}%")

        self.notification_count_var.set(
            str(low_stock + out_stock)
        )
        # Update Inventory Health Progress Bar
        self.inventory_health_progress.set(score / 100)

        if score >= 80:
            health_message = "🟢 Excellent Inventory Health"
        elif score >= 50:
            health_message = "🟡 Moderate Inventory Health"
        else:
            health_message = "🔴 Critical Inventory Health"

        self.inventory_health_text.set(
            f"{health_message} ({score}%)"
        )
        
        # =====================================================
        # WEEKLY SALES CHART
        # =====================================================

        weekly_sales = get_weekly_sales()

        self.draw_weekly_chart(weekly_sales)

        # =====================================================
        # SMART BUSINESS INSIGHTS
        # =====================================================

        for widget in self.insight_container.winfo_children():
            widget.destroy()

        insights = get_dashboard_insights()

        for title, message in insights:
            colors = {
                "🟢":"#DCFCE7",
                "🟡":"#FEF3C7",
                "🏆":"#DBEAFE",
                "🔴":"#FEE2E2"
            }

            for title, message in insights:

                bg = "#F9FAFB"

                for emoji, color in colors.items():
                    if emoji in title:
                        bg = color

                insight = ctk.CTkFrame(
                    self.insight_container,
                    fg_color=bg,
                    corner_radius=18,
                    border_width=1,
                    border_color="#E5E7EB"
                )

                insight.pack(fill="x", pady=8)

                ctk.CTkLabel(
                    insight,
                    text=title,
                    font=("Poppins",14,"bold"),
                    text_color="#065F46"
                ).pack(anchor="w", padx=18, pady=(12,4))

                ctk.CTkLabel(
                    insight,
                    text=message,
                    wraplength=760,
                    justify="left",
                    font=("Poppins",12)
                ).pack(anchor="w", padx=18, pady=(0,12))
            

    def draw_weekly_chart(self, sales_data):

        # Remove old graph if it exists
        for widget in self.weekly_chart_frame.winfo_children():
            widget.destroy()

        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        values = [0]*7

        for day, amount in sales_data:
            values[day.weekday()] = float(amount)

        fig, ax = plt.subplots(figsize=(8,3), dpi=100)

        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        ax.plot(
            days,
            values,
            linewidth=3,
            marker="o",
            markersize=7
        )

        ax.fill_between(days, values, alpha=0.15)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.grid(axis="y", alpha=0.3)

        ax.set_title(
            "Last 7 Days Revenue",
            fontsize=12,
            fontweight="bold",
            color="#065F46"
        )

        ax.set_ylabel("Revenue (₹)", fontsize=10)

        canvas = FigureCanvasTkAgg(fig, master=self.weekly_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        plt.close(fig)
# ==========================================================
# RUN APP
# ==========================================================
if __name__ == "__main__":
    app = ShingviSupermartApp()
    app.mainloop()