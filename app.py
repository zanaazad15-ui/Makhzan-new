import streamlit as st
import pandas as pd
from io import BytesIO

# لێرەدا دەگەڕێین بەدوای ئەوەی ئایا reportlab هەیە یان نا
try:
    from reportlab.pdfgen import canvas
    from reportlab.graphics.barcodes import code128
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

st.title("📦 سیستەمی لێبڵی مەخزەن")

if not HAS_REPORTLAB:
    st.error("تکایە دڵنیابەرەوە کە 'reportlab' لە فایلی requirements.txt نووسراوە.")
