import requests
from bs4 import BeautifulSoup


class Action:

    def __init__(self):
        self.direction = None
        self.languages = {1: "Arabic", 2: "German", 3: "English", 4: "Spanish", 5: "French", 6: "Hebrew", 7: "Japanese",
                          8: "Dutch", 9: "Polish", 10: "Portuguese", 11: "Romanian", 12: "Russian", 13: "Turkish"}
        self.url = 'https://context.reverso.net/translation/'
        self.headers = {'user-agent': 'Mozilla/5.0'}
        self.src_lang = None
        self.trg_lang = None
        self.word = None
        self.translations = []
        self.sentences = []

    def start(self):
        print("Hello, you're welcome to the translator. Translator supports:")
        for key, value in self.languages.items():
            print(key, value, sep='. ')
        self.src_lang = int(input('Type the number of your language:\n'))
        self.trg_lang = int(input("Type the number of a language you want to translate to or '0' to translate to all "
                                  "languages:\n"))
        self.word = input('Type the word you want to translate:\n')
        """if self.trg_lang == 0:
            self.all_languages()"""
        self.direction = f'{self.languages[self.src_lang].lower()}-{self.languages[self.trg_lang].lower()}/'
        print(self.direction)
        self.connection()

    def connection(self):
        r = requests.get(self.url + self.direction + self.word, headers=self.headers)
        if r:
            print(str(r.status_code) + " " + "OK")
            soup = BeautifulSoup(r.content, 'html.parser')
            text = soup.find_all('a', attrs={"class": 'translation'})
            sentences = soup.find_all('div', attrs={"class": ["src", "trg"]})
            for i in text:
                self.translations.append(i.text.strip())
            for i in sentences:
                self.sentences.append(i.text.strip())
            self.finish()

    def finish(self):
        print(f"\nContext examples:\n\n{self.languages[self.trg_lang]} Translations:")
        for i in self.translations[1:6]:
            print(i)
        print(f"\n{self.languages[self.trg_lang]} Examples:")
        for i in self.sentences[0:20]:
            print(i)

    """def all_languages(self):
        all = [f'{self.languages[self.src_lang].lower()}-{self.languages[key].lower()}/' for key in
               self.languages.keys() if key != self.src_lang]
        for i in all:
            r = requests.get(self.url + i + self.word, headers=self.headers)
            if r:
                soup = BeautifulSoup(r.content, 'html.parser')
                text = soup.find('a', attrs={"class": "translation ltr dict n"})
                sentences = soup.find_all('div', attrs={"class": ["src ltr", "trg ltr"]})
                with open(f'{self.word}.txt', 'a', encoding='utf-8') as f:
                    f.write()"""


here_we_start = Action()
here_we_start.start()

"""for i in all:
    r = requests.get(url + i + word, headers=headers)
    if r:
        soup = BeautifulSoup(r.content, 'html.parser')
        text = soup.find('a', attrs={'class': 'translation ltr dict n'})
        sentences = soup.find_all('div', attrs={"class": ["src ltr", "trg ltr"]})
        for i in text:
            print(i.text.strip())
        for i in sentences:
            print(i.text.strip())"""
