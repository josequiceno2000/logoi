import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

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
    words = word_tokenize(text) 
    stop_words = set(stopwords.words('english')) 
    stop_words.update(["said", "say", "says"])
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

    verb_map = {"came": "come"}
    final_words = [verb_map.get(word, word) for word in final_words]
    return final_words