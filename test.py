from datetime import date
from decimal import Decimal

from ledgerlens.persistence.database import initialize_database
from ledgerlens.persistence.invoice_repository import (
    get_invoice,
    list_invoices,
    save_invoice,
)
from ledgerlens.persistence.models import InvoiceRecord

# 1. Initialize schema
initialize_database()

# 2. Construct record
record = InvoiceRecord(
    source_filename="test_invoice.jpg",
    vendor="Richardson-Davis",
    invoice_number="2voM14-556",
    invoice_date=date(2007, 3, 20),
    subtotal=Decimal("764.34"),
    tax=Decimal("36.29"),
    discount=Decimal("22.24"),
    total=Decimal("790.46"),
    currency="EUR",
)

# 3. Save
invoice_id = save_invoice(record)
print(f"invoice_id -> {invoice_id} ({type(invoice_id).__name__})")

# 4. Fetch by ID
saved = get_invoice(invoice_id)
print(f"\nsaved -> {saved}")

# 5. Verify exact deserialized types
print(
    f"\nsaved.subtotal     = {saved.subtotal!r} | type = {type(saved.subtotal).__name__}"
)
print(
    f"saved.invoice_date = {saved.invoice_date!r} | type = {type(saved.invoice_date).__name__}"
)
print(
    f"saved.created_at   = {saved.created_at!r} | type = {type(saved.created_at).__name__}"
)

# 6. List all invoices
all_invoices = list_invoices()
print(f"\nall_invoices -> {all_invoices}")

# 7. Test missing ID handling
missing = get_invoice(999999)
print(f"\nget_invoice(999999) -> {missing}")
