# 🧾 Shopping Bill System

A simple **billing and invoicing web app** built with [Streamlit](https://streamlit.io/).It allows shopkeepers or small businesses to quickly:

- Add items with price and quantity
- Auto-calculate subtotal, GST (18%), and grand total
- Generate and download invoices in **CSV** and **PDF** formats
- Manage multiple customers with automatic invoice numbering

---

## 🚀 Features

- 👤 **Customer Details** – Save customer name and phone number
- ➕ **Add Items** – Add items with quantity and price
- 🛒 **View Items** – See items in the bill with an option to delete
- 💰 **Auto Calculations** – Subtotal + GST (18%) + Grand Total
- 📥 **Download Options** – Export bill as **CSV** or **PDF receipt**
- 🔁 **Invoice Management** – Auto-increment invoice number, reset after billing

---

## 🛠️ Installation

1. **Clone this repository**

   ```bash
   git clone https://github.com/yourusername/shopping-bill-system.git
   cd shopping-bill-system
   ```
2. **Create and activate a virtual environment** (optional but recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## 📦 Requirements

The app requires the following Python packages (already listed in `requirements.txt`):

```
streamlit
pandas
reportlab
```

> ✅ Recommended Python version: **3.8 or above**

---

## ▶️ Usage

Run the app using Streamlit:

```bash
streamlit run app.py
```

Then open your browser at **http://localhost:8501**

---

## 📂 Project Structure

```
📦 shopping-bill-system
 ┣ 📂 screenshots          # Store screenshots and sample invoices
 ┃ ┣ 📜 UI_1.png
 ┃ ┣ 📜 UI_2.png
 ┃ ┣ 📜 UI_3.png
 ┃ ┣ 📜 UI_4.png
 ┣ 📜 app.py               # Main Streamlit app
 ┣ 📜 requirements.txt     # Python dependencies
 ┣ 📜 README.md            # Documentation
```

---

## 🧾 Invoice Output

- **CSV** → Tabular data of items, subtotal, GST, and total
- **PDF** → Printable receipt with customer details, items, and totals

---


Feel free to use, modify, and distribute.

---

👉 Perfect for **small shops, billing counters, and quick receipt generation**!
