import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


class SummaryController:
    def __init__(self, text, percentage, language):
        self.text = text
        self.percentage = float(percentage)
        self.language = language

    def summarize(self):
        if self.language == 'en':
            return summarize_en_text(self.text, self.percentage)
        return None


def summarize_en_text(text, percentage):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.text for token in doc]
    freq_of_word = dict()

    for word in doc:
        if word.text.lower() not in STOP_WORDS:
            if word.text.lower() not in punctuation:
                if word.text not in freq_of_word.keys():
                    freq_of_word[word.text] = 1
                else:
                    freq_of_word[word.text] += 1

    max_freq = max(freq_of_word.values())

    for word in freq_of_word.keys():
        freq_of_word[word] = (freq_of_word[word] / max_freq)

    sent_tokens = [sent for sent in doc.sents]
    sent_score = dict()
    for sent in sent_tokens:
        for word in sent:
            if word.text.lower() in freq_of_word.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = freq_of_word[word.text.lower()]
                else:
                    sent_score[sent] += freq_of_word[word.text.lower()]

    select_length = int(len(sent_tokens) * percentage)

    summary = nlargest(n=select_length, iterable=sent_score, key=sent_score.get)

    final_summary = [word.text for word in summary]

    result = ' '.join(final_summary)

    return result, len(result)
