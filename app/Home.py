import streamlit as st

from ledgerlens.config import settings
from ledgerlens.ingestion.file_validator import validate_upload

# -------Intro config-------
st.set_page_config(
    page_title=settings.app_name,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title(settings.app_name)
st.write("An AI-assisted invoice extraction and expense management project.")

# -------CSS for the page-------
# Custom CSS for background gradient
st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(120deg, #f3e8ff 0%, #e0e7ff 100%);
}
</style>
""",
    unsafe_allow_html=True,
)


# -------dialog section-------
@st.dialog("✅ Upload Successful")
def success_upload_dialog(uploaded_file, extension):
    st.write(
        f"☑️ File '{uploaded_file.name}' uploaded successfully."
        "\n\n"
        "File Details are displayed below.\n"
        f"\n- Filename: {uploaded_file.name}"
        f"\n- File type: {uploaded_file.type}"
        f"\n- File size: {uploaded_file.size / (1024 * 1024):.2f} MB"
        f"\n- File extension: {extension}"
    )


@st.dialog("🚫 Upload Failed")
def error_upload_dialog(uploaded_file, error_message):
    st.write(f"🚨 Error uploading file '{uploaded_file.name}': {error_message}")


# -------Sidebar content-------
st.sidebar.title("About the Page")
st.sidebar.markdown(
    "Explain that the current development phase will support: "
    "\n - Upload"
    "\n - Validation"
    "\n - Preview"
    "\n - RAW OCR"
)
st.sidebar.info(
    " ⚠️ Structured field extraction, categorization, and duplicate detection"
    " are not implemented yet."
)


# -------content-------
st.header("Planned Workflow")
st.markdown(
    """
<table style="width:fit-content; border-collapse: collapse; border: 1px solid black;">
<th> 
No.
</th>
<th>
Allowed operations for now
</th>
<tr>
<td style="text-align:center;"><strong>1</strong></td>
<td style="text-align:center;"><strong>Upload</strong></td>
</tr>
<tr>
<td style="text-align:center;"><strong>2</strong></td>
<td style="text-align:center;"><strong>Validation</strong></td>
</tr>
<td style="text-align:center;"><strong>3</strong></td>
<td style="text-align:center;"><strong>Preview</strong></td>
</tr>
<tr>
<td style="text-align:center;"><strong>4</strong></td>
<td style="text-align:center;"><strong>RAW OCR</strong></td>
</tr>
</table>

""",
    unsafe_allow_html=True,
)

extensions = (", ".join(settings.allowed_document_extensions)).upper()
image_extensions = (", ".join(settings.allowed_image_extensions)).upper()

# -------Development details-------
st.header("Current Development Phase")
st.write("Phase 1 in progress: building the invoice upload and raw OCR workflow.")
with st.expander("Development details"):
    st.write(f"App Name : {settings.app_name}")
    st.write(f"Environment : {settings.environment}")
    st.write(f"allowed image extensions: {image_extensions}")
    st.write(f"allowed document extensions: {extensions}")
    st.write(f"Maximum upload size : {settings.max_upload_size_mb} MB")


st.warning(
    "Privacy notice: "
    "Use sample or synthetic invoices during development. "
    "Do not upload documents containing sensitive financial "
    "or personal information.",
    icon="🛡️",
)

# -------Main uploading section-------
st.header("Please upload the invoice document for the analysis.")
uploaded_file = st.file_uploader(
    "Choose a file",
    type=settings.allowed_document_extensions + settings.allowed_image_extensions,
    max_upload_size=settings.max_upload_size_mb,
    accept_multiple_files=False,
)


if uploaded_file is not None:
    validation_result = validate_upload(
        file_name=uploaded_file.name,
        file_size_bytes=uploaded_file.size,
    )
    if validation_result.is_valid:
        success_upload_dialog(uploaded_file, validation_result.extension)

    else:
        error_upload_dialog(uploaded_file, validation_result.error_message)
