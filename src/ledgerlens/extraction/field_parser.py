from ledgerlens.extraction.currency_parser import extract_currency
from ledgerlens.extraction.discount_parser import extract_discount
from ledgerlens.extraction.invoice_date_parser import extract_invoice_date
from ledgerlens.extraction.invoice_number_parser import extract_invoice_number
from ledgerlens.extraction.schema import InvoiceExtraction
from ledgerlens.extraction.subtotal_parser import extract_subtotal
from ledgerlens.extraction.tax_parser import extract_tax
from ledgerlens.extraction.text_normalizer import normalize_ocr_text
from ledgerlens.extraction.total_parser import extract_total
from ledgerlens.extraction.vendor_parser import extract_vendor


def extract_invoice_fields(raw_text: str) -> InvoiceExtraction:
    if not raw_text:
        return InvoiceExtraction()

    text = normalize_ocr_text(raw_text)

    vendor = extract_vendor(text)

    invoice_number = extract_invoice_number(text)

    invoice_date = extract_invoice_date(text)

    tax = extract_tax(text)

    subtotal = extract_subtotal(text)
    discount = extract_discount(text)
    total = extract_total(text)
    currency = extract_currency(text)

    return InvoiceExtraction(
        vendor=vendor,
        invoice_number=invoice_number,
        invoice_date=invoice_date,
        tax=tax,
        subtotal=subtotal,
        discount=discount,
        total=total,
        currency=currency,
    )
