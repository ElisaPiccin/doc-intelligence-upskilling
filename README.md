# doc-intelligence-upskilling
The content of this repository is intended for training purposes only.


- **`searchable_pdf.py`**: A Python script to convert images or PDFs into searchable PDFs using Azure Document Intelligence APIs.
- **`client_quickstart.ipynb`**: A Jupyter Notebook for quick experimentation and testing of the Document Intelligence API.
- **`requirements.txt`**: A list of Python dependencies required to run the scripts in this repository.
- **`assets/`**: A folder containing sample files, such as invoices and layouts, for testing and demonstration purposes.
- **`.env`**: A file to store environment variables like API keys and endpoints (not included in the repository for security reasons).
- **`README.md`**: Documentation for setting up and using the repository.


## Setting up the Conda Environment

To create a conda environment called `di-upskilling` with Python 3.10, follow these steps:

1. Open your terminal or command prompt.
2. Run the following command to create the environment:

    ```sh
    conda create --name di-upskilling python=3.10
    ```

3. Activate the newly created environment:

    ```sh
    conda activate di-upskilling
    ```

4. Install the required dependencies from [requirements.txt](requirements.txt):

    ```sh
    pip install -r requirements.txt
    ```