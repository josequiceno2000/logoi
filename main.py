import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
from bible_data_loader import load_bible_data

# Create the Biblical Dataframe
biblical_dataframe = load_bible_data()


def clean_text(text):
    """
    Takes text from a biblical dataframe and standardizes the format for data processing.
    """
    text = re.sub(r'^\d+\s*', '', text) 
    text = " ".join(text.split()) 
    text = re.sub(r"[^\w\s\']", "", text)
    text = re.sub(r"\'\s|\s\'|\'", "", text)
    text = text.lower()
    return text

def preprocess_text(text):
    """
    Takes cleaned text and tokenizes, removes stop words, lemmatizes, and corrects "u" to "us".
    """
    words = word_tokenize(cleaned_text) # Tokenize words in each sentence
    stop_words = set(stopwords.words('english')) # Get a list of stopwords
    filtered_words = [word for word in words if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
    final_words = ["us" if word == "u" else word for word in lemmatized_words]
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