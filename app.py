import streamlit as st
import pandas as pd

# ناوی بەرنامە
st.title("📦 سیستەمی مەخزەن")

# بەشی بارکردنی فایل
uploaded_db = st.file_uploader("فایلی ئێکسڵ باربکە", type=["xlsx"])

if uploaded_db:
    try:
        df = pd.read_excel(uploaded_db)
        st.success("✅ فایلەکە بە سەرکەوتوویی بارکرا")
        
        # پیشاندانی زانیاری
        st.write("زانیاری ناو فایلەکە:")
        st.dataframe(df.head())
        
        # بەشی گەڕان بەپێی بارکۆد
        barcode = st.text_input("بارکۆد سکان بکە:")
        if barcode:
            st.info(f"سکانکرا: {barcode}")
            
    except Exception as e:
        st.error(f"هەڵەیەک ڕوویدا: {e}")
        
import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas

def create_pdf(item_name, barcode, qty):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(300, 200))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20, 160, f"Item: {item_name}")
    c.drawString(20, 130, f"Barcode: {barcode}")
    c.drawString(20, 100, f"Quantity: {qty}")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

st.title("📦 سیستەمی لێبڵی مەخزەن")

uploaded_db = st.file_uploader("فایلی ئێکسڵ باربکە", type=["xlsx"])

if uploaded_db:
    df = pd.read_excel(uploaded_db)
    # پیشاندانی ناوی ستوونەکان بۆ ئەوەی دڵنیابیت
    st.write("ناوی ستوونەکان:", df.columns.tolist())
    
    barcode_input = st.text_input("بارکۆد سکان بکە:")
    
    if barcode_input:
        # گەڕان بەپێی بارکۆد (لێرەدا تەنها یەکەم ستوون بەکاردێنین بۆ بارکۆد)
        barcode_col = df.columns[0] 
        name_col = df.columns[1]
        
        result = df[df[barcode_col].astype(str) == barcode_input]
        
        if not result.empty:
            item_name = result.iloc[0][name_col]
            qty = st.number_input("عدد:", min_value=1, value=1)
            
            if st.button("💾 دروستکردنی PDF"):
                pdf_file = create_pdf(item_name, barcode_input, qty)
                st.download_button(
                    label="📥 دابەزاندنی لێبڵ",
                    data=pdf_file,
                    file_name="label.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("بارکۆدەکە نەدۆزرایەوە!")
