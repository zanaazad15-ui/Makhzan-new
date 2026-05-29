import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.graphics.barcodes import code128

def draw_table_label(buffer, item_name, barcode, qty, expiry_date):
    # قەبارەی لاپەڕەی لێبڵ
    c = canvas.Canvas(buffer, pagesize=(450, 320))
    c.setLineWidth(1.5)
    c.rect(10, 10, 430, 300)
    
    # هێڵە ئاسۆییەکان
    c.line(10, 275, 440, 275)
    c.line(10, 220, 440, 220)
    c.line(10, 165, 440, 165)
    c.line(10, 110, 440, 110)
    c.line(10, 55, 440, 55)
    
    # هێڵە ستوونییەکان
    c.line(150, 10, 150, 275)
    c.line(230, 220, 230, 275)
    
    # ١. ناوی بابەت (Item)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20, 285, "Item")
    c.setFont("Times-Bold", 12) # فۆنتی ستاندارد بۆ عەرەبی و کوردی
    c.drawRightString(430, 285, f"{item_name}")
    
    # ٢. بارکۆد (Barc.)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(20, 240, "Barc.")
    try:
        bc128 = code128.Code128(str(barcode), barHeight=22, barWidth=1.1)
        bc128.drawOn(c, 15, 223)
    except:
        pass
    
    c.setFont("Helvetica", 34)
    c.drawString(180, 235, "J")
    
    short_barcode = str(barcode)[-7:] if len(str(barcode)) >= 7 else str(barcode)
    c.setFont("Helvetica-Bold", 38)
    c.drawRightString(430, 232, f"{short_barcode}")
    
    # ٣. عدد (PCS.)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(20, 185, "PCS.")
    try:
        qty_bc = code128.Code128(str(qty), barHeight=18, barWidth=1.2)
        qty_bc.drawOn(c, 20, 170)
    except:
        pass
    c.setFont("Helvetica-Bold", 46)
    c.drawRightString(430, 175, f"{qty}")
    
    # ٤. بەرهەمهێنان (PRO.)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(20, 130, "PRO.")
    pro_date = datetime.now().strftime("%d-%m-%Y")
    c.setFont("Helvetica-Bold", 36)
    c.drawRightString(430, 122, f"{pro_date}")
    
    # ٥. بەسەرچوون (EXP.)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(20, 75, "EXP.")
    try:
        exp_bc = code128.Code128(str(expiry_date), barHeight=14, barWidth=1.0)
        exp_bc.drawOn(c, 15, 60)
    except:
        pass
    c.setFont("Helvetica-Bold", 36)
    c.drawRightString(430, 67, f"{expiry_date}")
    
    # ٦. کاتی وەرگرتن (DATA OF RECEIVING)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20, 25, "DATA OF RECEIVING")
    now_str = datetime.now().strftime("%d-%m-%Y    %I:%M %p")
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(430, 22, f"{now_str}")
    
    c.showPage()
    c.save()

# شاشەی ماڵپەڕەکە
st.set_page_config(page_title="سیستەمی مەخزەن", layout="centered")
if 'db' not in st.session_state:
    st.session_state.db = None

st.title("📦 سیستەمی لێبڵی جەرد و مەخزەن")
st.sidebar.header("⚙️ داتابەیس")
uploaded_db = st.sidebar.file_uploader("بارکردنی فایلی ئێکسڵ", type=["xlsx"])

if uploaded_db:
    try:
        st.session_state.db = pd.read_excel(uploaded_db)
        st.sidebar.success("✅ داتابەیس بارکرا!")
    except:
        st.sidebar.error("❌ کێشەیەک لە فایلەکەدا هەیە")

if st.session_state.db is None:
    st.warning("⚠️ تکایە سەرەتا فایلی ئێکسڵەکە لە لای چەپەوە باربکە.")
else:
    barcode_input = st.text_input("بارکۆد سکان بکە:").strip()
    if barcode_input:
        df = st.session_state.db
        barcode_col = [col for col in df.columns if 'barcode' in col.lower()]
        name_col = [col for col in df.columns if 'name' in col.lower()]
        
        if barcode_col and name_col:
            result = df[df[barcode_col[0]].astype(str) == barcode_input]
            if not result.empty:
                item_name = result.iloc[0][name_col[0]]
                st.info(f"📋 کاڵای دۆزراوە: {item_name}")
                expiry = st.text_input("تاریخ (EXP):", value="20-12-2026")
                qty = st.number_input("عدد (PCS):", min_value=1, value=660, step=1)
                
                if st.button("💾 دروستکردنی لێبڵ"):
                    buffer = BytesIO()
                    draw_table_label(buffer, item_name, barcode_input, qty, expiry)
                    buffer.seek(0)
                    st.download_button(
                        label="🖨️ دابەزاندنی لێبڵی کۆتایی PDF",
                        data=buffer,
                        file_name=f"Label_{barcode_input}.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error("⚠️ ئەم بارکۆدە لە داتابەیسدا نییە!")
        else:
            st.error("❌ ستوونی ناو یان بارکۆد لە فایلی ئێکسڵەکەدا نەدۆزرایەوە!")
