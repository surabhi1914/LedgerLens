# src/ledgerlens/persistence/invoice_repository.py
import sqlite3
from typing import Any

from ledgerlens.persistence.database import DB_PATH, get_connection
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


def save_invoice(invoice: InvoiceRecord, conn: sqlite3.Connection | None = None) -> int:
    """Insert an InvoiceRecord into the database and return the assigned database ID.

    Accepts an optional active connection, defaulting to creating a new one.
    """
    data = _serialize_record(invoice)

    query = """
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
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    params = (
        data["source_filename"],
        data["vendor"],
        data["invoice_number"],
        data["invoice_date"],
        data["subtotal"],
        data["tax"],
        data["discount"],
        data["total"],
        data["currency"],
    )

    if conn is not None:
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.lastrowid

    with get_connection(DB_PATH) as connection:
        cursor = connection.execute(query, params)
        connection.commit()
        return cursor.lastrowid
