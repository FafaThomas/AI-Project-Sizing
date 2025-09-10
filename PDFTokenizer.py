import re
import os
import pytesseract
import fitz  # PyMuPDF

# IMPORTANT: You must have Tesseract OCR installed on your system and its
# path configured in your environment variables for this program to work.
# For Windows, you might need to set the path like this:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def simple_tokenizer(text):
    """
    A simple tokenizer that counts tokens in a given string.
    
    This function considers words, numbers, and punctuation marks as individual tokens.
    It splits the text based on spaces and then further separates any attached punctuation.

    Args:
        text (str): The input string to tokenize.

    Returns:
        tuple: A tuple containing a list of the tokens and the total token count.
    """
    if not isinstance(text, str):
        return [], 0

    # Use a regular expression to find all words, numbers, and punctuation.
    # This pattern matches any sequence of letters, numbers, or a single non-whitespace character.
    tokens = re.findall(r'\b\w+\b|\S', text.strip())
    
    return tokens, len(tokens)

def pdf_to_text(pdf_path):
    """
    Extracts text from a PDF file using a hybrid approach:
    First, it tries to get text directly from the PDF. If that fails, it falls back to OCR.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' was not found.")
        return ""

    full_text = ""
    try:
        with fitz.open(pdf_path) as doc:
            print(f"Processing '{pdf_path}' with {len(doc)} pages...")
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_text = ""

                # Try to extract text directly first
                try:
                    page_text = page.get_text()
                    if page_text.strip():
                        full_text += page_text
                        print(f"Page {page_num + 1} processed using direct text extraction.")
                        continue # Move to the next page if text was found
                except Exception as direct_e:
                    print(f"Direct text extraction failed for page {page_num + 1}: {direct_e}")

                # If no text was found, fall back to OCR
                try:
                    pix = page.get_pixmap()
                    page_text = pytesseract.image_to_string(pix.tobytes(), lang='eng')
                    full_text += page_text
                    print(f"Page {page_num + 1} processed using OCR.")
                except Exception as ocr_e:
                    print(f"Error on page {page_num + 1} during OCR: {ocr_e}. Skipping this page.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
    
    return full_text

if __name__ == "__main__":
    print("Welcome to the OCR tokenizer!")
    print("This program will extract text from a PDF file and tokenize it.")
    print("To exit, type 'quit' or 'exit'.\n")
    print("Dependencies: You need to install PyMuPDF, pytesseract, and the Tesseract OCR engine.")
    print("Run the following commands in your terminal:")
    print("pip install PyMuPDF pytesseract Pillow")
    print("\nFor Tesseract OCR engine installation, please refer to the documentation for your OS.")
    print("----------------------------\n")

    # Hard-coded path for a placeholder PDF file
    hardcoded_pdf_path = r"D:\Organized Projects\For Portfolio\__Portfolio Overview__\Field Automation Hub - Product Overview and Operation Manual.pdf"
    
    while True:
        # Use the hard-coded path instead of user input for simplicity
        pdf_file = hardcoded_pdf_path
        print(f"Using hard-coded PDF file: {pdf_file}")

        extracted_text = pdf_to_text(pdf_file)
        
        if extracted_text:
            tokens, token_count = simple_tokenizer(extracted_text)
            
            print("\n--- Tokenization Results ---")
            print(f"Original Text (first 500 characters): {extracted_text[:500]}...")
            print(f"Total token count: {token_count}")
            print("----------------------------\n")
            break # Exit the loop after processing the hard-coded file
        else:
            print("Could not process the PDF. Please check the file path and try again.")
            break # Exit on error to avoid infinite loop
