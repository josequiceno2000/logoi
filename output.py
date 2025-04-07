import csv, os
from collections import Counter
from rich.progress import track
import plotly.express as px
import pandas as pd

def export_frequencies_to_csv(freq_dict: dict, folder_name, translation, filename="word_frequencies.csv"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, filename)

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([f"Word Frequencies in {translation.upper()}"])
        writer.writerow(["Book", "Word", "Frequency"])

        total_words = sum(len(counter) for counter in freq_dict.values())
        progress_data = []

        for book, counter in freq_dict.items():
            for word, freq in counter.most_common():
                progress_data.append([book, word, freq])
        
        for row in track(progress_data, description="Writing to CSV..."):
            writer.writerow(row)
    
    return file_path

def plot_top_words(counter, book_name, top_n=10):
    top_words = counter.most_common(top_n)
    dataframe = pd.DataFrame(top_words, columns=["Word", "Frequency"])
    fig = px.bar(dataframe, x="Word", y="Frequency", title=f"{top_n} Most Frequent Words in {book_name}")
    fig.show()