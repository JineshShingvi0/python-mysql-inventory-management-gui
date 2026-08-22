import customtkinter as ctk
from tkinter import ttk

from backend import (
    get_today_revenue,
    get_today_orders,
    get_total_products,
    get_low_stock_products,
    get_best_selling_products,
    get_top_customers,
    get_monthly_sales 
)


class ReportsPage(ctk.CTkScrollableFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="#F9FAFB",
            corner_radius=0
        )

        self.build_ui()
        self.load_reports()

    # ==========================================================
    # BUILD UI
    # ==========================================================
    def build_ui(self):

        # ---------------- Page Title ----------------
        ctk.CTkLabel(
            self,
            text="📊 Reports & Analytics",
            font=("Poppins", 30, "bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=30, pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="Business insights, sales analytics and inventory health.",
            font=("Poppins", 13),
            text_color="gray40"
        ).pack(anchor="w", padx=30)

        # ---------------- Refresh Button ----------------
        refresh_btn = ctk.CTkButton(
            self,
            text="🔄 Refresh Reports",
            width=180,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.load_reports
        )
        refresh_btn.pack(anchor="e", padx=30, pady=(0, 20))

        # =====================================================
        # SUMMARY CARDS
        # =====================================================

        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30)

        cards_frame.grid_columnconfigure((0, 1), weight=1)

        self.revenue_var = ctk.StringVar(value="₹0")
        self.orders_var = ctk.StringVar(value="0")
        self.products_var = ctk.StringVar(value="0")
        self.low_stock_var = ctk.StringVar(value="0")

        self.create_card(cards_frame, "💰 Today's Revenue",
                         self.revenue_var, 0, 0)

        self.create_card(cards_frame, "🛒 Orders Today",
                         self.orders_var, 0, 1)

        self.create_card(cards_frame, "📦 Products",
                         self.products_var, 1, 0)

        self.create_card(cards_frame, "⚠️ Low Stock Products",
                         self.low_stock_var, 1, 1)

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

    def create_card(self, parent, title, variable, row, column):

        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=18,
            border_width=1,
            border_color="#D1D5DB",
            height=120
        )

        card.grid(row=row, column=column,
                  sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Poppins", 14),
            text_color="#64748B"
        ).pack(anchor="w", padx=18, pady=(18, 6))

        ctk.CTkLabel(
            card,
            textvariable=variable,
            font=("Poppins", 26, "bold"),
            text_color="#065F46"
        ).pack(anchor="w", padx=18)

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

    # ==========================================================
    # LOAD REPORTS
    # ==========================================================

    def load_reports(self):

        # Summary Cards
        revenue = get_today_revenue()
        orders = get_today_orders()
        products = get_total_products()
        low_stock = get_low_stock_products()

        self.revenue_var.set(f"₹{revenue:.2f}")
        self.orders_var.set(str(orders))
        self.products_var.set(str(products))
        self.low_stock_var.set(str(len(low_stock)))

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