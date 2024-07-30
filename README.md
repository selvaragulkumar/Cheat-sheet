# Cheat-sheet

## Cheat Sheet Generator

**openai_cheat_sheet.py** Python script extracts major content from a given webpage and generates a cheat sheet in JSON format using OpenAI's GPT-4. The cheat sheet is formatted into a table-like structure with columns based on the content of the webpage.

### Requirements
- requests for making HTTP requests
- beautifulsoup4 for parsing HTML
- openai for interacting with OpenAI's GPT-4
- pandas for handling tabular data (if needed in future extensions)

### Configuration
You need to set the following configuration values in the script:

- url: The URL of the webpage you want to extract content from.
- key: Your OpenAI API key.

### Script Overview
#### Define the Prompt for OPENAI

A prompt template is defined for **OpenAI's API**. It instructs the model to categorize and tabulate the content extracted from the webpage into a cheat sheet format.

#### Extract Main Content from Webpage

**extact_main_content** function fetches the webpage content and extracts text from a specific HTML div with class content.

#### Create and Call OpenAI API Prompt

The script formats the prompt with the extracted text and calls the OpenAI API to generate the cheat sheet in JSON format.

#### Save JSON Output

The generated JSON is saved to a file named **cheat_sheet_json.json**.

## JSON to PDF Cheat Sheet Generator
**cheat_sheet_gen.py** Python script generates a PDF cheat sheet from a JSON file. It uses the ReportLab library to create a well-formatted PDF that includes tables and text extracted from the JSON file.

### Requirements
- reportlab for generating PDFs
- json for handling JSON data

### Script Overview
#### Import Libraries

The script imports necessary libraries for creating PDFs and handling JSON data.

#### Text Wrapping Function

**wrap_text** function creates a Paragraph object to calculate the width and height of text given a maximum width and font size.

#### Cell Height Adjustment

**adjust_cell_height** function calculates the height required for each cell based on its content and the column width.

#### Table Drawing

**draw_table** function creates and draws tables on the PDF canvas. It handles wrapping and adjusting cell heights to fit content within the page.

#### Adding JSON Content to PDF

**add_json_to_pdf** function processes JSON data to create tables and paragraphs, recursively handling nested dictionaries and lists. It formats the text into lines and adjusts the PDF canvas accordingly.

#### Generate PDF from JSON

**generate_pdf_from_json** function reads JSON data from a file, initializes the PDF canvas, and calls add_json_to_pdf to populate the PDF with content from the JSON file.

## Usage

Run the script **openai_cheat_sheet.py**

Ensure you have a JSON file (**cheat_sheet_json.json**) formatted with the necessary data.

Run the script **cheat_sheet_gen.py**

Execute the script to generate a PDF (**cheat_sheet.pdf**) from the JSON file:

## Notes
- The wrap_text function uses Paragraph from ReportLab to calculate text height and ensure it fits within column widths.
- The draw_table function ensures that the table content does not overflow the page boundaries by dynamically adjusting row heights and managing page breaks.
- Nested JSON structures are handled recursively to format tables and text appropriately.
