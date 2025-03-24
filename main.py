from bible_data_loader import load_bible_data
from text_preprocessing import clean_text, preprocess_text
from analysis import get_word_frequencies, get_section_frequencies, print_frequencies
from bible_sections import bible_map
import nltk
from nltk.corpus import stopwords

# Initialize stop words
stop_words = set(stopwords.words('english'))
stop_words.update(["said", "say", "says"])

# Ask user if they want to exclude certain words from analysis:
will_exclude_words = input("Should we exclude any words from analysis? [Type y/n]:\n").lower()

while will_exclude_words != "y" and will_exclude_words != "n":
    print(f"\nError: That is not a valid response.")
    will_exclude_words = input("\nShould we exclude any words from analysis? [Type y/n]:\n").lower()

if will_exclude_words == "y":
    user_excluded_words = input(
        "\nOkay! Which words shall we exclude? [Type words separated by a space]\n"
        "Example: god try call\n"
    ).split()
    print(f"\nGot it. Beginning analysis while excluding {[word for word in user_excluded_words]}...")
    stop_words.update(user_excluded_words)
elif will_exclude_words == "n":
    print("\nOkay! Beginning analysis...\n")

# Create the Biblical Dataframe
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
    print_frequencies(section_frequencies, section.upper(), words_to_display)
# new_testament_frequencies = get_section_frequencies(biblical_dataframe, bible_sections.new_testament)
# gospels_frequencies = get_section_frequencies(biblical_dataframe, bible_sections.gospels)
# general_epistles_frequencies = get_section_frequencies(biblical_dataframe, bible_sections.general_epistles)
# pauline_epistles_frequencies = get_section_frequencies(biblical_dataframe, bible_sections.pauline_epistles)

# print_frequencies(new_testament_frequencies, "NEW TESTAMENT", words_to_display)
# print_frequencies(gospels_frequencies, "GOSPELS", words_to_display)
# print_frequencies(new_testament_frequencies, "PAULINE EPISTLES", words_to_display)
# print_frequencies(new_testament_frequencies, "GENERAL EPISTLES", words_to_display)