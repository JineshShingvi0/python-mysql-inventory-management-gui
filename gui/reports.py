import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

from backend import (
    get_today_revenue,
    get_today_orders,
    get_total_products,
    get_low_stock_products,
    get_best_selling_products,
    get_top_customers,
    get_monthly_sales,
    get_inventory_value,
    get_stock_movements,
    get_sales_history,
    get_payment_analytics,
    get_inventory_health,
    get_sale_for_return,
    get_sale_items_for_return,
    process_return,
    get_return_history,
    get_purchase_history,
    get_today_purchase_analytics,
    get_today_profit_analytics
)


class ReportsPage(ctk.CTkScrollableFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="#F9FAFB",
            corner_radius=0
        )

        self.revenue_var = ctk.StringVar(value="₹0")
        self.orders_var = ctk.StringVar(value="0")
        self.products_var = ctk.StringVar(value="0")
        self.low_stock_var = ctk.StringVar(value="0")
        self.purchase_value_var = ctk.StringVar(value="₹0")
        self.selling_value_var = ctk.StringVar(value="₹0")
        self.profit_value_var = ctk.StringVar(value="₹0")
        self.cash_var = ctk.StringVar(value="₹0")
        self.upi_var = ctk.StringVar(value="₹0")
        self.card_var = ctk.StringVar(value="₹0")
        self.payment_var = ctk.StringVar(value="Cash")
        self.date_var = ctk.StringVar()
        self.time_var = ctk.StringVar()
        self.last_updated_var = ctk.StringVar(value="Last Updated • --:--:--")
        self.healthy_var = ctk.StringVar(value="0")
        self.low_inventory_var = ctk.StringVar(value="0")
        self.out_stock_var = ctk.StringVar(value="0")
        self.health_score_var = ctk.StringVar(value="0%")
        self.today_purchase_var = ctk.StringVar(value="₹0.00")
        self.purchase_count_var = ctk.StringVar(value="0")
        self.gross_profit_var = ctk.StringVar(value="₹0.00")
        self.profit_margin_var = ctk.StringVar(value="0.00%")

        self.build_ui()
        self.load_reports()     
        self.update_clock() 

    # ==========================================================
    # BUILD UI
    # ==========================================================
    def build_ui(self):

        # =====================================================
        # PREMIUM HEADER
        # =====================================================

        header = ctk.CTkFrame(
            self,
            fg_color="#ECFDF5",
            corner_radius=18
        )
        header.pack(fill="x", padx=30, pady=(20,20))

        # Left Side
        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", padx=20, pady=15)

        ctk.CTkLabel(
            left,
            text="Welcome Back 👋",
            font=("Poppins",14)
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Jinesh",
            font=("Poppins",28,"bold"),
            text_color="#065F46"
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Shingvi Supermart Analytics Dashboard",
            font=("Poppins",13)
        ).pack(anchor="w")

        # Right Side
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=20, pady=15)

        ctk.CTkLabel(
            right,
            textvariable=self.date_var,
            font=("Poppins",14,"bold")
        ).pack(anchor="e")

        ctk.CTkLabel(
            right,
            textvariable=self.time_var,
            font=("Poppins",22,"bold"),
            text_color="#16A34A"
        ).pack(anchor="e")

        ctk.CTkLabel(
            right,
            textvariable=self.last_updated_var,
            font=("Poppins",11)
        ).pack(anchor="e")

        # Refresh Button
        refresh_btn = ctk.CTkButton(
            right,
            text="↻ Refresh Reports",
            width=170,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.load_reports
        )
        refresh_btn.pack(anchor="e", pady=(10,0))
        ctk.CTkLabel(
            self,
            text="Business insights, sales analytics and inventory health.",
            font=("Poppins", 13),
            text_color="gray40"
        ).pack(anchor="w", padx=30)


        # =====================================================
        # SUMMARY CARDS
        # =====================================================

        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30)

        cards_frame.grid_columnconfigure((0, 1), weight=1)

        self.create_card(
            cards_frame,
            "💰 Today's Revenue",
            self.revenue_var,
            0,0,
            "#DCFCE7"
        )

        self.create_card(
            cards_frame,
            "🛒 Orders Today",
            self.orders_var,
            0,1,
            "#DBEAFE"
        )

        self.create_card(
            cards_frame,
            "📦 Products",
            self.products_var,
            1,0,
            "#FEF3C7"
        )

        self.create_card(
            cards_frame,
            "⚠ Low Stock Products",
            self.low_stock_var,
            1,1,
            "#FEE2E2"
        )

        separator = ctk.CTkFrame(
            self,
            fg_color="#E5E7EB",
            height=2,
            corner_radius=2
        )
        separator.pack(fill="x", padx=30, pady=(8,18))


        # =====================================================
        # PAYMENT ANALYTICS
        # =====================================================

        payment_frame = ctk.CTkFrame(self, fg_color="transparent")
        payment_frame.pack(fill="x", padx=30, pady=(0,20))

        payment_frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.create_payment_card(
            payment_frame,
            "Cash Revenue",
            self.cash_var,
            "#DCFCE7",
            "💵",
            0,0
        )

        self.create_payment_card(
            payment_frame,
            "UPI Revenue",
            self.upi_var,
            "#DBEAFE",
            "📱",
            0,1
        )

        self.create_payment_card(
            payment_frame,
            "Card Revenue",
            self.card_var,
            "#F3E8FF",
            "💳",
            0,2
        )

        self.create_payment_card(
            payment_frame,
            "Most Used",
            self.payment_var,
            "#FEF3C7",
            "🏆",
            0,3
        )
        
        progress_frame = ctk.CTkFrame(self)
        progress_frame.pack(fill="x", padx=30, pady=(0,20))

        ctk.CTkLabel(
            progress_frame,
            text="Payment Distribution",
            font=("Poppins",18,"bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=20, pady=(15,10))

        self.cash_progress = ctk.CTkProgressBar(progress_frame)
        self.upi_progress = ctk.CTkProgressBar(progress_frame)
        self.card_progress = ctk.CTkProgressBar(progress_frame)

        self.cash_progress.configure(progress_color="#16A34A")
        self.upi_progress.configure(progress_color="#2563EB")
        self.card_progress.configure(progress_color="#9333EA")

        self.cash_progress.set(0)
        self.upi_progress.set(0)
        self.card_progress.set(0)
        
        for title, bar in [
            ("💵 Cash", self.cash_progress),
            ("📱 UPI", self.upi_progress),
            ("💳 Card", self.card_progress)
        ]:
            ctk.CTkLabel(progress_frame,
                        text=title,
                        font=("Poppins",13,"bold")).pack(anchor="w", padx=20)

            bar.pack(fill="x", padx=20, pady=(0,12))

            # ---------------- DONUT CHART ----------------

        self.payment_canvas = ctk.CTkCanvas(
            progress_frame,
            width=280,
            height=280,
            bg="white",
            highlightthickness=0
        )

        self.payment_canvas.pack(pady=(10,20))

        self.cash_progress.configure(progress_color="#16A34A")
        self.upi_progress.configure(progress_color="#2563EB")
        self.card_progress.configure(progress_color="#9333EA")

        self.cash_progress.set(0)
        self.upi_progress.set(0)
        self.card_progress.set(0)

        
        separator = ctk.CTkFrame(
            self,
            fg_color="#E5E7EB",
            height=2,
            corner_radius=2
        )
        separator.pack(fill="x", padx=30, pady=(8,18))

        # =====================================================
        # INVENTORY HEALTH
        # =====================================================

        health_frame = ctk.CTkFrame(self, fg_color="transparent")
        health_frame.pack(fill="x", padx=30, pady=(0,20))

        ctk.CTkLabel(
            health_frame,
            text="📦 Inventory Health",
            font=("Poppins",20,"bold"),
            text_color="#065F46"
        ).pack(anchor="w", pady=(0,10))

        cards = ctk.CTkFrame(health_frame, fg_color="transparent")
        cards.pack(fill="x")

        cards.grid_columnconfigure((0,1,2,3), weight=1)

        self.create_payment_card(
            cards,
            "Healthy",
            self.healthy_var,
            "#DCFCE7",
            "🟢",
            0,0
        )

        self.create_payment_card(
            cards,
            "Low Stock",
            self.low_inventory_var,
            "#FEF3C7",
            "🟡",
            0,1
        )

        self.create_payment_card(
            cards,
            "Out of Stock",
            self.out_stock_var,
            "#FEE2E2",
            "🔴",
            0,2
        )

        self.create_payment_card(
            cards,
            "Health Score",
            self.health_score_var,
            "#DBEAFE",
            "💯",
            0,3
        )

        score_frame = ctk.CTkFrame(health_frame)
        score_frame.pack(fill="x", pady=(15,0))

        ctk.CTkLabel(
            score_frame,
            text="Overall Inventory Health",
            font=("Poppins",15,"bold")
        ).pack(anchor="w", padx=20, pady=(15,8))

        self.health_progress = ctk.CTkProgressBar(score_frame, height=20)
        self.health_progress.pack(fill="x", padx=20, pady=(0,20))
        self.health_progress.configure(
            progress_color="#16A34A",
            fg_color="#DCFCE7"
        )

        separator = ctk.CTkFrame(
            self,
            fg_color="#E5E7EB",
            height=2,
            corner_radius=2
        )
        separator.pack(fill="x", padx=30, pady=(8,18))

        # =====================================================
        # INVENTORY VALUE CARDS
        # =====================================================

        inventory_cards = ctk.CTkFrame(self, fg_color="transparent")
        inventory_cards.pack(fill="x", padx=30, pady=(5,20))

        inventory_cards.grid_columnconfigure((0,1,2), weight=1)

        self.create_card(
            inventory_cards,
            "📦 Inventory Purchase Value",
            self.purchase_value_var,
            0,0
        )

        self.create_card(
            inventory_cards,
            "💰 Inventory Selling Value",
            self.selling_value_var,
            0,1
        )

        self.create_card(
            inventory_cards,
            "📈 Expected Profit",
            self.profit_value_var,
            0,2
        )


        # =====================================================
        # PURCHASE ANALYTICS
        # =====================================================

        purchase_cards = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        purchase_cards.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        purchase_cards.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        self.create_card(
            purchase_cards,
            "📦 Today's Purchases",
            self.today_purchase_var,
            0,
            0
        )

        self.create_card(
            purchase_cards,
            "🧾 Purchase Transactions",
            self.purchase_count_var,
            0,
            1
        )

        # =====================================================
        # REALIZED PROFIT
        # =====================================================

        profit_cards = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        profit_cards.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        profit_cards.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        self.create_card(
            profit_cards,
            "📈 Today's Gross Profit",
            self.gross_profit_var,
            0,
            0
        )

        self.create_card(
            profit_cards,
            "📊 Profit Margin",
            self.profit_margin_var,
            0,
            1
        )
        # =====================================================
        # TABLE SECTION
        # =====================================================

        tables_frame = ctk.CTkFrame(self, fg_color="transparent")
        tables_frame.pack(fill="both", expand=True, padx=30, pady=25)

        tables_frame.grid_columnconfigure((0, 1), weight=1)

        # Left
        self.best_frame = ctk.CTkFrame(tables_frame)
        self.best_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Right
        self.customer_frame = ctk.CTkFrame(tables_frame)
        self.customer_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.build_best_selling_table()
        self.build_top_customer_table()

        separator = ctk.CTkFrame(
            self,
            fg_color="#E5E7EB",
            height=2,
            corner_radius=2
        )
        separator.pack(fill="x", padx=30, pady=(8,18))

        # =====================================================
        # MONTHLY REVENUE CHART
        # =====================================================

        chart_frame = ctk.CTkFrame(self)
        chart_frame.pack(fill="x", padx=30, pady=(0,25))

        ctk.CTkLabel(
            chart_frame,
            text="📈 Monthly Revenue (2026)",
            font=("Poppins",18,"bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=20, pady=(15,10))

        self.chart_canvas = ctk.CTkCanvas(
            chart_frame,
            height=240,
            bg="white",
            highlightthickness=0
        )

        self.chart_canvas.pack(fill="x", padx=20, pady=(0,20))

        separator = ctk.CTkFrame(
            self,
            fg_color="#E5E7EB",
            height=2,
            corner_radius=2
        )
        separator.pack(fill="x", padx=30, pady=(8,18))

        # =====================================================
        # STOCK MOVEMENT HISTORY
        # =====================================================

        movement_frame = ctk.CTkFrame(self)
        movement_frame.pack(fill="both", expand=True, padx=30, pady=(0,25))

        ctk.CTkLabel(
            movement_frame,
            text="📦 Stock Movement History",
            font=("Poppins",18,"bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=20, pady=(15,10))

        columns = ("Date","Product","Movement","Quantity","Stock After")

        self.movement_table = ttk.Treeview(
            movement_frame,
            columns=columns,
            show="headings",
            height=7
        )

        for col in columns:
            self.movement_table.heading(col, text=col)

        self.movement_table.column("Date", width=140, anchor="center")
        self.movement_table.column("Product", width=180)
        self.movement_table.column("Movement", width=110, anchor="center")
        self.movement_table.column("Quantity", width=80, anchor="center")
        self.movement_table.column("Stock After", width=100, anchor="center")

        scroll = ttk.Scrollbar(
            movement_frame,
            orient="vertical",
            command=self.movement_table.yview
        )

        self.movement_table.configure(yscrollcommand=scroll.set)

        self.movement_table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(20,0),
            pady=(0,15)
        )

        scroll.pack(
            side="right",
            fill="y",
            padx=(0,20),
            pady=(0,15)
        )
        separator = ctk.CTkFrame(
            self,
            fg_color="#E5E7EB",
            height=2,
            corner_radius=2
        )
        separator.pack(fill="x", padx=30, pady=(8,18))


        # =====================================================
        # SALES LEDGER
        # =====================================================

        ledger_frame = ctk.CTkFrame(self)
        ledger_frame.pack(fill="both", expand=True, padx=30, pady=(0,25))

        # Header
        header = ctk.CTkFrame(ledger_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15,10))

        ctk.CTkLabel(
            header,
            text="🧾 Sales Ledger",
            font=("Poppins",18,"bold"),
            text_color="#065F46"
        ).pack(side="left")

        # Search Box
        self.search_var = ctk.StringVar()

        search_entry = ctk.CTkEntry(
            header,
            textvariable=self.search_var,
            placeholder_text="Search customer...",
            width=220,
            height=36
        )

        search_entry.pack(side="right")

        search_entry.bind("<KeyRelease>", lambda event: self.load_reports())

        # Ledger Table
        columns = (
            "Invoice",
            "Customer",
            "Payment",
            "Total",
            "Date"
        )

        self.sales_table = ttk.Treeview(
            ledger_frame,
            columns=columns,
            show="headings",
            height=8
        )

        for col in columns:
            self.sales_table.heading(col, text=col)

        self.sales_table.column("Invoice", width=90, anchor="center")
        self.sales_table.column("Customer", width=180)
        self.sales_table.column("Payment", width=100, anchor="center")
        self.sales_table.column("Total", width=120, anchor="center")
        self.sales_table.column("Date", width=150, anchor="center")

        scroll = ttk.Scrollbar(
            ledger_frame,
            orient="vertical",
            command=self.sales_table.yview
        )

        self.sales_table.configure(yscrollcommand=scroll.set)

        self.sales_table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(20,0),
            pady=(0,20)
        )

        scroll.pack(
            side="right",
            fill="y",
            padx=(0,20),
            pady=(0,20)
        )

# ==========================================================
        # SALES RETURN / REFUND
        # ==========================================================

        return_button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        return_button_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 10)
        )

        self.return_button = ctk.CTkButton(
            return_button_frame,
            text="↩ Return / Refund Selected Invoice",
            width=260,
            height=40,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            font=("Poppins", 13, "bold"),
            command=self.open_return_popup
        )

        self.return_button.pack(
            side="right"
        )
        separator = ctk.CTkFrame(
            self,
            fg_color="#E5E7EB",
            height=2,
            corner_radius=2
        )
        separator.pack(fill="x", padx=30, pady=(8,18))

        # ==========================================================
        # RETURN HISTORY
        # ==========================================================

        return_history_frame = ctk.CTkFrame(
            self,
            fg_color="#E5E7EB",
            corner_radius=10
        )

        return_history_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        ctk.CTkLabel(
            return_history_frame,
            text="↩ Return History",
            font=("Poppins", 18, "bold"),
            text_color="#DC2626"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        return_table_frame = ctk.CTkFrame(
            return_history_frame,
            fg_color="transparent"
        )

        return_table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        return_columns = (
            "Return ID",
            "Invoice",
            "Customer",
            "Product",
            "Qty",
            "Refund",
            "Date"
        )

        self.return_table = ttk.Treeview(
            return_table_frame,
            columns=return_columns,
            show="headings",
            height=6
        )

        for col in return_columns:

            self.return_table.heading(
                col,
                text=col
            )

        self.return_table.column(
            "Return ID",
            width=80,
            anchor="center"
        )

        self.return_table.column(
            "Invoice",
            width=90,
            anchor="center"
        )

        self.return_table.column(
            "Customer",
            width=140
        )

        self.return_table.column(
            "Product",
            width=180
        )

        self.return_table.column(
            "Qty",
            width=70,
            anchor="center"
        )

        self.return_table.column(
            "Refund",
            width=110,
            anchor="e"
        )

        self.return_table.column(
            "Date",
            width=150,
            anchor="center"
        )

        return_scroll = ttk.Scrollbar(
            return_table_frame,
            orient="vertical",
            command=self.return_table.yview
        )

        self.return_table.configure(
            yscrollcommand=return_scroll.set
        )

        self.return_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        return_scroll.pack(
            side="right",
            fill="y"
        )

        # ==========================================================
        # PURCHASE HISTORY
        # ==========================================================

        purchase_history_frame = ctk.CTkFrame(
            self,
            fg_color="#E5E7EB",
            corner_radius=10
        )

        purchase_history_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        ctk.CTkLabel(
            purchase_history_frame,
            text="📦 Purchase History",
            font=("Poppins", 18, "bold"),
            text_color="#EA580C"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        purchase_table_frame = ctk.CTkFrame(
            purchase_history_frame,
            fg_color="transparent"
        )

        purchase_table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        purchase_columns = (
            "Purchase ID",
            "Supplier",
            "Product",
            "Qty",
            "Purchase Price",
            "Total Cost",
            "Date"
        )

        self.purchase_table = ttk.Treeview(
            purchase_table_frame,
            columns=purchase_columns,
            show="headings",
            height=6
        )

        for col in purchase_columns:

            self.purchase_table.heading(
                col,
                text=col
            )

        self.purchase_table.column(
            "Purchase ID",
            width=90,
            anchor="center"
        )

        self.purchase_table.column(
            "Supplier",
            width=150
        )

        self.purchase_table.column(
            "Product",
            width=170
        )

        self.purchase_table.column(
            "Qty",
            width=70,
            anchor="center"
        )

        self.purchase_table.column(
            "Purchase Price",
            width=120,
            anchor="e"
        )

        self.purchase_table.column(
            "Total Cost",
            width=120,
            anchor="e"
        )

        self.purchase_table.column(
            "Date",
            width=150,
            anchor="center"
        )

        purchase_scroll = ttk.Scrollbar(
            purchase_table_frame,
            orient="vertical",
            command=self.purchase_table.yview
        )

        self.purchase_table.configure(
            yscrollcommand=purchase_scroll.set
        )

        self.purchase_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        purchase_scroll.pack(
            side="right",
            fill="y"
        )
        # =====================================================
        # LOW STOCK TABLE
        # =====================================================

        low_frame = ctk.CTkFrame(self)
        low_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        ctk.CTkLabel(
            low_frame,
            text="⚠️ Low Stock Products",
            font=("Poppins", 18, "bold"),
            text_color="#DC2626"
        ).pack(anchor="w", padx=20, pady=(15, 10))

        columns = ("Product", "Stock", "Minimum")

        self.low_table = ttk.Treeview(
            low_frame,
            columns=columns,
            show="headings",
            height=6
        )

        for col in columns:
            self.low_table.heading(col, text=col)

        self.low_table.column("Product", width=220)
        self.low_table.column("Stock", width=80, anchor="center")
        self.low_table.column("Minimum", width=90, anchor="center")

        scrollbar = ttk.Scrollbar(
            low_frame,
            orient="vertical",
            command=self.low_table.yview
        )

        self.low_table.configure(yscrollcommand=scrollbar.set)

        self.low_table.pack(side="left", fill="both", expand=True,
                            padx=(20, 0), pady=(0, 15))

        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=(0, 15))


    # ==========================================================
    # CARD UI
    # ==========================================================

    def create_card(self, parent, title, variable, row, column, color="#FFFFFF"):

        card = ctk.CTkFrame(
            parent,
            fg_color=color,
            corner_radius=20,
            border_width=1,
            border_color="#D1D5DB",
            height=135
        )

        card.grid(
            row=row,
            column=column,
            padx=12,
            pady=12,
            sticky="nsew"
        )

        # Top Row
        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=18, pady=(15,8))

        ctk.CTkLabel(
            top,
            text=title,
            font=("Poppins",14,"bold"),
            text_color="#475569"
        ).pack(side="left")

        badge = ctk.CTkLabel(
            top,
            text="LIVE",
            width=48,
            height=22,
            corner_radius=20,
            fg_color="#DCFCE7",
            text_color="#15803D",
            font=("Poppins",10,"bold")
        )
        badge.pack(side="right")

        # Main Value
        ctk.CTkLabel(
            card,
            textvariable=variable,
            font=("Poppins",30,"bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=18)

        # Footer
        ctk.CTkLabel(
            card,
            text="Updated Today",
            font=("Poppins",11),
            text_color="#64748B"
        ).pack(anchor="w", padx=18, pady=(5,15))
        
    def create_payment_card(
        self,
        parent,
        title,
        variable,
        color,
        emoji,
        row,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=color,
            corner_radius=18,
            border_width=1,
            border_color="#E5E7EB",
            height=110
        )

        card.grid(
            row=row,
            column=column,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ctk.CTkLabel(
            card,
            text=f"{emoji} {title}",
            font=("Poppins",13,"bold"),
            text_color="#334155"
        ).pack(anchor="w", padx=15, pady=(15,8))

        ctk.CTkLabel(
            card,
            textvariable=variable,
            font=("Poppins",24,"bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=15)

        ctk.CTkLabel(
            card,
            text="Today's Analytics",
            font=("Poppins",10),
            text_color="#64748B"
        ).pack(anchor="w", padx=15, pady=(4,12))
    # ==========================================================
    # BEST SELLING TABLE
    # ==========================================================

    def build_best_selling_table(self):

        ctk.CTkLabel(
            self.best_frame,
            text="🏆 Best Selling Products",
            font=("Poppins", 18, "bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=20, pady=(15, 10))

        columns = ("Product", "Sold")

        self.best_table = ttk.Treeview(
            self.best_frame,
            columns=columns,
            show="headings",
            height=7
        )

        self.best_table.heading("Product", text="Product")
        self.best_table.heading("Sold", text="Sold Qty")

        self.best_table.column("Product", width=220)
        self.best_table.column("Sold", width=90, anchor="center")

        self.best_table.pack(fill="both", expand=True,
                             padx=20, pady=(0, 15))

    # ==========================================================
    # TOP CUSTOMERS TABLE
    # ==========================================================

    def build_top_customer_table(self):

        ctk.CTkLabel(
            self.customer_frame,
            text="👑 Top Customers",
            font=("Poppins", 18, "bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=20, pady=(15, 10))

        columns = ("Customer", "Spent")

        self.customer_table = ttk.Treeview(
            self.customer_frame,
            columns=columns,
            show="headings",
            height=7
        )

        self.customer_table.heading("Customer", text="Customer")
        self.customer_table.heading("Spent", text="Total Spent")

        self.customer_table.column("Customer", width=180)
        self.customer_table.column("Spent", width=110, anchor="center")

        self.customer_table.pack(fill="both", expand=True,
                                 padx=20, pady=(0, 15))


    # =====================================================
    # LIVE CLOCK
    # =====================================================

    def update_clock(self):

        now = datetime.now()

        self.date_var.set(now.strftime("%d %B %Y"))
        self.time_var.set(now.strftime("%I:%M:%S %p"))

        self.after(1000, self.update_clock)

    def draw_payment_chart(self, cash, upi, card):

        self.payment_canvas.delete("all")

        total = cash + upi + card

        if total == 0:
            self.payment_canvas.create_text(
                140,
                140,
                text="No Sales",
                font=("Poppins",16,"bold"),
                fill="#64748B"
            )
            return

        x1, y1, x2, y2 = 30, 30, 250, 250

        start = 90

        colors = [
            ("Cash", cash, "#16A34A"),
            ("UPI", upi, "#2563EB"),
            ("Card", card, "#9333EA")
        ]

        for label, value, color in colors:

            extent = (value / total) * 360

            self.payment_canvas.create_arc(
                x1, y1, x2, y2,
                start=start,
                extent=-extent,
                fill=color,
                outline="white",
                width=3
            )

            start -= extent

        # Donut Hole
        self.payment_canvas.create_oval(
            75, 75, 205, 205,
            fill="white",
            outline="white"
        )

        self.payment_canvas.create_text(
            140,
            120,
            text="Today's Sales",
            font=("Poppins",11),
            fill="#64748B"
        )

        self.payment_canvas.create_text(
            140,
            145,
            text=f"₹{total:.0f}",
            font=("Poppins",20,"bold"),
            fill="#065F46"
        )

        # Legend
        legend_y = 260

        legend_items = [
            ("Cash", "#16A34A"),
            ("UPI", "#2563EB"),
            ("Card", "#9333EA")
        ]

        legend_x = 20

        for text, color in legend_items:

            self.payment_canvas.create_rectangle(
                legend_x,
                legend_y,
                legend_x + 12,
                legend_y + 12,
                fill=color,
                outline=color
            )

            self.payment_canvas.create_text(
                legend_x + 40,
                legend_y + 6,
                text=text,
                font=("Poppins",10),
                anchor="w"
            )

            legend_x += 90

    # ==========================================================
    # RETURN / REFUND POPUP
    # ==========================================================

    def open_return_popup(self):

        selected = self.sales_table.selection()

        if not selected:

            messagebox.showwarning(
                "No Invoice Selected",
                "Please select an invoice from Sales History first."
            )

            return

        # ------------------------------------------------------
        # Get selected invoice
        # ------------------------------------------------------

        values = self.sales_table.item(
            selected[0],
            "values"
        )

        invoice_text = str(
            values[0]
        )

        if not invoice_text.startswith("INV"):

            messagebox.showerror(
                "Invalid Invoice",
                "Unable to determine the selected invoice."
            )

            return

        try:

            sale_id = int(
                invoice_text.replace(
                    "INV",
                    ""
                )
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Invoice",
                "Unable to determine the sale ID."
            )

            return

        # ------------------------------------------------------
        # Load sale
        # ------------------------------------------------------

        sale = get_sale_for_return(
            sale_id
        )

        if not sale:

            messagebox.showerror(
                "Invoice Not Found",
                "The selected invoice could not be found."
            )

            return

        # ------------------------------------------------------
        # Load sale items
        # ------------------------------------------------------

        items = get_sale_items_for_return(
            sale_id
        )

        if not items:

            messagebox.showinfo(
                "No Items",
                "No sale items were found for this invoice."
            )

            return

        # ======================================================
        # CREATE POPUP
        # ======================================================

        popup = ctk.CTkToplevel(
            self
        )

        popup.title(
            "Sales Return / Refund"
        )

        popup.geometry(
            "760x650"
        )

        popup.minsize(
            760,
            650
        )

        popup.maxsize(
            760,
            650
        )

        popup.resizable(
            False,
            False
        )

        popup.grab_set()

        popup.configure(
            fg_color="#F9FAFB"
        )

        # ======================================================
        # HEADER
        # ======================================================

        ctk.CTkLabel(
            popup,
            text="↩ Sales Return / Refund",
            font=("Poppins", 24, "bold"),
            text_color="#DC2626"
        ).pack(
            pady=(15, 3)
        )

        ctk.CTkLabel(
            popup,
            text=f"Invoice: INV{sale_id:04d}",
            font=("Poppins", 14, "bold"),
            text_color="#374151"
        ).pack(
            pady=(0, 2)
        )

        ctk.CTkLabel(
            popup,
            text=f"Customer: {values[1]}",
            font=("Poppins", 11),
            text_color="#64748B"
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
        # SALE ITEMS CARD
        # ======================================================

        table_card = ctk.CTkFrame(
            content_frame,
            fg_color="white",
            corner_radius=16,
            border_width=1,
            border_color="#E5E7EB"
        )

        table_card.pack(
            fill="x",
            padx=10,
            pady=5
        )

        ctk.CTkLabel(
            table_card,
            text="Invoice Products",
            font=("Poppins", 13, "bold"),
            text_color="#065F46"
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        table_body = ctk.CTkFrame(
            table_card,
            fg_color="transparent"
        )

        table_body.pack(
            fill="both",
            padx=10,
            pady=(0, 10)
        )

        columns = (
            "Product",
            "Sold",
            "Returned",
            "Available",
            "Price"
        )

        item_table = ttk.Treeview(
            table_body,
            columns=columns,
            show="headings",
            height=7
        )

        for col in columns:

            item_table.heading(
                col,
                text=col
            )

        item_table.column(
            "Product",
            width=250
        )

        item_table.column(
            "Sold",
            width=80,
            anchor="center"
        )

        item_table.column(
            "Returned",
            width=90,
            anchor="center"
        )

        item_table.column(
            "Available",
            width=90,
            anchor="center"
        )

        item_table.column(
            "Price",
            width=110,
            anchor="e"
        )

        table_scroll = ttk.Scrollbar(
            table_body,
            orient="vertical",
            command=item_table.yview
        )

        item_table.configure(
            yscrollcommand=table_scroll.set
        )

        item_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        table_scroll.pack(
            side="right",
            fill="y"
        )

        # ======================================================
        # KEEP ITEM DATA
        # ======================================================

        item_lookup = {}

        for item in items:

            (
                sale_item_id,
                product_id,
                product_name,
                sold_quantity,
                selling_price,
                subtotal,
                returned_quantity
            ) = item

            sold_quantity = int(
                sold_quantity
            )

            returned_quantity = int(
                returned_quantity or 0
            )

            available_quantity = (
                sold_quantity
                - returned_quantity
            )

            row_id = item_table.insert(
                "",
                "end",
                values=(
                    product_name.title(),
                    sold_quantity,
                    returned_quantity,
                    available_quantity,
                    f"₹{float(selling_price):,.2f}"
                )
            )

            item_lookup[row_id] = {
                "sale_item_id": sale_item_id,
                "product_id": product_id,
                "product_name": product_name,
                "sold_quantity": sold_quantity,
                "returned_quantity": returned_quantity,
                "available_quantity": available_quantity,
                "selling_price": float(
                    selling_price
                )
            }

        # ======================================================
        # RETURN CONTROL CARD
        # ======================================================

        control_card = ctk.CTkFrame(
            content_frame,
            fg_color="white",
            corner_radius=16,
            border_width=1,
            border_color="#E5E7EB"
        )

        control_card.pack(
            fill="x",
            padx=10,
            pady=(10, 15)
        )

        ctk.CTkLabel(
            control_card,
            text="Return Details",
            font=("Poppins", 13, "bold"),
            text_color="#065F46"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 8)
        )

        # ------------------------------------------------------
        # Return quantity
        # ------------------------------------------------------

        ctk.CTkLabel(
            control_card,
            text="Return Quantity",
            font=("Poppins", 12, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=20
        )

        quantity_var = ctk.StringVar(
            value="1"
        )

        quantity_entry = ctk.CTkEntry(
            control_card,
            textvariable=quantity_var,
            width=130,
            height=38,
            justify="center",
            font=("Poppins", 13, "bold")
        )

        quantity_entry.pack(
            anchor="w",
            padx=20,
            pady=(5, 10)
        )

        # ------------------------------------------------------
        # Refund amount
        # ------------------------------------------------------

        refund_var = ctk.StringVar(
            value="Refund Amount: ₹0.00"
        )

        ctk.CTkLabel(
            control_card,
            textvariable=refund_var,
            font=("Poppins", 15, "bold"),
            text_color="#DC2626"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 5)
        )

        status_var = ctk.StringVar(
            value="Select a product."
        )

        ctk.CTkLabel(
            control_card,
            textvariable=status_var,
            font=("Poppins", 10, "bold"),
            text_color="#B45309"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # ======================================================
        # REFUND PREVIEW
        # ======================================================

        def update_refund_preview(
            event=None
        ):

            selected_item = item_table.selection()

            if not selected_item:

                refund_var.set(
                    "Refund Amount: ₹0.00"
                )

                status_var.set(
                    "Select a product."
                )

                return

            item = item_lookup[
                selected_item[0]
            ]

            try:

                quantity = int(
                    quantity_var.get().strip()
                )

            except ValueError:

                refund_var.set(
                    "Refund Amount: ₹0.00"
                )

                status_var.set(
                    "Enter a valid quantity."
                )

                return

            if quantity <= 0:

                refund_var.set(
                    "Refund Amount: ₹0.00"
                )

                status_var.set(
                    "Quantity must be greater than zero."
                )

                return

            if quantity > item[
                "available_quantity"
            ]:

                refund_var.set(
                    "Refund Amount: ₹0.00"
                )

                status_var.set(
                    f"Maximum returnable quantity: "
                    f"{item['available_quantity']}"
                )

                return

            refund_amount = (
                quantity
                * item["selling_price"]
            )

            refund_var.set(
                f"Refund Amount: ₹{refund_amount:,.2f}"
            )

            status_var.set(
                f"{item['product_name'].title()} • "
                f"{item['available_quantity']} unit(s) available"
            )

        item_table.bind(
            "<<TreeviewSelect>>",
            update_refund_preview
        )

        quantity_entry.bind(
            "<KeyRelease>",
            update_refund_preview
        )

        # ======================================================
        # FIXED BOTTOM BUTTON AREA
        # ======================================================

        bottom_frame = ctk.CTkFrame(
            popup,
            fg_color="white"
        )

        bottom_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        # ======================================================
        # PROCESS RETURN
        # ======================================================

        def process_selected_return():

            selected_item = item_table.selection()

            if not selected_item:

                messagebox.showwarning(
                    "No Product Selected",
                    "Select a product to return.",
                    parent=popup
                )

                return

            item = item_lookup[
                selected_item[0]
            ]

            try:

                quantity = int(
                    quantity_var.get().strip()
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Quantity",
                    "Enter a valid whole number.",
                    parent=popup
                )

                return

            if quantity <= 0:

                messagebox.showerror(
                    "Invalid Quantity",
                    "Return quantity must be greater than zero.",
                    parent=popup
                )

                return

            if quantity > item[
                "available_quantity"
            ]:

                messagebox.showerror(
                    "Return Limit",
                    f"Only {item['available_quantity']} "
                    f"unit(s) can still be returned.",
                    parent=popup
                )

                return

            refund_amount = (
                quantity
                * item["selling_price"]
            )

            confirm = messagebox.askyesno(
                "Confirm Return",
                f"Product: {item['product_name'].title()}\n"
                f"Quantity: {quantity}\n"
                f"Refund: ₹{refund_amount:,.2f}\n\n"
                f"Process this return?",
                parent=popup
            )

            if not confirm:
                return

            try:

                result = process_return(
                    sale_id,
                    item["sale_item_id"],
                    item["product_id"],
                    quantity
                )

            except Exception as error:

                messagebox.showerror(
                    "Return Failed",
                    str(error),
                    parent=popup
                )

                return

            if not result.get(
                "success"
            ):

                messagebox.showerror(
                    "Return Failed",
                    "The return could not be completed.",
                    parent=popup
                )

                return

            refund_amount = result[
                "refund_amount"
            ]

            popup.destroy()

            self.load_reports()

            messagebox.showinfo(
                "Return Successful",
                f"Return completed successfully.\n\n"
                f"Product: {item['product_name'].title()}\n"
                f"Quantity: {quantity}\n"
                f"Refund: ₹{refund_amount:,.2f}"
            )

        # ======================================================
        # BUTTONS
        # ======================================================

        ctk.CTkButton(
            bottom_frame,
            text="↩ Process Return",
            height=42,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            font=("Poppins", 13, "bold"),
            command=process_selected_return
        ).pack(
            side="left",
            expand=True,
            padx=5
        )

        ctk.CTkButton(
            bottom_frame,
            text="Cancel",
            height=42,
            fg_color="#6B7280",
            hover_color="#4B5563",
            font=("Poppins", 13, "bold"),
            command=popup.destroy
        ).pack(
            side="left",
            expand=True,
            padx=5
        )

        quantity_entry.focus_set()
    # ==========================================================
    # LOAD REPORTS
    # ==========================================================

    def load_reports(self):

        # Summary Cards
        revenue = get_today_revenue()
        orders = get_today_orders()
        products = get_total_products()
        low_stock = get_low_stock_products()
        inventory = get_inventory_value()
        payment = get_payment_analytics()
        health = get_inventory_health()
        purchase_analytics = get_today_purchase_analytics()
        profit = get_today_profit_analytics()


        cash = payment["Cash"]["amount"]
        upi = payment["UPI"]["amount"]
        card = payment["Card"]["amount"]

        total = cash + upi + card

        if total > 0:
            self.cash_progress.set(cash / total)
            self.upi_progress.set(upi / total)
            self.card_progress.set(card / total)
        else:
            self.cash_progress.set(0)
            self.upi_progress.set(0)
            self.card_progress.set(0)

        self.healthy_var.set(str(health["healthy"]))
        self.low_inventory_var.set(str(health["low_stock"]))
        self.out_stock_var.set(str(health["out_of_stock"]))
        self.health_score_var.set(f"{health['score']}%")

        score = health["score"]

        self.health_progress.set(score / 100)

        if score >= 80:
            self.health_progress.configure(progress_color="#16A34A")

        elif score >= 50:
            self.health_progress.configure(progress_color="#F59E0B")

        else:
            self.health_progress.configure(progress_color="#DC2626")
                    
        self.cash_var.set(
            f"₹{payment['Cash']['amount']:.2f}"
        )

        self.upi_var.set(
            f"₹{payment['UPI']['amount']:.2f}"
        )

        self.card_var.set(
            f"₹{payment['Card']['amount']:.2f}"
        )

        self.payment_var.set(payment["most_used"])

        self.draw_payment_chart(cash, upi, card)
        
        self.revenue_var.set(f"₹{revenue:.2f}")
        self.orders_var.set(str(orders))
        self.products_var.set(str(products))
        self.low_stock_var.set(str(len(low_stock)))

        self.purchase_value_var.set(
            f"₹{inventory['purchase_value']:.2f}"
        )

        self.selling_value_var.set(
            f"₹{inventory['selling_value']:.2f}"
        )

        self.profit_value_var.set(
            f"₹{inventory['expected_profit']:.2f}"
        )

        self.today_purchase_var.set(
            f"₹{purchase_analytics['amount']:,.2f}"
        )

        self.purchase_count_var.set(
            str(purchase_analytics["count"])
        )

        self.gross_profit_var.set(
            f"₹{profit['gross_profit']:,.2f}"
        )

        self.profit_margin_var.set(
            f"{profit['profit_margin']:.2f}%"
        )


        
        # Best Selling Table
        for row in self.best_table.get_children():
            self.best_table.delete(row)

        for product, sold in get_best_selling_products():
            self.best_table.insert("", "end", values=(product.title(), sold))

        # Top Customers Table
        for row in self.customer_table.get_children():
            self.customer_table.delete(row)

        for name, spent in get_top_customers():
            self.customer_table.insert(
                "",
                "end",
                values=(name.title(), f"₹{float(spent):.2f}")
            )

        # Low Stock Table
        for row in self.low_table.get_children():
            self.low_table.delete(row)

        for name, stock, minimum in low_stock:
            self.low_table.insert(
                "",
                "end",
                values=(name.title(), stock, minimum)
            )

        # Draw monthly revenue chart
        self.draw_monthly_chart()

        now = datetime.now()

        self.last_updated_var.set(
            f"Last Updated • {now.strftime('%I:%M:%S %p')}"
        )

        # =====================================================
        # STOCK MOVEMENT TABLE
        # =====================================================

        # Clear old rows
        for row in self.movement_table.get_children():
            self.movement_table.delete(row)

        movements = get_stock_movements()

        for movement_date, product, movement_type, qty, stock_after in movements:

            movement_type = movement_type.strip().upper()

            if movement_type in ("STOCK IN", "STOCKIN"):
                movement = "🟢 STOCK IN"
                quantity_display = f"+{abs(qty)}"

            elif movement_type == "SALE":
                movement = "🔴 SALE"
                quantity_display = f"-{abs(qty)}"

            else:
                movement = movement_type
                quantity_display = str(qty)

            self.movement_table.insert(
                "",
                "end",
                values=(
                    movement_date.strftime("%d-%b %H:%M"),
                    product.title(),
                    movement,
                    quantity_display,
                    stock_after
                )
            )

        # =====================================================
        # SALES LEDGER
        # =====================================================

        for row in self.sales_table.get_children():
            self.sales_table.delete(row)

        sales = get_sales_history()

        search_text = self.search_var.get().strip().lower()

        for sale_id, customer, payment, total, sale_date in sales:

            customer_name = customer.title() if customer else "Walk-in Customer"

            if search_text:
                if search_text not in customer_name.lower():
                    continue

            invoice = f"INV{sale_id:04d}"

            self.sales_table.insert(
                "",
                "end",
                values=(
                    invoice,
                    customer_name,
                    payment,
                    f"₹{float(total):.2f}",
                    sale_date.strftime("%d-%b-%Y")
                )
            )

        # =====================================================
        # RETURN HISTORY
        # =====================================================

        for row in self.return_table.get_children():
            self.return_table.delete(row)

        returns = get_return_history()

        for (
            return_id,
            sale_id,
            customer,
            product,
            quantity,
            refund_amount,
            return_date
        ) in returns:

            customer_name = (
                customer.title()
                if customer
                else "Walk-in Customer"
            )

            product_name = (
                product.title()
                if product
                else "Unknown Product"
            )

            invoice = (
                f"INV{sale_id:04d}"
            )

            self.return_table.insert(
                "",
                "end",
                values=(
                    return_id,
                    invoice,
                    customer_name,
                    product_name,
                    quantity,
                    f"₹{float(refund_amount):,.2f}",
                    return_date.strftime(
                        "%d-%b-%Y %H:%M"
                    )
                )
            )

        # =====================================================
        # PURCHASE HISTORY
        # =====================================================

        for row in self.purchase_table.get_children():
            self.purchase_table.delete(row)

        purchases = get_purchase_history()

        for (
            purchase_id,
            supplier,
            product,
            quantity,
            purchase_price,
            total_cost,
            purchase_date
        ) in purchases:

            supplier_name = (
                supplier.title()
                if supplier
                else "Unknown Supplier"
            )

            product_name = (
                product.title()
                if product
                else "Unknown Product"
            )

            self.purchase_table.insert(
                "",
                "end",
                values=(
                    purchase_id,
                    supplier_name,
                    product_name,
                    quantity,
                    f"₹{float(purchase_price):,.2f}",
                    f"₹{float(total_cost):,.2f}",
                    purchase_date.strftime(
                        "%d-%b-%Y %H:%M"
                    )
                )
            )
    # ==========================================================
    # DRAW MONTHLY REVENUE CHART
    # ==========================================================

    def draw_monthly_chart(self):

        self.chart_canvas.delete("all")

        monthly_data = get_monthly_sales()

        months = ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"]

        revenue = [0]*12

        for month, amount in monthly_data:
            revenue[month-1] = float(amount)

        canvas_width = 720
        canvas_height = 220

        self.chart_canvas.configure(width=canvas_width)

        max_value = max(revenue) if max(revenue) > 0 else 1

        bar_width = 35
        spacing = 20
        left = 30
        bottom = 180

        # X-axis
        self.chart_canvas.create_line(
            left,
            bottom,
            canvas_width-20,
            bottom,
            fill="#CBD5E1",
            width=2
        )

        for i, value in enumerate(revenue):

            x = left + i*(bar_width+spacing)

            bar_height = (value/max_value)*120

            y = bottom-bar_height

            # Green Bar
            self.chart_canvas.create_rectangle(
                x,
                y,
                x+bar_width,
                bottom,
                fill="#16A34A",
                outline=""
            )

            # Revenue value
            if value > 0:
                self.chart_canvas.create_text(
                    x+bar_width/2,
                    y-12,
                    text=f"₹{int(value)}",
                    fill="#065F46",
                    font=("Poppins",9,"bold")
                )

            # Month label
            self.chart_canvas.create_text(
                x+bar_width/2,
                bottom+15,
                text=months[i],
                fill="#475569",
                font=("Poppins",10)
            )