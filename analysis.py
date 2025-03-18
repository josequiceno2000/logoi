from collections import Counter

def get_word_frequencies(words):
    return Counter(words)

def get_section_frequencies(biblical_dataframe, biblical_set):
    section_dataframe = biblical_dataframe[biblical_dataframe["biblical_book"].isin(biblical_set)]
    cumulative_words = [word for sublist in section_dataframe["processed_words"] for word in sublist]
    return Counter(cumulative_words)

def print_frequencies(frequencies, title, words_to_display):
    book_title = f"\n--- {title.upper()} ---"
    book_title_length = len(book_title) - 1
    print(book_title)

    for word, count in frequencies.most_common(words_to_display):
        result = f"{word.title()}: {count}"
        print(result)

    print("-" * book_title_length)