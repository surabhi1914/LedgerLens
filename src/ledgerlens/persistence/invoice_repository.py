import sqlite3
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from ledgerlens.persistence.database import get_connection
from ledgerlens.persistence.models import InvoiceRecord


def _serialize_record(invoice: InvoiceRecord) -> dict[str, Any]:
    """Helper to convert date and Decimal types into text representation for SQLite."""
    return {
        "source_filename": invoice.source_filename,
        "vendor": invoice.vendor,
        "invoice_number": invoice.invoice_number,
        "invoice_date": invoice.invoice_date.isoformat()
        if invoice.invoice_date
        else None,
        "subtotal": str(invoice.subtotal) if invoice.subtotal is not None else None,
        "tax": str(invoice.tax) if invoice.tax is not None else None,
        "discount": str(invoice.discount) if invoice.discount is not None else None,
        "total": str(invoice.total) if invoice.total is not None else None,
        "currency": invoice.currency,
    }


def save_invoice(invoice: InvoiceRecord) -> int:
    """Persist an InvoiceRecord to SQLite and return the auto-generated ID."""
    data = _serialize_record(invoice)
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO invoices (
                source_filename,
                vendor,
                invoice_number,
                invoice_date,
                subtotal,
                tax,
                discount,
                total,
                currency
            ) VALUES (
                :source_filename,
                :vendor,
                :invoice_number,
                :invoice_date,
                :subtotal,
                :tax,
                :discount,
                :total,
                :currency
            )
            """,
            data,
        )
        conn.commit()

        if cursor.lastrowid is None:
            raise RuntimeError("Failed to retrieve generated row ID after insert.")

        return cursor.lastrowid
    finally:
        conn.close()


def _row_to_invoice_record(row: sqlite3.Row) -> InvoiceRecord:
    """Convert a SQLite database row into a strongly-typed InvoiceRecord."""

    def parse_decimal(val: Any) -> Decimal | None:
        if val is None:
            return None
        return Decimal(str(val))

    def parse_date(val: Any) -> date | None:
        if val is None:
            return None
        if isinstance(val, date):
            return val
        return date.fromisoformat(str(val))

    def parse_datetime(val: Any) -> datetime | None:
        if val is None:
            return None
        if isinstance(val, datetime):
            return val
        return datetime.fromisoformat(str(val))

    return InvoiceRecord(
        id=row["id"],
        source_filename=row["source_filename"],
        vendor=row["vendor"],
        invoice_number=row["invoice_number"],
        invoice_date=parse_date(row["invoice_date"]),
        subtotal=parse_decimal(row["subtotal"]),
        tax=parse_decimal(row["tax"]),
        discount=parse_decimal(row["discount"]),
        total=parse_decimal(row["total"]),
        currency=row["currency"],
        created_at=parse_datetime(row["created_at"]),
    )


def get_invoice(invoice_id: int) -> InvoiceRecord | None:
    """Fetch a single invoice record by its primary key ID."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM invoices WHERE id = ?",
            (invoice_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return _row_to_invoice_record(row)
    finally:
        conn.close()


def list_invoices() -> list[InvoiceRecord]:
    """Retrieve all invoice records ordered by newest first."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM invoices ORDER BY created_at DESC, id DESC")
        rows = cursor.fetchall()
        return [_row_to_invoice_record(row) for row in rows]
    finally:
        conn.close()
