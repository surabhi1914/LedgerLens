"""LedgerLens Streamlit application entry point."""

from src.ledgerlens.config import settings
import streamlit as st

st.set_page_config(page_title="LedgerLens", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

st.title("LedgerLens")
st.write("An AI-assisted invoice extraction and expense management project.")

st.sidebar.title("About the Page")
st.sidebar.markdown(" Explain that the current development phase will support: Upload, Validation, Preview and RAW OCR ")
st.sidebar.warning(" ⚠️ Structured field extraction, categorization, and duplicate detection are not implemented yet.")


st.header("Planned Workflow")
df_target = {
    1: "Upload an invoice.",
    2: "Extract invoice text and fields.",
    3: "Review and correct the result.",
    4: "Categorize the expense.",
    5: "Check for duplicates.",
    6: "View spending insights."
}
st.table(data = df_target, width ="content")


st.header("Current Development Phase")
st.write("Phase 1 in progress: building the invoice upload and raw OCR workflow.")
with st.expander("Development details"):
    st.write(f"App Name : {settings.app_name}")
    st.write(f"Environment : {settings.environment}")
    st.write(f"allowed image extensions: {settings.allowed_image_extensions}")
    st.write(f"allowed document extensions: {settings.allowed_document_extensions}")
    st.write(f"max upload size (MB): {settings.max_upload_size_mb}")


st.warning("Privacy notice \n Use sample or synthetic invoices during development. Do not upload documents containing sensitive financial or personal information.", icon="🛡️")
