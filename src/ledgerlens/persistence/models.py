# src/ledgerlens/persistence/models.py
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class InvoiceRecord(BaseModel):
    """Data model representing a saved invoice record."""

    id: int | None = None
    source_filename: str
    vendor: str | None = None
    invoice_number: str | None = None
    invoice_date: date | None = None

    subtotal: Decimal | None = None
    tax: Decimal | None = None
    discount: Decimal | None = None
    total: Decimal | None = None

    currency: str | None = None
    created_at: datetime | None = None
