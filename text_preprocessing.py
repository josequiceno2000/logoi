import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from InquirerPy import inquirer
import nltk

def get_default_stop_words():
    """Returns a set of default stop words."""
    default_stop_words = set(stopwords.words('english'))
    additional_stop_words = {"said", "say", "says", "shall", "like", "let", "may"}
    return default_stop_words.union(additional_stop_words)

def get_user_excluded_words():
    """Gets user-specified excluded words."""
    user_excluded_words = input("\nOkay! Which words shall we exclude? [Type words separated by a space]\n» ").split()
    return user_excluded_words

def set_stop_words():
    """
    Makes a set of default and user-specified stop-words.
    """
    stop_words = get_default_stop_words()

    will_exclude_words = inquirer.select(
        message="Should we exclude any words from analysis?",
        choices= [
            "Yes",
            "No"
        ],
        default="No"
    ).execute()

    if will_exclude_words == "Yes":
        user_excluded_words = get_user_excluded_words()
        print(f"\nGot it. Beginning analysis while excluding {[word for word in user_excluded_words]}...\n")
        stop_words.update(user_excluded_words)
    else:
        print("\nOkay! Beginning analysis...\n")
        return stop_words

    return stop_words

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

def preprocess_text(text, stop_words):
    """
    Takes cleaned text and tokenizes, removes stop words, lemmatizes, and corrects "u" to "us".
    """
    words = word_tokenize(text)
    word_map = {"gods": "god"}
    words = [word_map.get(word, word) for word in words]
    filtered_words = [word for word in words if word not in stop_words]
    pos_tags = nltk.pos_tag(filtered_words)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = []
    for word, tag in pos_tags:
        # Check if the word is a verb
        if tag == "VBZ":
            lemmatized_words.append(lemmatizer.lemmatize(word, 'v'))
        else:
            lemmatized_words.append(lemmatizer.lemmatize(word))
    final_words = ["us" if word == "u" else word for word in lemmatized_words]
    verb_map = {"came": "come",}
    final_words = [verb_map.get(word, word) for word in final_words]
    return final_words