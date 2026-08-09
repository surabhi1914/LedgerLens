# Phase 0: Project framing and planning

- created basic structure of the repo
- created doc files:
  - [architecture.md](docs\architecture.md) : gives brief description about the technology stack reasoning, MVP components and data flow.
  - [roadmap.md](docs\roadmap.md): My initial plan for this project is split into phases. The deliverables, expected outcome checklist, objective of the phase is mentioned in this document.
  - [evaluation.md](docs\evaluation.md): it briefly mentions the evaluation criteria to keep in mind post the phase execution.

# Phase 1: Invoice upload and raw OCR vertical slice.

- created the [pyproject.toml](pyproject.toml) with the dependencies mentioned below:
  - pydantic
  - pytest
  - pytest -cov
  - wheel
  - ruff
  - streamlit
  - python-dotenv
  - pillow
- created [config.py](src\ledgerlens\config.py)
  - By inheriting from BaseSettings, this class automatically gains the power to look at your computer's environment variables and load them into Python objects.
  - extra="ignore": This is a safety feature. If someone adds an extra variable to the .env file (like SUPER_SECRET_KEY=123) that is not defined as a variable inside my Python Settings class, Pydantic will simply ignore it instead of throwing a disruptive crash error.
  - lru_cache ensures that the .env file is read exactly once.
- created a streamlit homepage python file - [home.py](app\Home.py)
  - added basic configuration of the homepage
    ![alt text](assets\changelog_images\image.png)
  - added a runOnSave in the streamlit config file - [config.py](app.streamlit\config.py)
  - added a uploader for the file and it returns the error/success based on what is returned from the [file_validator.py](src\ledgerlens\ingestion\file_validator.py)
- created injection folder under ledgerlens
- created [file_validator.py](src\ledgerlens\ingestion\file_validator.py)
  - normalizes the extension
  - checks whether the extension is valid
  - checks whether the file size is valid
  - return pydantic model which will be used by the [home.py](app\Home.py) to show the errors
- created [document_loader.py](src\ledgerlens\ingestion\document_loader.py)
  - created 3 functions:
    - create_document_preview()
    - image_handling()
      - loading the filebytes using pillow and bytesio
      - then if its an image then returning them using pydantic model DocumentPreview
    - doc_handling()
      - opening the filebytes using pymupdf
      - create a matrix, why?: By default, PyMuPDF renders PDF pages at standard screen resolution (72 DPI). Rendering at 72 DPI often results in blurry text. Scaling by 1.5× bumps the effective resolution up to 108 DPI, making the text sharper and easier to read or feed into OCR engines.
      - convert the first page into pixmap
      - conver Pixmap object into a byte string in the PPM (Portable Pixmap) format
      - then loading the Image into PIL (Pillow
      - then return the image
- added preview setup in the streamlit file [home.py](app\Home.py) 
- created a file [ocr_engine.py](src\ledgerlens\extraction\ocr_engine.py)
  - file takes the image sent from the streamlit
  - extracts text from image using pytesseract 
  - and returns the text
  - minimal error handling is also added
- added OCR extract button in the streamlit file [home.py](app\Home.py) 
  - this views the text return from the [ocr_engine.py](src\ledgerlens\extraction\ocr_engine.py)

# Phase 2 - Structured Field Extraction and Review