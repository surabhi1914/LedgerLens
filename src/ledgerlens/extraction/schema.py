from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class InvoiceExtraction(BaseModel):
    # --- Vendor Information ---
    vendor: str | None = Field(
        default=None, description="Name of the vendor or supplier"
    )

    # --- Invoice Identification ---
    invoice_number: str | None = Field(
        default=None,
        description="Invoice reference number",
    )

    # --- Date ---
    invoice_date: date | None = Field(
        default=None,
        description="Invoice date as a proper date object for filtering and sorting",
    )

    # --- Financial Fields (using Decimal for precision) ---
    subtotal: Decimal | None = Field(
        default=None,
        description="Subtotal before tax (without currency symbol)",
    )

    tax: Decimal | None = Field(
        default=None,
        description="Tax amount (without currency symbol)",
    )

    total: Decimal | None = Field(
        default=None,
        description="Final total including tax (without currency symbol)",
    )

    # --- Currency ---
    currency: str | None = Field(
        default=None,
        description="Currency code (ISO 4217 format)",
        min_length=3,
        max_length=3,
    )

    discount: Decimal | None = Field(
        default=None,
        description="Discount deduction amount",
    )
