import streamlit as st

from ledgerlens.config import settings
from ledgerlens.extraction.field_parser import extract_invoice_fields
from ledgerlens.extraction.ocr_engine import extract_text
from ledgerlens.extraction.text_normalizer import normalize_ocr_text
from ledgerlens.ingestion.document_loader import create_document_preview
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

# session state handling
if "show_image" not in st.session_state:
    st.session_state.show_image = False
if "success_dialog_shown" not in st.session_state:
    st.session_state.success_dialog_shown = False
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "invoice_fields" not in st.session_state:
    st.session_state.invoice_fields = ""


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
st.write("Phase 2 in progress - Structuring Field Extraction and Review the OCR text.")
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
def reset_preview():
    st.session_state.show_image = False
    st.session_state.success_dialog_shown = False
    """Clear extracted fields and review widget keys from session state."""
    keys_to_clear = [
        "extracted_text",
        "invoice_fields",
        "review_vendor",
        "review_invoice_number",
        "review_invoice_date",
        "review_subtotal",
        "review_tax",
        "review_total",
        "review_currency",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


st.header("Please upload the invoice document for the analysis.")
uploaded_file = st.file_uploader(
    "Choose a file",
    type=settings.allowed_document_extensions + settings.allowed_image_extensions,
    max_upload_size=settings.max_upload_size_mb,
    accept_multiple_files=False,
    on_change=reset_preview,
)


if uploaded_file is not None:
    validation_result = validate_upload(
        file_name=uploaded_file.name,
        file_size_bytes=uploaded_file.size,
    )

    if validation_result.is_valid:
        if not st.session_state.success_dialog_shown:
            st.session_state.success_dialog_shown = True
            success_upload_dialog(uploaded_file, validation_result.extension)

        file_bytes = uploaded_file.getvalue()
        preview_result = create_document_preview(
            file_bytes, validation_result.extension
        )

        ## --- Preview image section ----

        if not preview_result.is_successful:
            st.error(f"There is an error\n : {preview_result.error_message}")
        else:
            if st.button("📸 Preview the file"):
                st.session_state.show_image = True

            if st.session_state.show_image:
                # hide button
                if st.button("Hide Image"):
                    st.session_state.show_image = False
                    st.rerun()
                if preview_result.page_count == 1:
                    st.image(preview_result.image, caption="Only one page")
                else:
                    st.image(
                        preview_result.image,
                        caption=f"Showing 1 out of {preview_result.page_count} pages",
                    )

            ## --- Extract image section ----
            if st.button("📸 Extract text"):
                text = extract_text(preview_result.image)
                if text.is_successful:
                    normalized_text = normalize_ocr_text(text.text)
                    st.session_state.extracted_text = normalized_text

                else:
                    st.error(f"🚨Error Message: {text.error_message}")

            ## --- Extract invoice fields section ----
            if st.button("📸 Extract invoice fields"):
                if not st.session_state.get("extracted_text"):
                    st.warning("Please extract the text first.")
                else:
                    with st.spinner("Extracting structured fields..."):
                        st.session_state.invoice_fields = extract_invoice_fields(
                            st.session_state.extracted_text
                        )

    else:
        error_upload_dialog(uploaded_file, validation_result.error_message)
        st.session_state.show_image = False
        st.session_state.success_dialog_shown = False

if "extracted_text" in st.session_state and st.session_state.extracted_text:
    st.subheader("Review Raw Extracted Information")
    st.text_area(
        "📝 Extracted Text",
        value=st.session_state.extracted_text,
        height=300,
        disabled=False,
        key="ocr_output",
    )


def format_ui_value(val) -> str:
    """Format any extracted value (Decimal, Date, None) into a display string."""
    if val is None:
        return ""
    return str(val)


# --- Extract Image / Fields Section ---

if st.button("📸 Extract invoice fields"):
    if not st.session_state.get("extracted_text"):
        st.warning("Please extract the raw text first.")
    else:
        with st.spinner("Extracting structured fields..."):
            # 1. Run extraction and store domain model (or None)
            fields = extract_invoice_fields(st.session_state.extracted_text)
            st.session_state.invoice_fields = fields

            # 2. Populate the review keys directly into session state.
            # This ensures that re-running extraction updates the widget state explicitly!
            st.session_state.review_vendor = format_ui_value(
                getattr(fields, "vendor", None)
            )
            st.session_state.review_invoice_number = format_ui_value(
                getattr(fields, "invoice_number", None)
            )
            st.session_state.review_invoice_date = format_ui_value(
                getattr(fields, "invoice_date", None)
            )
            st.session_state.review_subtotal = format_ui_value(
                getattr(fields, "subtotal", None)
            )
            st.session_state.review_tax = format_ui_value(getattr(fields, "tax", None))
            st.session_state.review_total = format_ui_value(
                getattr(fields, "total", None)
            )
            st.session_state.review_currency = format_ui_value(
                getattr(fields, "currency", None)
            )


# --- Review & Edit Extracted Fields Section ---

if st.session_state.get("invoice_fields") is not None:
    st.subheader("Review Extracted Information")
    st.caption("Inspect and correct any fields before committing.")

    st.text_input("Vendor", key="review_vendor")
    st.text_input("Invoice Number", key="review_invoice_number")
    st.text_input("Invoice Date", key="review_invoice_date")
    st.text_input("Subtotal", key="review_subtotal")
    st.text_input("Tax", key="review_tax")
    st.text_input("Total", key="review_total")
    st.text_input("Currency", key="review_currency")
