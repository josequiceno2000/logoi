from pyfiglet import Figlet
from InquirerPy import inquirer
from colorama import Fore, Style, init
import time, sys


def show_banner():
    figlet = Figlet(font='isometric1')
    banner = (figlet.renderText('Logoi'))
    print("\n" + Fore.CYAN + banner)

def colorful_intro():
    init(autoreset=True)
    print(Fore.CYAN + "\nWelcome to the " + Style.BRIGHT + Fore.CYAN + "Ultimate Biblical NLP Tool.\n")
    
    analysis = inquirer.select(
        message="What kind of analysis shall we perform today?",
        choices= [
            "📊 Word Frequency",
            "🤝 Collocation",
            "⛓️ N-gram",
            "🔑 Keyword Extraction",
            "💭 Sentiment",
            "📈 Lexical Diversity"
        ],
        default="Word Frequency"
    ).execute()

    return analysis

def loading_animation():
    print("Initializing Logoi", end="")
    for _ in range(5):
        time.sleep(0.2)
        print(".", end="")
        sys.stdout.flush()


def select_translation():
    translation = inquirer.select(
        message="Which biblical translation should we use?",
        choices= [
            "New Revised Standard Version - Catholic Edition",
            "Revised Standard Version - Catholic Edition",
            "Revised Standard Version - Second Catholic Edition",
            "New American Bible, Revised Edition",
            "Jerusalem Bible",
            "Douay-Rheims Bible"
        ],
        default="New Revised Standard Version - Catholic Edition"
    ).execute()

    return translation