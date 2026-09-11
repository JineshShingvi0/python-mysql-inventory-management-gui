# 🛒 Shingvi Supermart — Inventory Management & POS Billing Software

A professional **Inventory Management and Point of Sale (POS)** desktop application built using **Python, CustomTkinter, MySQL, and ReportLab**.

Designed for retail supermarkets and stores to manage products, billing, inventory, suppliers, customers, and loyalty rewards in one place.

---

## ✨ Features

### 🛍 Billing & POS

* Barcode scanner support.
* Fast billing with keyboard shortcuts.
* Customer phone auto-fetch.
* Loyalty points earning & redemption.
* Multiple payment methods (Cash, UPI, Card).
* GST Enable / Disable support.
* Professional Thermal Printer (80mm POS) invoices.
* QR Code payment on invoice.

### 📦 Inventory Management

* Product management.
* Barcode generation.
* Low stock alerts.
* Stock movement history.
* Purchase price & selling price tracking.
* Purchase management.

### 👥 Customer Management

* Customer database.
* Loyalty points system.
* Purchase history.
* Total spending tracking.

### 🚚 Supplier Management

* Supplier records.
* Purchase entries.
* Purchase history.

### 📊 Dashboard & Reports

* Today's sales.
* Weekly sales graph.
* Inventory value.
* Top-selling products.
* Healthy / Low / Out-of-stock indicators.
* Business snapshot.

---

## 🛠 Tech Stack

| Technology    | Usage                 |
| ------------- | --------------------- |
| Python 3.11   | Core Application      |
| CustomTkinter | Modern Desktop GUI    |
| MySQL         | Database              |
| ReportLab     | PDF & Thermal Invoice |
| Pillow        | Image Handling        |
| Git & GitHub  | Version Control       |

---

## ⌨ Keyboard Shortcuts

| Shortcut | Action                       |
| -------- | ---------------------------- |
| F2       | Product Selection            |
| F3       | Barcode Scanner              |
| F4       | Quantity                     |
| F5       | Customer Phone               |
| Enter    | Add Product                  |
| + / -    | Increase / Decrease Quantity |
| Delete   | Remove Item                  |
| Ctrl + B | Generate Bill                |

---

## 🚀 Future Roadmap

* Settings page for business customization.
* WhatsApp invoice sharing.
* Automatic thermal printer printing.
* Backup & Restore.
* Multi-store support.

---

## 👨‍💻 Developed By

**Jinesh Shingvi**

Python Developer • Automation Enthusiast • Inventory & Billing Solutions


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