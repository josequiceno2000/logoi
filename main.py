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
        biblical_book_name = file_path.split('/')[-1].replace(".txt", "").replace("_", " ").lower().capitalize()
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
                        "biblical_book": biblical_book_name,
                        "chapter": chapter,
                        "verse_number": verse_number,
                        "text": line
                    })
                    verse_number += 1
    return pd.DataFrame(data)     


# File paths:
file_paths = [
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/matthew.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/mark.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/luke.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/john.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/acts.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/romans.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/1_corinthians.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/2_corinthians.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/galatians.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/ephesians.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/philippians.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/colossians.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/1_thessalonians.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/2_thessalonians.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/1_timothy.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/2_timothy.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/titus.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/philemon.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/hebrews.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/james.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/1_peter.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/2_peter.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/1_john.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/2_john.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/3_john.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/jude.txt",
    "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/revelation.txt"
]

biblical_dataframe = load_bible_data(file_paths)


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

    # Remove punctuation besides apostraphes
    text = re.sub(r"[^\w\s\']", "", text)

    # Remove single quotation marks left by themselves
    text = re.sub(r"\'\s|\s\'|\'", "", text)
    
    text = text.lower() # Lower the text for ease of parsing
    return text

def preprocess_text(text):
    """
    Takes text and tokenizes its words and lemmatizes them for analysis
    Args:
        text: text of the Bible which may or may not have been cleaned (str)
    Returns:
        final_words: a list of lemmatized words (str)
    """
    cleaned_text = clean_text(text) # Repeat cleaning just in case
    words = word_tokenize(cleaned_text) # Tokenize words in each sentence
    stop_words = set(stopwords.words('english')) # Get a list of stopwords
    filtered_words = [word for word in words if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
    final_words = []
    for word in lemmatized_words:
        if word == "u":
            final_words.append("us")
        else:
            final_words.append(word)
    return final_words

biblical_dataframe["cleaned_text"] = biblical_dataframe["text"].apply(clean_text)
biblical_dataframe["processed_words"] = biblical_dataframe["cleaned_text"].apply(preprocess_text)

# Group Data Frame by book and count word frequencies across a book or sections
def get_word_frequencies(words):
    return Counter(words)

biblical_book_frequencies = biblical_dataframe.groupby("biblical_book")["processed_words"].apply(lambda x: [word for sublist in x for word in sublist]).apply(get_word_frequencies)

# Print the top 7 most common words from each book
most_common_words = 7

for biblical_book, frequencies in biblical_book_frequencies.items():
    book_title = f"\n--- {biblical_book.upper()} ---"
    book_title_length = len(book_title) - 1
    print(book_title)

    for word, count in frequencies.most_common(most_common_words):
        result = f"{word.title()}: {count}"
        print(result)

    print("-" * (book_title_length))

# Define Bible Sections:
old_testament = [
    'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
    'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings',
    '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther',
    'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Songs',
    'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel',
    'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum',
    'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
    'Tobit', 'Judith', 'Wisdom', 'Sirach', 'Baruch'
]

pentateuch = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"
]

historical_books = [
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Tobit", "Judith", "Esther", "1 Maccabees", "2 Maccabees"
]

poetic_books = [
    "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Songs", "Wisdom", "Sirach"
]

prophetic_books = [
    "Isaiah", "Jeremiah", "Lamentations", "Baruch", "Ezekiel", "Daniel", "Hosea", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"
]

new_testament = [
    'Matthew', 'Mark', 'Luke', 'John', 'Acts',
    'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
    'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
    '1 Timothy', '2 Timothy', 'Titus', 'Philemon',
    'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John',
    'Jude', 'Revelation'
]

gospels = [
    "Matthew", "Mark", "Luke", "John"
]

pauline_epistles = [
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon"
]

general_epistles = [
    "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude"
]

revelation = [
    "Revelation"
]

# Analyze word frequencies based on section
def get_section_frequencies(biblical_set):
    section_dataframe = biblical_dataframe[biblical_dataframe["biblical_book"].isin(biblical_set)]
    cumulative_words = [word for sublist in section_dataframe["processed_words"] for word in sublist]
    return Counter(cumulative_words)

new_testament_frequencies = get_section_frequencies(new_testament)
gospels_frequencies = get_section_frequencies(gospels)
general_epistles_frequencies = get_section_frequencies(general_epistles)
pauline_epistles_frequencies = get_section_frequencies(pauline_epistles)

section_title = "\n--- NEW TESTAMENT ---"
section_title_length = len(section_title) - 1
print(section_title)

for word, count in new_testament_frequencies.most_common(most_common_words):
    result = f"{word.title()}: {count}"
    print(result)

print("-" * (section_title_length))

section_title = "\n--- GOSPELS ---"
section_title_length = len(section_title) - 1
print(section_title)

for word, count in gospels_frequencies.most_common(most_common_words):
    result = f"{word.title()}: {count}"
    print(result)

print("-" * (section_title_length))

section_title = "\n--- PAULINE EPISTLES ---"
section_title_length = len(section_title) - 1
print(section_title)

for word, count in pauline_epistles_frequencies.most_common(most_common_words):
    result = f"{word.title()}: {count}"
    print(result)

print("-" * (section_title_length))

section_title = "\n--- GENERAL EPISTLES ---"
section_title_length = len(section_title) - 1
print(section_title)

for word, count in general_epistles_frequencies.most_common(most_common_words):
    result = f"{word.title()}: {count}"
    print(result)

print("-" * (section_title_length))