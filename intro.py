from pyfiglet import Figlet
from colorama import Fore, Style, init
import time, sys


def show_banner():
    figlet = Figlet(font='isometric1')
    banner = (figlet.renderText('Logoi'))
    print("\n" + Fore.CYAN + banner)

def colorful_intro():
    init(autoreset=True)
    print(Fore.CYAN + "\nWelcome to the " + Style.BRIGHT + Fore.CYAN + "Ultimate Biblical NLP Tool.")
    analysis = input("\nWhat kind of analysis will you perform today?\n[1] Word Frequency\n[2] Collocation\n[3] N-gram\n[4] Keyword Extraction\n[5] Sentiment\n[6] Lexical Diversity")
    return analysis

def loading_animation():
    print("Initializing Logoi ", end="")
    for _ in range(7):
        time.sleep(0.3)
        print(".", end="")
        sys.stdout.flush()