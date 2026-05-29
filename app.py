import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.graphics.barcodes import code128

def draw_label(buffer, item_name, barcode, qty):
    c = canvas.Canvas(buffer, pagesize=(400, 250))
    # چوارچێوەی لێبڵ
    c.rect(10, 10, 380, 230)
    
    # نووسینی ناو و زانیارییەکان
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20, 210, f"Item: {item_name}")
    
    # کێشانی بارکۆد
    bc = code128.Code128(str(barcode), barHeight=40, barWidth=1.2)
    bc.drawOn(c, 20, 140)
    
    c.setFont("Helvetica", 12)
    c.drawString(20, 120, f"Barcode: {barcode}")
    c.drawString(20, 100, f"Quantity: {qty}")
    
    c.save()
    buffer.seek(0)

st.title("📦 سیستەمی لێبڵی مەخزەن")
uploaded_db = st.file_uploader("فایلی ئێکسڵ باربکە", type=["xlsx"])

if uploaded_db:
    df = pd.read_excel(uploaded_db)
    barcode_input = st.text_input("بارکۆد سکان بکە:")
    
    if barcode_input:
        # گەڕان بەپێی بارکۆد
        result = df[df.iloc[:, 0].astype(str) == barcode_input]
        
        if not result.empty:
            item_name = result.iloc[0].iloc[1]
            qty = st.number_input("عدد:", min_value=1, value=1)
            
            if st.button("🖨️ دروستکردنی لێبڵ"):
                buffer = BytesIO()
                draw_label(buffer, item_name, barcode_input, qty)
                st.download_button("📥 دابەزاندنی لێبڵی PDF", buffer, "label.pdf", "application/pdf")
        else:
            st.error("بارکۆدەکە نەدۆزرایەوە!")
