import deepl
import os
from dotenv import load_dotenv
from languages import languages


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


if __name__ == "__main__":
    load_dotenv()
    auth_key = os.getenv("DEEPL_API_KEY")
    deepl_client = deepl.DeepLClient(auth_key)

    print(f"{AnsiColor.HEADER}{AnsiColor.BOLD}Programmierungsprojektsnamenssuchmaschine{AnsiColor.CLEAR}")
    to_translate = input(f"{AnsiColor.GREY}Expression in English: {AnsiColor.CLEAR}")
    print(f"{AnsiColor.CYAN}Translating, this may take a while...{AnsiColor.CLEAR}")

    translations = []
    for code, language in languages:
        try:
            result = deepl_client.translate_text(to_translate, target_lang=code, source_lang="EN")
            translations.append((result.text, language))
        except Exception as e:
            print(f"{AnsiColor.RED}Error translating to {language}: {e}{AnsiColor.CLEAR}")

    translations.sort(key=lambda x: x[1], reverse=False)
    max_length = max(len(f"{translation[0]} ({translation[1]})") for translation in translations)

    print()
    for i in range(0, len(translations), 3):
        row = translations[i:i+3]
        for translation in row:
            print(f"{translation[0]} {AnsiColor.GREY}({translation[1]}){AnsiColor.CLEAR}".ljust(max_length + 10), end="")
        print()
    print()