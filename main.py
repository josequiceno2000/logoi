from bible_data_loader import load_bible_data
from text_preprocessing import set_stop_words, clean_text, preprocess_text
from analysis import get_word_frequencies, get_section_frequencies, print_frequencies
from bible_sections import bible_map
import nltk
from nltk.corpus import stopwords
from rich.progress import track
from colorama import Fore, Style, init
import intro

def main():
    # 0: Intro
    init(autoreset=True)
    intro.loading_animation()
    intro.show_banner()
    analysis = intro.colorful_intro()
    if analysis == "📊 Word Frequency":
        intro.select_translation()
    else:
        print("We're working on that functionality! Please check back soon.")
        return


    # 1: Generate stop words
    stop_words = set_stop_words()

    # 2: Create the Biblical Dataframe
    print("Loading biblical data...")
    biblical_dataframe = load_bible_data()
    print(Fore.GREEN + "✅ Successfully loaded Bible.\n")

    # 3: Clean and Preprocess the text
    print("Cleaning the biblical text...")
    cleaned_texts = []
    for row in track(biblical_dataframe.itertuples(), description="Cleaning...", transient=True):
        cleaned_texts.append(clean_text(row.text))
    biblical_dataframe["cleaned_text"] = cleaned_texts
    print(Fore.GREEN + "✅ Cleaning complete.\n")

    print("Preprocessing the biblical text...")
    processed_words = []
    for text in track(biblical_dataframe["cleaned_text"], description="Preprocessing...", transient=True):
        processed_words.append(preprocess_text(text, stop_words))
    biblical_dataframe["processed_words"] = processed_words
    print(Fore.GREEN + "✅ Preprocessing complete.\n")


    # 4: Group Data Frame by book and count word frequencies across a book or sections
    print("Getting word frequencies...")

    biblical_book_frequencies = {}

    grouped = biblical_dataframe.groupby("biblical_book")["processed_words"]

    for book, lists_of_words in track(grouped, description="Analyzing books...", transient=True):
        all_words = [word for sublist in lists_of_words for word in sublist]
        biblical_book_frequencies[book] = get_word_frequencies(all_words)

    print(Fore.GREEN + "✅ Got word frequencies.\n")

    words_to_display = 7

    # Loop through the books
    for biblical_book, frequencies in biblical_book_frequencies.items():
        print_frequencies(frequencies, biblical_book, words_to_display)

    # Loop through map to get section counts and print them
    for section, books in bible_map.items():
        section_frequencies = get_section_frequencies(biblical_dataframe, books)
        print_frequencies(section_frequencies, section.upper().replace("_", " "), words_to_display)

if __name__ == "__main__":
    main()
