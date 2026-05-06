import deepl
import os
from dotenv import load_dotenv
from languages import languages
import threading
import time

class AnsiColor:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GREY = "\033[90m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ITALIC = "\033[3m"
    CLEAR = "\033[0m"

def print_progress():
    dots = 3
    delay = 0
    while True:
        if(delay % 6 == 0):
            if dots < 3:
                dots += 1
            else:
                dots = 1
        print(
            f"\r{AnsiColor.CYAN}Translating, this may take a while️{"." * dots}{" " * (3 - dots)}{AnsiColor.CLEAR} {AnsiColor.GREY}({len(translations)}/{len(languages)}){AnsiColor.CLEAR}",
            end="")
        global stop_threads
        if stop_threads:
            break
        time.sleep(0.1)
        delay += 1

def download_translations(word, translations):
    for code, language in languages:
        try:
            result = deepl_client.translate_text(to_translate, target_lang=code, source_lang="EN")
            translations.append((result.text, language))

        except Exception as e:
            print()
            print(f"{AnsiColor.RED}Error translating to {language}: {e}{AnsiColor.CLEAR}", end="")

if __name__ == "__main__":
    load_dotenv()
    auth_key = os.getenv("DEEPL_API_KEY")
    deepl_client = deepl.DeepLClient(auth_key)

    print(f"{AnsiColor.HEADER}{AnsiColor.BOLD}Programmierungsprojektsnamenssuchmaschine{AnsiColor.CLEAR}")
    to_translate = input(f"{AnsiColor.GREY}Expression in English: {AnsiColor.CLEAR}")
    print(f"{AnsiColor.CYAN}Translating, this may take a while️... {AnsiColor.CLEAR} {AnsiColor.GREY}(0/{len(languages)}){AnsiColor.CLEAR}", end="")

    translations = []
    stop_threads = False

    translationThread = threading.Thread(target=download_translations, args=(to_translate, translations))
    printThread = threading.Thread(target=print_progress)

    translationThread.start()
    printThread.start()

    translationThread.join()
    stop_threads = True
    printThread.join()

    translations.sort(key=lambda x: x[1], reverse=False)
    max_length = max(len(f"{translation[0]} ({translation[1]})") for translation in translations)

    print()
    for i in range(0, len(translations), 3):
        row = translations[i:i+3]
        for translation in row:
            print(f"{translation[0]} {AnsiColor.GREY}({translation[1]}){AnsiColor.CLEAR}".ljust(max_length + 10), end="")
        print()
    print()
