# Roadmap

This roadmap keeps LedgerLens focused on one practical step at a time. Phase 0 covers planning only. Phase 1 is the next implementation phase.

## Phase 0 - Project Framing and Planning

Objective: Define the project scope, planned architecture, roadmap, and evaluation approach.

Main tasks:

- Create or update the README.
- Document the planned architecture.
- Document the implementation roadmap.
- Document the evaluation plan and data policy.

Expected deliverable: Four planning documents: `README.md`, `docs/architecture.md`, `docs/roadmap.md`, and `docs/evaluation_plan.md`.

Completion checklist:

- [x] README created or updated.
- [x] Architecture document created or updated.
- [x] Roadmap created or updated.
- [x] Evaluation plan created or updated.
- [x] No Phase 1 implementation started.

## Phase 1 - Invoice Upload and Raw OCR Vertical Slice

Objective: Build the smallest working path from uploaded document to visible OCR text.

Main tasks:

- Add a simple Streamlit upload screen.
- Accept PDF, JPG, and PNG files.
- Validate file type and basic file properties.
- Run OCR on a sample uploaded document.
- Display raw OCR output for review.

Expected deliverable: A local app that can upload an invoice and show raw OCR text.

Completion checklist:

- [ ] Upload control works for supported formats.
- [ ] Invalid files are rejected safely.
- [ ] OCR output is displayed.
- [ ] Errors are handled without crashing the app.

## Phase 2 - Structured Field Extraction and Review

Objective: Extract candidate invoice fields and let the user correct them.

Main tasks:

- Parse vendor, invoice number, invoice date, subtotal, tax, total, and currency when available.
- Inspect FATURA annotation labels and field mappings.
- Design a review form for extracted fields.
- Track which values were extracted and which were corrected.

Expected deliverable: A review screen with editable extracted fields.

Completion checklist:

- [ ] Key fields appear in editable controls.
- [ ] Missing fields are handled clearly.
- [ ] User corrections can be captured.
- [ ] FATURA field mapping assumptions are documented.

## Phase 3 - Data Persistence and Expense Ledger

Objective: Store reviewed expense records and display a basic ledger.

Main tasks:

- Add a small PostgreSQL-backed data model.
- Save reviewed invoice fields.
- Store document metadata and file hashes.
- Display saved expenses in a ledger view.
- Support CSV export of reviewed records.

Expected deliverable: Reviewed expenses can be saved, listed, and exported.

Completion checklist:

- [ ] Reviewed records are persisted.
- [ ] Ledger view loads saved expenses.
- [ ] CSV export matches reviewed values.
- [ ] Basic database errors are handled.

## Phase 4 - Exact and Near-Duplicate Detection

Objective: Detect duplicate invoices before and after field review.

Main tasks:

- Detect exact file duplicates with hashing.
- Detect exact normalized-field duplicates.
- Create a near-duplicate similarity score.
- Show duplicate explanations to the user.
- Build a small robustness set for duplicate and corrupted-document checks if needed.

Expected deliverable: The app flags exact and possible duplicate invoices with understandable reasons.

Completion checklist:

- [ ] Exact file duplicates are detected.
- [ ] Exact normalized-field duplicates are detected.
- [ ] Near-duplicate candidates are scored.
- [ ] Duplicate warnings explain the reason for the match.

## Phase 5 - Expense Categorization and MLflow Tracking

Objective: Suggest expense categories and track model experiments.

Main tasks:

- Create a rule-based category baseline.
- Train simple scikit-learn models.
- Evaluate model performance with macro F1 and per-category metrics.
- Track experiments in MLflow.
- Compare models against the baseline.

Expected deliverable: Category suggestions with documented experiment results.

Completion checklist:

- [ ] Rule-based baseline exists.
- [ ] At least one model is trained.
- [ ] MLflow records parameters and metrics.
- [ ] Incorrect classifications are reviewed.

## Phase 6 - Spending Insights

Objective: Add simple views that help users understand reviewed expenses.

Main tasks:

- Summarize spending by category.
- Summarize spending by vendor.
- Summarize spending over time.
- Add simple filters for date, category, vendor, and currency.

Expected deliverable: A basic insights page based on reviewed expense records.

Completion checklist:

- [ ] Category summary is available.
- [ ] Vendor summary is available.
- [ ] Time-based summary is available.
- [ ] Filters work on saved records.

## Phase 7 - PySpark Batch Analytics

Objective: Use PySpark for a contained batch analytics learning exercise.

Main tasks:

- Export reviewed expenses to a batch-friendly format.
- Load expense data with PySpark.
- Run simple aggregations.
- Compare results with the app's smaller-scale summaries.

Expected deliverable: A small PySpark job or script that performs batch expense analytics.

Completion checklist:

- [ ] PySpark reads exported expense data.
- [ ] Batch aggregations run locally.
- [ ] Outputs are documented.
- [ ] Scope stays separate from the MVP app path.

## Phase 8 - Airflow Orchestration

Objective: Practice scheduling a simple batch workflow.

Main tasks:

- Create a small Airflow DAG for batch processing.
- Run validation or aggregation tasks on a schedule.
- Log task outputs clearly.
- Document how the DAG fits into the project.

Expected deliverable: A small Airflow workflow for scheduled batch processing.

Completion checklist:

- [ ] DAG runs locally.
- [ ] Tasks are small and understandable.
- [ ] Logs show success or failure.
- [ ] Airflow is documented as a learning extension.

## Phase 9 - Dockerization

Objective: Make local services reproducible.

Main tasks:

- Add Docker configuration for the app and local services.
- Document local setup.
- Keep environment variables out of source control.
- Confirm the app can run through the documented setup.

Expected deliverable: A Docker-based local development path.

Completion checklist:

- [ ] App service is containerized.
- [ ] PostgreSQL service is available locally.
- [ ] Setup instructions are clear.
- [ ] Secrets are not committed.

## Phase 10 - CI/CD and Deployment

Objective: Add basic automated checks and a simple deployment path.

Main tasks:

- Add GitHub Actions for tests and linting.
- Add deployment documentation.
- Keep deployment scope small.
- Verify checks run on pull requests or pushes.

Expected deliverable: Basic CI/CD support for the project.

Completion checklist:

- [ ] Automated checks run in GitHub Actions.
- [ ] Failing checks block unnoticed regressions.
- [ ] Deployment notes are documented.
- [ ] No production-grade infrastructure is claimed.

## Phase 11 - Portfolio Documentation and Final Evaluation

Objective: Prepare the project for review as a portfolio artifact.

Main tasks:

- Update README with final setup and demo instructions.
- Document evaluation results without exaggeration.
- Include screenshots or short demo notes.
- Describe known limitations and next steps.

Expected deliverable: A finished portfolio write-up with honest evaluation results.

Completion checklist:

- [ ] Setup instructions are accurate.
- [ ] Evaluation results are documented.
- [ ] Limitations are clear.
- [ ] Demo materials contain no sensitive personal data.

## Phase 12 - Optional AWS SageMaker Experiment

Objective: Run one optional cloud training experiment for learning.

Main tasks:

- Select a small category-model training task.
- Prepare a minimal SageMaker experiment.
- Compare the cloud run with the local workflow.
- Document cost, setup friction, and lessons learned.

Expected deliverable: A short optional write-up about one SageMaker training experiment.

Completion checklist:

- [ ] Experiment scope is small.
- [ ] Costs and cleanup steps are considered.
- [ ] Results are compared with local training.
- [ ] The experiment is documented as optional.
