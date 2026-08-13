from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from ledgerlens.extraction.currency_parser import SUPPORTED_CODES
from ledgerlens.extraction.money_parser import parse_money
from ledgerlens.extraction.schema import InvoiceExtraction


@dataclass
class ReviewValidationResult:
    is_valid: bool
    invoice: InvoiceExtraction | None
    errors: dict[str, str]


def _clean_string(value: str) -> str | None:
    """Strip whitespace and convert empty strings to None."""
    cleaned = value.strip()
    return cleaned if cleaned else None


def _validate_date(field_name: str, value: str, errors: dict[str, str]) -> date | None:
    """Validate canonical YYYY-MM-DD date format."""
    cleaned = _clean_string(value)
    if cleaned is None:
        return None

    try:
        return datetime.strptime(cleaned, "%Y-%m-%d").date()
    except ValueError:
        errors[field_name] = "Use YYYY-MM-DD format."
        return None


def _validate_money(
    field_name: str, value: str, errors: dict[str, str]
) -> Decimal | None:
    """Validate monetary amount string using parse_money."""
    cleaned = _clean_string(value)
    if cleaned is None:
        return None

    parsed = parse_money(cleaned)
    if parsed is None:
        errors[field_name] = "Enter a valid monetary amount."
        return None

    return parsed


def _validate_currency(
    field_name: str, value: str, errors: dict[str, str]
) -> str | None:
    """Validate currency code against allowed supported codes."""
    cleaned = _clean_string(value)
    if cleaned is None:
        return None

    normalized = cleaned.upper()
    if normalized not in SUPPORTED_CODES:
        supported_str = ", ".join(sorted(SUPPORTED_CODES))
        errors[field_name] = f"Currency must be one of: {supported_str}"
        return None

    return normalized


def validate_reviewed_invoice(
    vendor: str,
    invoice_number: str,
    invoice_date: str,
    subtotal: str,
    tax: str,
    total: str,
    currency: str,
) -> ReviewValidationResult:
    errors: dict[str, str] = {}

    clean_vendor = _clean_string(vendor)
    clean_invoice_number = _clean_string(invoice_number)

    # Validate typed/formatted fields
    parsed_date = _validate_date("invoice_date", invoice_date, errors)
    parsed_subtotal = _validate_money("subtotal", subtotal, errors)
    parsed_tax = _validate_money("tax", tax, errors)
    parsed_total = _validate_money("total", total, errors)
    parsed_currency = _validate_currency("currency", currency, errors)

    if errors:
        return ReviewValidationResult(is_valid=False, invoice=None, errors=errors)

    invoice = InvoiceExtraction(
        vendor=clean_vendor,
        invoice_number=clean_invoice_number,
        invoice_date=parsed_date,
        subtotal=parsed_subtotal,
        tax=parsed_tax,
        total=parsed_total,
        currency=parsed_currency,
    )

    return ReviewValidationResult(is_valid=True, invoice=invoice, errors={})
