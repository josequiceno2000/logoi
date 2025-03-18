from bible_data_loader import load_bible_data
from text_preprocessing import clean_text, preprocess_text
from analysis import get_word_frequencies, get_section_frequencies, print_frequencies
import bible_sections

# Create the Biblical Dataframe
biblical_dataframe = load_bible_data()

# Clean and Preprocess the text
print("Cleaning the biblical text...")
biblical_dataframe["cleaned_text"] = biblical_dataframe["text"].apply(clean_text)
print("Preprocessing the biblical text...")
biblical_dataframe["processed_words"] = biblical_dataframe["cleaned_text"].apply(preprocess_text)

# Group Data Frame by book and count word frequencies across a book or sections
biblical_book_frequencies = biblical_dataframe.groupby("biblical_book")["processed_words"].apply(lambda x: [word for sublist in x for word in sublist]).apply(get_word_frequencies)

words_to_display = 7

for biblical_book, frequencies in biblical_book_frequencies.items():
    print_frequencies(frequencies, biblical_book, words_to_display)


# new_testament_frequencies = get_section_frequencies(biblical_dataframe, bible_sections.new_testament)
# gospels_frequencies = get_section_frequencies(biblical_dataframe, bible_sections.gospels)
# general_epistles_frequencies = get_section_frequencies(biblical_dataframe, bible_sections.general_epistles)
# pauline_epistles_frequencies = get_section_frequencies(biblical_dataframe, bible_sections.pauline_epistles)

# print_frequencies(new_testament_frequencies, "NEW TESTAMENT", words_to_display)
# print_frequencies(gospels_frequencies, "GOSPELS", words_to_display)
# print_frequencies(new_testament_frequencies, "PAULINE EPISTLES", words_to_display)
# print_frequencies(new_testament_frequencies, "GENERAL EPISTLES", words_to_display)