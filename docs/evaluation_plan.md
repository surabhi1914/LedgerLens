# Evaluation Plan

This document defines how LedgerLens should be evaluated as implementation phases are completed. It does not contain performance results.

## Field Extraction

Planned evaluation:

- Normalized exact-match accuracy by field.
- Missing-field handling.
- Per-field error analysis.
- Examples of OCR failures and parsing failures.

Fields:

- Vendor.
- Invoice number.
- Invoice date.
- Subtotal.
- Tax.
- Total.
- Currency.

Field values should be normalized before comparison where appropriate. Dates, currency values, vendor names, and invoice numbers may need different normalization rules.

Failures should be separated into OCR failures and parsing failures when possible. This distinction matters because poor OCR text and weak field parsing require different fixes.

## Expense Categorization

Planned evaluation:

- Rule-based baseline.
- Machine-learning model comparison.
- Macro F1.
- Per-category precision and recall.
- Confusion matrix.
- Review of incorrectly classified examples.

The first categorization result should be compared against a simple baseline before adding more complex models. Macro F1 is planned because category distributions may be uneven.

Incorrectly classified examples should be reviewed manually to identify unclear labels, weak features, OCR problems, or categories that should be merged or renamed.

## Duplicate Detection

Planned evaluation:

- Exact file duplicates.
- Exact normalized-field duplicates.
- Near-duplicate similarity score.
- Precision.
- Recall.
- False-positive analysis.
- False-negative analysis.
- Documented threshold-selection method.

Exact file duplicates should be detected with file hashes. Exact normalized-field duplicates should compare trusted reviewed fields such as vendor, invoice number, invoice date, total, and currency.

Near-duplicate detection should use a documented similarity score and a documented threshold-selection method. The threshold should not be chosen only because it looks good on a few examples.

## Product Workflow

Planned checks:

- Invalid files are rejected safely.
- Partial extraction does not crash the app.
- Users can correct extracted data.
- Duplicate explanations are understandable.
- Exported data matches reviewed values.
- Demo invoices contain no sensitive personal information.

The workflow should be tested with successful uploads, invalid files, partial OCR output, missing fields, duplicate candidates, and CSV export.

## Data Policy

- FATURA will be evaluated as the primary invoice dataset candidate.
- Dataset annotation labels must be inspected before finalizing field mappings.
- Train, validation, and test documents must remain separated.
- Documents created from the same template or original invoice must not leak across evaluation splits when testing generalization.
- Duplicate and corrupted-document test cases may later be created as a small separate robustness set.
- No fake performance metrics should appear in the documentation.
