from bible_data_loader import load_bible_data
from text_preprocessing import set_stop_words, clean_text, preprocess_text
from analysis import get_word_frequencies, get_section_frequencies, print_frequencies
from bible_sections import bible_map
import nltk
from nltk.corpus import stopwords

# Generate stop words
stop_words = set_stop_words()

# Create the Biblical Dataframe
print("Loading biblical data...")
biblical_dataframe = load_bible_data()

# Clean and Preprocess the text
print("Cleaning the biblical text...")
biblical_dataframe["cleaned_text"] = biblical_dataframe["text"].apply(clean_text)
print("Preprocessing the biblical text...")
biblical_dataframe["processed_words"] = biblical_dataframe["cleaned_text"].apply(lambda x: preprocess_text(x, stop_words))

# Group Data Frame by book and count word frequencies across a book or sections
biblical_book_frequencies = biblical_dataframe.groupby("biblical_book")["processed_words"].apply(lambda x: [word for sublist in x for word in sublist]).apply(get_word_frequencies)

words_to_display = 7

for biblical_book, frequencies in biblical_book_frequencies.items():
    print_frequencies(frequencies, biblical_book, words_to_display)


# Loop through map to get section counts and print them
for section, books in bible_map.items():
    section_frequencies = get_section_frequencies(biblical_dataframe, books)
    print_frequencies(section_frequencies, section.upper().replace("_", " "), words_to_display)
