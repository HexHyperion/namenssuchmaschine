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

    print(AnsiColor.HEADER + AnsiColor.BOLD + "Programmierungsprojektsnamenssuchmaschine" + AnsiColor.CLEAR)
    to_translate = input(AnsiColor.GREY + "Name in English: " + AnsiColor.CLEAR)
    print()

    for code, language in languages:
        try:
            result = deepl_client.translate_text(to_translate, target_lang=code)
            print(result.text + AnsiColor.GREY + f" ({language})" + AnsiColor.CLEAR)
        except Exception as e:
            print(AnsiColor.RED + f"Error translating to {language}: {e}" + AnsiColor.CLEAR)
