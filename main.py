from collections import Counter
from bible_data_loader import load_bible_data
from text_preprocessing import clean_text, preprocess_text
import bible_sections

# Create the Biblical Dataframe
biblical_dataframe = load_bible_data()

# Clean and Preprocess the text
print("Cleaning the biblical text...")
biblical_dataframe["cleaned_text"] = biblical_dataframe["text"].apply(clean_text)
print("Preprocessing the biblical text...")
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


# Analyze word frequencies based on section
def get_section_frequencies(biblical_set):
    section_dataframe = biblical_dataframe[biblical_dataframe["biblical_book"].isin(biblical_set)]
    cumulative_words = [word for sublist in section_dataframe["processed_words"] for word in sublist]
    return Counter(cumulative_words)

new_testament_frequencies = get_section_frequencies(bible_sections.new_testament)
gospels_frequencies = get_section_frequencies(bible_sections.gospels)
general_epistles_frequencies = get_section_frequencies(bible_sections.general_epistles)
pauline_epistles_frequencies = get_section_frequencies(bible_sections.pauline_epistles)

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