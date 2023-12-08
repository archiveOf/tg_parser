import pymorphy2
import re


class TextProcessor:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def lemmatize_text(self, text):
        words = text.split()
        lemmatized_words = [self.lemmatize_word(word) for word in words]
        return ' '.join(lemmatized_words)

    def lemmatize_word(self, word):
        parsed_word = self.morph.parse(word)[0]
        return parsed_word.normal_form

    def highlight_words(self, text, word_list):
        text.split()
        for word in word_list:
            pattern = re.compile(r'\b' + re.escape(word) + r'\b', flags=re.IGNORECASE)
            text = pattern.sub(f'<b><i><u>{word}</u></i></b>', text)
        return text

    def highlight_lemmatized(self, original_text, lemmatized_words):
        original_words = original_text.split()

        for i in range(len(original_words)):
            word = original_words[i].strip('.,?!')  # Убираем знаки препинания для корректного сравнения
            lemmatized_word = self.lemmatize_word(word.lower())  # Лемматизируем и приводим к нижнему регистру
            if lemmatized_word in lemmatized_words:
                original_words[i] = f'<b><i><u>{original_words[i]}</u></i></b>'

        return ' '.join(original_words)

    def get_result(self, text, keywords):
        res_txt = text

        if any(word in text for word in keywords['minus_valid_word']):
            return

        lemmatized_text = self.lemmatize_text(text)
        if any(word in lemmatized_text for word in keywords['minus_lemma']):
            return

        if any(word in text for word in keywords['valid_word']):
            res_txt = self.highlight_words(text, keywords['valid_word'])

        if any(word in lemmatized_text for word in keywords['first_lemma']):
            res_txt = self.highlight_lemmatized(res_txt, keywords['first_lemma'])

        if any(word in lemmatized_text for word in keywords['second_lemma']):
            res_txt = self.highlight_lemmatized(res_txt, keywords['second_lemma'])

        return res_txt
