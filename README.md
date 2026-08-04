# LedgerLens: AI-Assisted Invoice & Expense Manager

LedgerLens is a small portfolio project for exploring how invoices and receipts can be turned into reviewed expense records. The system is planned as an AI-assisted workflow, where extraction and categorization help the user move faster, but the user still reviews and corrects the final data before it is saved or exported.

## Why This Project Is Useful

Invoices and receipts often arrive as PDFs or images, which makes expense tracking slow and error-prone. This project focuses on a practical middle ground: extract the most useful fields, show them clearly for review, flag possible duplicates, and produce a simple expense ledger that can be exported.

## MVP User Workflow

1. Upload a PDF, JPG, or PNG invoice.
2. Run OCR and parse key fields.
3. Review and correct extracted values.
4. Predict an expense category.
5. Check for exact or possible duplicate invoices.
6. Save the reviewed expense record.
7. View simple spending insights.
8. Export reviewed expenses as CSV.

## MVP Features

- Upload PDF, JPG, or PNG invoices.
- Extract vendor, invoice number, invoice date, subtotal, tax, total, and currency when available.
- Let the user review and correct extracted fields.
- Predict an expense category.
- Detect exact and possible duplicates.
- Display simple spending insights.
- Export reviewed expenses as CSV.

## Non-Goals

The MVP will not include:

- User authentication.
- Multiple organizations.
- Payment processing.
- Bank integrations.
- Tax or financial advice.
- Reliable line-item extraction.
- Large-scale distributed processing.
- Production-grade cloud infrastructure.
- Multiple cloud providers.

## Planned Technology Stack

The project is expected to introduce tools gradually:

- Python for core processing and data handling.
- Streamlit for the review-focused user interface.
- OCR tools for reading text from invoice images and PDFs.
- scikit-learn for expense categorization experiments.
- PostgreSQL for storing reviewed expense records.
- Docker for reproducible local services.
- MLflow for tracking category-model experiments.
- Airflow for scheduled batch workflows.
- PySpark for batch transformations and analytics.
- GitHub Actions for basic CI/CD.
- Optional Databricks for one Spark learning exercise.
- Optional AWS SageMaker for one cloud training experiment.

These technologies are planned, not implemented in Phase 0.

## Dataset Decision

The current primary dataset candidate is the FATURA Dataset, Zenodo DOI: `10.5281/zenodo.8261508`. FATURA contains synthetic invoice images with JSON annotations and predefined evaluation splits, making it a suitable starting point for an invoice-first project.

The annotation classes and field mappings must be inspected during the data phase before deciding how well FATURA supports the MVP fields. The project should not claim that every required MVP field is directly available in the annotations until that inspection is complete.

SROIE may be useful later as an optional secondary receipt dataset, but it is not the primary invoice dataset candidate.

## Development Phases

- Phase 0: Project framing and planning. - Completed
- Phase 1: Invoice upload and raw OCR vertical slice. - In progress
- Phase 2: Structured field extraction and review.
- Phase 3: Data persistence and expense ledger.
- Phase 4: Exact and near-duplicate detection.
- Phase 5: Expense categorization and MLflow tracking.
- Phase 6: Spending insights.
- Phase 7: PySpark batch analytics.
- Phase 8: Airflow orchestration.
- Phase 9: Dockerization.
- Phase 10: CI/CD and deployment.
- Phase 11: Portfolio documentation and final evaluation.
- Phase 12: Optional AWS SageMaker experiment.

## Current status

Phase 1 in progress: building the invoice upload and raw OCR workflow.

## Privacy and Limitations

This project is intended for learning and portfolio use. Demo invoices should avoid sensitive personal information. Extracted values may be incomplete or incorrect, so the workflow must keep human review between automated extraction and saved expense records.
