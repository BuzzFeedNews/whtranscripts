try:
    from nltk.tokenize import word_tokenize
    nltk_installed = True
except:
    nltk_installed = False
import sys

class Passage(object):
    
    def __init__(self, speaker, text, transcript):
        self.speaker = speaker
        self.is_question = True if speaker == "Q" else False
        self.text = text
        self.transcript = transcript
        if nltk_installed:
            self.tokens = word_tokenize(self.text)

    def get_word_count(self):
        return len(self.text.split())
        
    def count_occurrences(self, string, case_sensitive=False):
        if case_sensitive:
            return self.text.count(string)
        else:
            return self.text.lower().count(string.lower())
    
    def count_token_occurrences(self, string, case_sensitive=False):
        try:
            if case_sensitive:
                return len([ t for t in self.tokens if t == string ])
            else:
                return len([ t for t in self.tokens if t.lower() == string.lower() ])
        except AttributeError:
            sys.stderr.write("!!! Tokenizing requires NLTK. It appears you don't have it installed.\n")
