import pandas as pd
import streamlit as st

from ledgerlens.config import settings
from ledgerlens.extraction.consistency_validator import check_invoice_consistency
from ledgerlens.extraction.field_parser import extract_invoice_fields
from ledgerlens.extraction.ocr_engine import extract_text
from ledgerlens.extraction.review_validator import validate_reviewed_invoice
from ledgerlens.ingestion.document_loader import create_document_preview
from ledgerlens.ingestion.file_validator import validate_upload
from ledgerlens.persistence.database import initialize_database
from ledgerlens.persistence.invoice_repository import list_invoices, save_invoice
from ledgerlens.persistence.models import InvoiceRecord


# -----Setup database-----
@st.cache_resource
def setup_database() -> None:
    """Initialize database tables once per app session lifetime."""
    initialize_database()


setup_database()
# ------- Page config -------
st.set_page_config(
    page_title=settings.app_name,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title(settings.app_name)
st.write("An AI-assisted invoice extraction and expense management project.")


# ------- CSS -------
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


# ------- Session-state initialization -------
if "show_image" not in st.session_state:
    st.session_state.show_image = False
if "success_dialog_shown" not in st.session_state:
    st.session_state.success_dialog_shown = False
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "invoice_fields" not in st.session_state:
    st.session_state.invoice_fields = None
if "confirmed_invoice" not in st.session_state:
    st.session_state.confirmed_invoice = None


# ------- Dialog functions -------
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


# ------- Sidebar / page description -------
st.sidebar.title("About the Page")
st.sidebar.markdown(
    "Explain that the current development phase will support: "
    "\n - Upload"
    "\n - Validation"
    "\n - Preview"
    "\n - RAW OCR"
)
# st.sidebar.info(
#     " ⚠️ Structured field extraction, categorization, and duplicate detection"
#     " are not implemented yet."
# )


# ------- Planned Workflow / Development details / Privacy warning -------
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


# ------- Helper functions -------
def clear_structured_extraction_state():
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
        "confirmed_invoice",
        "review_discount",
        "file_name",
        "saved_invoice_id",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


def reset_preview():
    st.session_state.show_image = False
    st.session_state.success_dialog_shown = False
    clear_structured_extraction_state()


def format_ui_value(val) -> str:
    """Format any extracted value (Decimal, Date, None) into a display string."""
    if val is None:
        return ""
    return str(val)


def invalidate_confirmation():
    st.session_state.confirmed_invoice = None
    st.session_state.saved_invoice_id = None


# ------- UPLOAD -------
st.header("Please upload the invoice document for the analysis.")
uploaded_file = st.file_uploader(
    "Choose a file",
    type=settings.allowed_document_extensions + settings.allowed_image_extensions,
    max_upload_size=settings.max_upload_size_mb,
    accept_multiple_files=False,
    on_change=reset_preview,
)


# ------- VALIDATION -------
if uploaded_file is not None:
    validation_result = validate_upload(
        file_name=uploaded_file.name,
        file_size_bytes=uploaded_file.size,
    )
    st.session_state.file_name = uploaded_file.name
    if validation_result.is_valid:
        if not st.session_state.success_dialog_shown:
            st.session_state.success_dialog_shown = True
            success_upload_dialog(uploaded_file, validation_result.extension)

        file_bytes = uploaded_file.getvalue()

        # ------- PREVIEW -------
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

            # ------- OCR -------
            ## --- Extract image section ----
            if st.button("📸 Extract text"):
                text = extract_text(preview_result.image)
                if text.is_successful:
                    clear_structured_extraction_state()
                    st.session_state.extracted_text = text.text

                else:
                    st.error(f"🚨Error Message: {text.error_message}")

    else:
        # ------- INVALID-UPLOAD branch -------
        error_upload_dialog(uploaded_file, validation_result.error_message)
        st.session_state.show_image = False
        st.session_state.success_dialog_shown = False


# ------- RAW OCR DISPLAY -------
if "extracted_text" in st.session_state and st.session_state.extracted_text:
    st.subheader("Review Raw Extracted Information")
    st.text_area(
        "📝 Extracted Text",
        value=st.session_state.extracted_text,
        height=300,
        disabled=False,
        key="ocr_output",
    )

    # ------- EXTRACT INVOICE FIELDS -------
    if st.button("📸 Extract invoice fields"):
        if not st.session_state.get("extracted_text"):
            st.warning("Please extract the raw text first.")
        else:
            with st.spinner("Extracting structured fields..."):
                # Run extraction and store domain model (or None)
                fields = extract_invoice_fields(st.session_state.extracted_text)
                st.session_state.confirmed_invoice = None
                st.session_state.invoice_fields = fields

                # Populate the review keys directly into session state.
                # Ensures that re-running extraction updates the widget state explicitly
                st.session_state.review_vendor = format_ui_value(
                    getattr(fields, "vendor", None)
                )
                st.session_state.review_invoice_number = format_ui_value(
                    getattr(fields, "invoice_number", None)
                )
                st.session_state.review_invoice_date = format_ui_value(
                    getattr(fields, "invoice_date", None),
                )
                st.session_state.review_subtotal = format_ui_value(
                    getattr(fields, "subtotal", None)
                )
                st.session_state.review_tax = format_ui_value(
                    getattr(fields, "tax", None)
                )
                st.session_state.review_discount = format_ui_value(
                    getattr(fields, "discount", None)
                )
                st.session_state.review_total = format_ui_value(
                    getattr(fields, "total", None)
                )
                st.session_state.review_currency = format_ui_value(
                    getattr(fields, "currency", None)
                )


# ------- REVIEW + EDIT -------
if st.session_state.get("invoice_fields") is not None:
    st.subheader("Review Extracted Information")
    st.caption("Inspect and correct any fields before committing.")

    st.text_input("Vendor", key="review_vendor", on_change=invalidate_confirmation)
    st.text_input(
        "Invoice Number", key="review_invoice_number", on_change=invalidate_confirmation
    )
    st.text_input(
        "Invoice Date", key="review_invoice_date", on_change=invalidate_confirmation
    )
    st.text_input("Subtotal", key="review_subtotal", on_change=invalidate_confirmation)
    st.text_input("Tax", key="review_tax", on_change=invalidate_confirmation)
    st.text_input("Discount", key="review_discount", on_change=invalidate_confirmation)
    st.text_input("Total", key="review_total", on_change=invalidate_confirmation)
    st.text_input("Currency", key="review_currency", on_change=invalidate_confirmation)

    # ------- CONFIRM -------
    if st.button("Confirm"):
        validated_result = validate_reviewed_invoice(
            vendor=st.session_state.review_vendor,
            invoice_number=st.session_state.review_invoice_number,
            invoice_date=st.session_state.review_invoice_date,
            subtotal=st.session_state.review_subtotal,
            tax=st.session_state.review_tax,
            discount=st.session_state.review_discount,
            total=st.session_state.review_total,
            currency=st.session_state.review_currency,
        )
        if not validated_result.is_valid:
            st.session_state.confirmed_invoice = None
            for field, error in validated_result.errors.items():
                st.error(f"{field}:{error}")
        else:
            st.success("Validated successfully")
            st.session_state.confirmed_invoice = validated_result.invoice


# ------- CONFIRMED INFORMATION -------
if "confirmed_invoice" in st.session_state and st.session_state.confirmed_invoice:
    st.subheader("Confirmed Information by user")
    invoice_data = st.session_state.confirmed_invoice.model_dump()
    # for field_name, value in invoice_data.items():
    #     st.write(f"**{field_name}:** {value}")
    warnings = check_invoice_consistency(st.session_state.confirmed_invoice)
    if warnings:
        for warning in warnings:
            st.warning(f"{warning}")
    saved_invoice_id = st.session_state.get("saved_invoice_id")
    if saved_invoice_id is None:
        if st.button("Save Invoice"):
            record = InvoiceRecord(
                source_filename=st.session_state.file_name,
                vendor=invoice_data["vendor"],
                invoice_number=invoice_data["invoice_number"],
                invoice_date=invoice_data["invoice_date"],
                subtotal=invoice_data["subtotal"],
                tax=invoice_data["tax"],
                discount=invoice_data["discount"],
                total=invoice_data["total"],
                currency=invoice_data["currency"],
            )

            # Persist and store generated ID in session state
            invoice_id = save_invoice(record)
            st.session_state["saved_invoice_id"] = invoice_id

            # Force rerender to show confirmation view immediately
            st.rerun()
    else:
        st.success(
            "Invoice saved successfully!"
            f"(Record #{st.session_state['saved_invoice_id']})"
        )


st.divider()
st.subheader("Saved Invoice Ledger")

records = list_invoices()

if not records:
    st.info("No invoices saved yet.")
else:
    # Convert InvoiceRecord Pydantic models to dictionaries
    raw_data = [record.model_dump() for record in records]

    # Convert to DataFrame
    df = pd.DataFrame(raw_data)

    # Directly select expected columns matching InvoiceRecord schema
    df_display = df[
        [
            "id",
            "vendor",
            "invoice_number",
            "invoice_date",
            "subtotal",
            "discount",
            "tax",
            "total",
            "currency",
            "source_filename",
            "created_at",
        ]
    ]

    # Rename columns to user-friendly titles
    df_display = df_display.rename(
        columns={
            "id": "ID",
            "vendor": "Vendor",
            "invoice_number": "Invoice Number",
            "invoice_date": "Invoice Date",
            "subtotal": "Subtotal",
            "discount": "Discount",
            "tax": "Tax",
            "total": "Total",
            "currency": "Currency",
            "source_filename": "Source File",
            "created_at": "Created At",
        }
    )

    # Display in Streamlit dataframe
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
    )
