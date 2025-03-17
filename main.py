import pandas as pd
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter


def load_bible_data(file_paths):
    """
    Loads Bible text from multiple files into a Pandas DataFrame
    Assumes each file is a book of the Bible, and that each line is a verse

    Args:
        file_paths: list of strings containing file paths to .txt files of Bible books
    
    Returns:
        data frame containing book, chapter, verse, and text info for the entire book of the Bible
    """
    data = []
    for file_path in file_paths:
        biblical_book_name = file_path.split('/')[-1].replace(".txt", "").capitalize()
        with open(file_path, 'r', encoding='utf-8') as biblical_book:
            chapter = 1
            verse_number = 1
            for line in biblical_book:
                line = line.strip()
                if line.startswith("Chapter"):
                    chapter += 1
                    verse_number = 1
                    continue
                if len(line) != 0:
                    data.append({
                        "book": biblical_book_name,
                        "chapter": chapter,
                        "verse_number": verse_number,
                        "text": line
                    })
                    verse_number += 1
    return pd.DataFrame(data)     


# File paths:
file_paths = [
    "cleaned_bible_data/nrsvce/by_book/james_cleaned.txt",
    "cleaned_bible_data/nrsvce/by_book/1_john_cleaned.txt",
    "cleaned_bible_data/nrsvce/by_book/2_john_cleaned.txt",
    "cleaned_bible_data/nrsvce/by_book/3_john_cleaned.txt",
    "cleaned_bible_data/nrsvce/by_book/1_peter_cleaned.txt",
    "cleaned_bible_data/nrsvce/by_book/2_peter_cleaned.txt",
    "cleaned_bible_data/nrsvce/by_book/jude_cleaned.txt",
]

biblical_dataframe = load_bible_data(file_paths)
print(biblical_dataframe.head())

def clean_text(text):
    """
    Takes text from a biblical dataframe and standardizes the format for data processing

    Args:
        text: str containing one verse of the Bible
    
    Returns
        text: now cleaned for putting into a new column of the dataframe
    """
    text = re.sub(r'^\d+\s*', '', text) # Remove any leading numbers for verses
    text = " ".join(text.split()) # Normalize white-space
    text = text.translate(str.maketrans("", "", string.punctuation)) # Remove punctuation
    text = text.lower() # Lower the text for ease of parsing
    return text

def preprocess_text(text):
    """
    Takes text and tokenizes its words and lemmatizes them for analysis
    Args:
        text: text of the Bible which may or may not have been cleaned (str)
    Returns:
        lemmatized_words: a list of lemmatized words (str)
    """
    cleaned_text = clean_text(text) # Repeat cleaning just in case
    words = word_tokenize(cleaned_text) # Tokenize words in each sentence
    stop_words = set(stopwords.words('english')) # Get a list of stopwords
    filtered_words = [word for word in words if words not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
    return lemmatized_words

biblical_dataframe["cleaned_text"] = biblical_dataframe["text"].apply(clean_text)
biblical_dataframe["processed_words"] = biblical_dataframe["cleaned_text"].appyl(preprocess_text)

print(biblical_dataframe.head())

# Group Data Frame by book and count word frequencies across a book or sections
def get_word_frequencies(words):
    return Counter(words)

biblical_book_frequencies = biblical_dataframe.groupby("biblical_book")["processed_words"].apply(lambda x: [word for sublist in x for word in sublist]).apply(get_word_frequencies)

# Print the top 7 most common words from each book
for biblical_book, frequencies in biblical_book_frequencies.items():
    print(f"--- {biblical_book} ---")
    for word, count in frequencies.most_common(7):
        print(f"{word} appeared: {count} times")