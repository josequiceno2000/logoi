import re

def clean_bible_text(text):
    """Cleans the text of a single book of the Bible"""
    # Removing chapter and verse numbers
    text = re.sub(r'-- \d+ \w+ \d+:\d+', '', text)
    # Remove dashes:
    text = text.strip()
    # Standardize spacing and newline:
    text = '\n'.join(text.split())
    # Set all text to lowercase:
    text = text.lower()
    # Eliminate punctuation:
    text = text.replace(".", "").replace("?", "").replace("!", "").replace(",", "").replace("(", "").replace(")", "").replace(";", "").replace(":", "")
    return text


# Reading the book and outputting the cleaned format
input_file_path = "./bibles/new-testament/2-john/2-john-eng.txt"
output_file_path = "./bibles/new-testament/2-john/clean-2-john-eng.txt"
try:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        original_text = file.read()
    
    cleaned_text = clean_bible_text(original_text)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)
    
    print(f"Cleaned text successfully written to {output_file_path}")
except FileNotFoundError:
    print(f"Error: file does not exist at {input_file_path}")
except Exception as e:
    print(f"An error occurred while reading: {e}")
