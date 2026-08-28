# 🛒 Shingvi Supermart — Inventory Management & POS System

A desktop-based **Inventory Management and Point of Sale (POS) system** built with Python, CustomTkinter, and MySQL.

The application is designed for retail-store management and combines **billing, inventory, customers, suppliers, loyalty rewards, barcode management, sales analytics, purchases, and returns** in one interface.

---

## ✨ Features

### 🏠 Dashboard
- Today's revenue
- Orders today
- Inventory value
- Expected inventory profit
- Inventory health
- Low-stock and out-of-stock alerts
- Sales target tracking
- Recent sales
- Best-selling products
- Weekly revenue analytics
- Smart business insights
- Live date and time
- Store status indicator

### 📦 Product Management
- Add products
- Update products
- Delete unused products
- Search by product name, category, or barcode
- Purchase price and selling price management
- Minimum-stock levels
- Stock quantity management
- Internal barcode generation
- Barcode assignment and replacement
- Barcode copying
- Barcode preview
- Barcode PNG generation
- Barcode label generation

### 🛒 Billing / POS
- Customer billing
- Multiple products per bill
- Quantity management
- Cash, UPI, and Card payment methods
- GST calculation
- Percentage-based discounts
- Live bill summary
- Live receipt preview
- Barcode scanning
- Automatic stock deduction
- Invoice PDF generation
- Keyboard shortcuts for faster billing

### ⭐ Loyalty Program
- Customers earn loyalty points based on bill value
- **1 loyalty point for every ₹100 of final bill amount**
- **50 loyalty points = ₹10 discount**
- Redemption restricted to multiples of 50 points
- Customer point balance displayed during billing
- Loyalty redemption and earning handled as part of the billing transaction

### 👤 Customer Management
- Add customers
- Update customer information
- Delete customers when allowed
- Search by name or phone number
- Loyalty point tracking
- Customer profile
- Total orders
- Total spending
- Last purchase date
- Customer purchase history

### 🏭 Supplier Management
- Add suppliers
- Update suppliers
- Delete suppliers when allowed
- Search suppliers
- Supplier details
- Total purchase value
- Purchase transaction count
- Total units supplied
- Last purchase information
- Supplier purchase history

### 📊 Reports & Analytics
- Daily revenue
- Daily orders
- Product count
- Low-stock products
- Cash / UPI / Card analytics
- Payment distribution
- Inventory health score
- Inventory purchase value
- Inventory selling value
- Expected inventory profit
- Today's purchases
- Purchase transaction count
- Today's gross profit
- Profit margin
- Best-selling products
- Top customers
- Monthly revenue chart
- Weekly sales data
- Stock movement history
- Sales ledger
- Purchase history
- Return history
- Sales returns and refunds

### ↩ Returns / Refunds
- Select an invoice from the sales ledger
- View sold and returned quantities
- Calculate refundable quantity
- Process product returns
- Automatically return stock to inventory
- Record return history
- Update stock movement history
- Return-aware profit calculations

---

## 🧱 Technology Stack

- **Python 3**
- **CustomTkinter** — GUI
- **Tkinter ttk** — tables and widgets
- **MySQL** — database
- **mysql-connector-python** — MySQL connectivity
- **Pillow** — image and barcode preview handling
- **python-barcode** — barcode generation
- **ReportLab** — invoice and barcode-label PDF generation

---

## 📁 Project Structure

```text
inventory-management-gui/
│
├── app.py
├── backend.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── assets/
│   └── logo.png
│
└── gui/
    ├── __init__.py
    ├── billing.py
    ├── customers.py
    ├── products.py
    ├── reports.py
    └── suppliers.py