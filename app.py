import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# GST Rate
GST_RATE = 0.18  # 18% GST standard


# Initialize session variables

if "items_list" not in st.session_state:
    st.session_state.items_list = []

if "invoice_no" not in st.session_state:
    st.session_state.invoice_no = 1

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

if "customer_phone" not in st.session_state:
    st.session_state.customer_phone = ""

# Input fields state
if "item_name" not in st.session_state:
    st.session_state.item_name = ""
if "qty" not in st.session_state:
    st.session_state.qty = 1
if "price" not in st.session_state:
    st.session_state.price = 0

# App Title

st.title("Shopping Bill System")

# Customer Details

st.subheader("Customer Details")
col1, col2 = st.columns(2)
with col1:
    st.session_state.customer_name = st.text_input("Customer Name", st.session_state.customer_name)
with col2:
    st.session_state.customer_phone = st.text_input("Phone Number", st.session_state.customer_phone)


# Add Items

st.subheader("➕ Add Items")
col1, col2, col3 = st.columns(3)
with col1:
    st.session_state.item_name = st.text_input("Item Name", st.session_state.item_name)
with col2:
    st.session_state.qty = st.number_input("Quantity", min_value=1, step=1, value=st.session_state.qty)
with col3:
    st.session_state.price = st.number_input("Price per Unit", min_value=0, step=1, value=st.session_state.price)

if st.button("Add Item"):
    if st.session_state.item_name.strip() == "":
        st.warning("Enter an item name.")
    elif st.session_state.price <= 0:
        st.warning("Enter a valid price.")
    else:
        subtotal = st.session_state.qty * st.session_state.price
        st.session_state.items_list.append({
            "Item": st.session_state.item_name,
            "Quantity": st.session_state.qty,
            "Price": st.session_state.price,
            "Subtotal": subtotal
        })
        st.success(f"✅ Added {st.session_state.item_name} ({st.session_state.qty} × {st.session_state.price} = {subtotal})")

        # Reset input fields
        st.session_state.item_name = ""
        st.session_state.qty = 1
        st.session_state.price = 0


# Display Items

if st.session_state.items_list:
    st.subheader("Items in Bill")
    for idx, item in enumerate(st.session_state.items_list):
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
        with col1:
            st.write(item["Item"])
        with col2:
            st.write(item["Quantity"])
        with col3:
            st.write(item["Price"])
        with col4:
            st.write(item["Subtotal"])
        with col5:
            if st.button("❌ Delete", key=f"del_{idx}"):
                st.session_state.items_list.pop(idx)
                st.success("Item deleted!")

    
    # Calculate totals
    
    subtotal = sum(item["Subtotal"] for item in st.session_state.items_list)
    tax = subtotal * GST_RATE
    grand_total = subtotal + tax
    st.subheader(f" Subtotal: ₹ {subtotal:.2f} | GST (18%): ₹ {tax:.2f} | Grand Total: ₹ {grand_total:.2f}")

    
    # Prepare CSV
   
    df = pd.DataFrame(st.session_state.items_list)
    df["GST"] = df["Subtotal"] * GST_RATE
    df["Grand Total"] = df["Subtotal"] + df["GST"]

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Bill as CSV",
        data=csv,
        file_name=f"invoice_{st.session_state.invoice_no:03d}.csv",
        mime="text/csv",
    )

    
    # PDF Receipt
    
    def create_pdf_receipt(df, subtotal, tax, grand_total,
                           invoice_no, customer_name, customer_phone):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Shop Name
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, height - 50, "My Shop Receipt")

        # Invoice & Date
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 90, f"Invoice No: INV-{invoice_no:03d}")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.drawRightString(width - 50, height - 90, f"Date: {now}")

        # Customer Details
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 120, f"Customer: {customer_name}")
        c.drawRightString(width - 50, height - 120, f"Phone: {customer_phone}")

        # Table Header
        y = height - 150
        row_height = 20
        table_x = 50
        table_width = 500
        c.setLineWidth(1)

        # Header Box
        c.rect(table_x, y - 5, table_width, row_height, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(table_x + 5, y, "Item")
        c.drawRightString(table_x + 200, y, "Qty")
        c.drawRightString(table_x + 300, y, "Price")
        c.drawRightString(table_x + 400, y, "Subtotal")
        y -= row_height

        # Table Items
        c.setFont("Helvetica", 12)
        for _, row in df.iterrows():
            c.drawString(table_x + 5, y, str(row["Item"]))
            c.drawRightString(table_x + 200, y, str(row["Quantity"]))
            c.drawRightString(table_x + 300, y, f"₹ {row['Price']}")
            c.drawRightString(table_x + 400, y, f"₹ {row['Subtotal']:.2f}")
            y -= row_height

        # Totals Boxed
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        # Subtotal
        c.rect(table_x, y - 5, table_width, row_height, stroke=1, fill=0)
        c.drawString(table_x + 5, y, "Subtotal")
        c.drawRightString(table_x + 400, y, f"₹ {subtotal:.2f}")
        y -= row_height
        # GST
        c.rect(table_x, y - 5, table_width, row_height, stroke=1, fill=0)
        c.drawString(table_x + 5, y, f"GST ({int(GST_RATE*100)}%)")
        c.drawRightString(table_x + 400, y, f"₹ {tax:.2f}")
        y -= row_height
        # Grand Total
        c.rect(table_x, y - 5, table_width, row_height, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(table_x + 5, y, "Grand Total")
        c.drawRightString(table_x + 400, y, f"₹ {grand_total:.2f}")

        # Footer
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(width / 2, 50, "Thank you for shopping with us!")

        c.save()
        buffer.seek(0)
        return buffer

    pdf = create_pdf_receipt(df, subtotal, tax, grand_total,
                             st.session_state.invoice_no,
                             st.session_state.customer_name,
                             st.session_state.customer_phone)

    st.download_button(
        label="Download Bill as PDF",
        data=pdf,
        file_name=f"invoice_{st.session_state.invoice_no:03d}.pdf",
        mime="application/pdf",
    )

    
    # Finalize Bill
  
    if st.button("Finalize & Reset Bill"):
        st.session_state.items_list = []
        st.session_state.invoice_no += 1
        st.session_state.customer_name = ""
        st.session_state.customer_phone = ""
        st.success("✅ Bill finalized. Ready for new customer!")
