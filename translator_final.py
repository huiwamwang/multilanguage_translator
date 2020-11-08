import requests
from bs4 import BeautifulSoup
import sys


args = sys.argv


class Action:

    def __init__(self):
        self.direction = None
        self.languages = ["all", "arabic", "german", "english", "spanish", "french", "hebrew", "japanese", "dutch",
                          "polish", "portuguese", "romanian", "russian", "turkish"]
        self.url = 'https://context.reverso.net/translation/'
        self.headers = {'user-agent': 'Mozilla/5.0'}
        self.src_lang = None
        self.trg_lang = None
        self.word = None
        self.translations = []
        self.sentences = []
        self.zero = False
        self.s = requests.Session()

    def start(self):
        self.src_lang = args[1]
        self.trg_lang = args[2]
        if self.trg_lang not in self.languages:
            print(f"Sorry, the program doesn't support {self.trg_lang}")
            exit()
        self.word = args[3]
        if self.trg_lang == 'all':
            self.zero = True
            self.all_languages()
        self.direction = f'{self.src_lang}-{self.trg_lang}/'
        self.connection(self.direction)

    def connection(self, direction):
        self.translations = []
        self.sentences = []
        r = self.s.get(self.url + direction + self.word, headers=self.headers)
        if r:
            soup = BeautifulSoup(r.content, 'html.parser')
            for i in soup.find_all('a', attrs={"class": 'translation'}):
                self.translations.append(i.text.strip())
            for i in soup.find_all('div', attrs={"class": ["src", "trg"]}):
                self.sentences.append(i.text.strip())
            for _ in self.sentences:
                try:
                    self.sentences.remove('')
                except ValueError:
                    if not self.zero:
                        print(f"No translation for {self.src_lang} to {self.trg_lang} yet. Sorry!")
                        exit()
                    elif self.zero:
                        with open(f'{self.word}.txt', 'r', encoding='utf-8') as f:
                            print(f.read())
                            print(f"No translation for {self.src_lang} to {self.trg_lang} yet. Sorry!")
                        exit()

            if not self.zero:
                self.finish()
            elif self.zero:
                return
        elif r.status_code == 404:
            print(f'Sorry, unable to find {self.word}')

    def finish(self):
        print(f"\n{self.trg_lang.capitalize()} Translations:")
        for i in self.translations[1:6]:
            print(i)
        print(f"\n{self.trg_lang.capitalize()} Examples:")
        for i in self.sentences[0:10]:
            print(i)

    def all_languages(self):
        try:
            with open(f'{self.word}.txt', 'r', encoding='utf-8') as f:
                print(f.read())
            exit()
        except FileNotFoundError:
            all_directions = [f'{self.src_lang}-{i}/' for i in self.languages[1:] if i != self.src_lang]
            for i in all_directions:
                self.connection(i)
                if not self.translations:
                    print(f'Sorry, unable to find {self.word}')
                    exit()
                with open(f'{self.word}.txt', 'a', encoding='utf-8') as f:
                    f.write(f"\n{i[i.find('-') + 1:-1].capitalize()} Translations:\n")
                    f.write(self.translations[1] + '\n')
                    f.write(f"\n{i[i.find('-') + 1:-1].capitalize()} Examples:\n")
                    for example in self.sentences[0:2]:
                        f.write(example + '\n')
            with open(f'{self.word}.txt', 'r', encoding='utf-8') as f:
                print(f.read())
            exit()


here_we_start = Action()
here_we_start.start()
