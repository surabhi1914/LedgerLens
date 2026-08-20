from ledgerlens.extraction.schema import InvoiceExtraction


def check_invoice_consistency(invoice: InvoiceExtraction) -> list[str]:
    warnings: list[str] = []

    subtotal = invoice.subtotal
    tax = invoice.tax
    discount = invoice.discount
    total = invoice.total

    if subtotal is None or tax is None or discount is None or total is None:
        return warnings

    expected_total = subtotal - discount + tax

    if expected_total != total:
        warnings.append("Subtotal minus discount plus tax does not match the total.")

    return warnings
