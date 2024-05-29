## Contents
[OCR Model](#ocr-model-robot)<br>
- [Overview](#mag-overview)<br>
- [Components](#open_file_folder-components)<br>
- [Tools Used](#hammer_and_wrench-tools-used)<br>
- [Getting Started](#rocket-getting-started)<br>
- [References](#books-references)<br>

# OCR Model :robot:

**`Recently, OpenAI launched the GPT-4o model, claimed to be the most powerful model to date. This project explores its OCR capabilities within a simple OCR Model.`**

## :mag: Overview
This project develops a OCR Model utilizing the latest and most powerful GPT-4o model from OpenAI. The model processes images and extracts text using OCR capabilities, integrating these functionalities into a application built with Flask. The application can be run locally.[^1]

## :open_file_folder: Components
Below is a breakdown of the key components included in this repository:

- [**`tests/`**](tests/readme.md): Test cases documentation.

- [**`src/`**](src/): Source files for the application.
  - [`__init__.py`](src/__init__.py): Initializes src as a Python module.
  - [`main.py`](src/main.py): Main script to run the application.
  - [`app.py`](src/app.py): Flask application endpoints for image upload and OCR processing.
  - [`ocr_model.py`](src/rag_model.py): OCR Model's functionality and methods.
  - [`.env`](src/.env): Environment file for setting the OpenAI API key.

- [**`config/`**](config/): Configuration files.
  - [`parameters.json`](config/parameters.json): Configuration settings for OCR Model.
  - [`invoice_schema.json`](config/invoice_schema.json): Configuration invoice schema for OCR Model.

- [**`requirements.txt`**](requirements.txt): Python dependencies.

- [**`README.md`**](README.md): Detailed description of the project.

- [**`LICENSE`**](LICENSE): MIT License information.


## :hammer_and_wrench: Tools Used
The following tools are utilized in this project:

1. **Flask**
2. **GPT-4o**

## :rocket: Getting Started
Follow these steps to set up and run the project on your local machine:

1. **Clone the repository:**

``` bash
git clone https://github.com/jairzinhosantos/ocr-model.git
```

3. **Set up a virtual environment:**

``` bash
python -m venv venv
source venv/bin/activate
```

4. **Install dependencies:**

``` bash
pip install -r requirements.txt
```

5. **Run the application:**

``` bash
python src/main.py
```

### :books: References
[^1]: [GPT4o_Vision](https://github.com/AI-Unleashed/GPT4o_Vision)

