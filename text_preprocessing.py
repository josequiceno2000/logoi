import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

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
    words = word_tokenize(text) # Tokenize words in each sentence
    stop_words = set(stopwords.words('english')) # Get a list of stopwords
    filtered_words = [word for word in words if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
    final_words = ["us" if word == "u" else word for word in lemmatized_words]
    return final_words