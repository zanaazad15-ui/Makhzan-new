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
