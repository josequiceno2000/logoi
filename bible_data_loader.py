import pandas as pd

def load_bible_data():
    """
    Loads Bible text from multiple files into a Pandas DataFrame
    Assumes each file is a book of the Bible, and that each line is a verse

    Args:
        file_paths: list of strings containing file paths to .txt files of Bible books
    
    Returns:
        data frame containing book, chapter, verse, and text info for the entire book of the Bible
    """

    file_paths = []

    # Add translations as needed:
    translation_folders = [
        "/home/jquiceno2000/workspace/github.com/josequiceno2000/logoi/raw_bible_data/nrsvce/by_book/"
    ]

    bible_books = [
        "1_chronicles.txt",
        "1_corinthians.txt",
        "1_john.txt",
        "1_kings.txt",
        "1_maccabees.txt",
        "1_peter.txt",
        "1_samuel.txt",
        "1_thessalonians.txt",
        "1_timothy.txt",
        "2_chronicles.txt",
        "2_corinthians.txt",
        "2_john.txt",
        "2_kings.txt",
        "2_maccabees.txt",
        "2_peter.txt",
        "2_samuel.txt",
        "2_thessalonians.txt",
        "2_timothy.txt",
        "3_john.txt",
        "acts.txt",
        "amos.txt",
        "baruch.txt",
        "colossians.txt",
        "daniel.txt",
        "deuteronomy.txt",
        "ecclesiastes.txt",
        "ephesians.txt",
        "esther.txt",
        "exodus.txt",
        "ezekiel.txt",
        "ezra.txt",
        "galatians.txt",
        "genesis.txt",
        "habakkuk.txt",
        "haggai.txt",
        "hebrews.txt",
        "hosea.txt",
        "isaiah.txt",
        "james.txt",
        "jeremiah.txt",
        "job.txt",
        "joel.txt",
        "john.txt",
        "jonah.txt",
        "joshua.txt",
        "jude.txt",
        "judges.txt",
        "judith.txt",
        "lamentations.txt",
        "leviticus.txt",
        "luke.txt",
        "malachi.txt",
        "mark.txt",
        "matthew.txt",
        "micah.txt",
        "nahum.txt",
        "nehemiah.txt",
        "numbers.txt",
        "obadiah.txt",
        "philemon.txt",
        "philippians.txt",
        "proverbs.txt",
        "psalms.txt",
        "revelation.txt",
        "romans.txt",
        "ruth.txt",
        "sirach.txt",
        "song_of_songs.txt",
        "titus.txt",
        "tobit.txt",
        "wisdom.txt",
        "zechariah.txt",
        "zephaniah.txt"
    ]

    for folder in translation_folders:
        for book in bible_books:
            file_paths.append(folder + book)

    data = []
    for file_path in file_paths:
        biblical_book_name = file_path.split('/')[-1].replace(".txt", "").replace("_", " ").lower().capitalize()
        with open(file_path, 'r', encoding='utf-8') as biblical_book:
            chapter = 1
            verse_number = 1
            for line in biblical_book:
                line = line.strip()
                if line.startswith("Chapter"):
                    chapter += 1
                    verse_number = 1
                    continue
                if len(line) != 0:
                    data.append({
                        "biblical_book": biblical_book_name,
                        "chapter": chapter,
                        "verse_number": verse_number,
                        "text": line
                    })
                    verse_number += 1
    return pd.DataFrame(data)     



