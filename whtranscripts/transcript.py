# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys, os
import re
import datetime as dt
import lxml.html
import requests
import itertools
import glob
from . import patterns
from . import fixes
from . import passage
flatten = lambda x: list(itertools.chain.from_iterable(x))

end_punctuation = [".", "!", "?", "-", "]", u"—", u"–", '"', ",", ":", ")", ";"]
not_header = ["Thank you", "We'll", "What's", "Item", "any questions", "involving", "dated"]
safe_speakers = [
    'White House Press Secretary James "Jay" Carney',
    'White House Press Secretary James F. "Jay" Carney',
    'White House Principal Deputy Press Secretary Joshua R. Earnest',
    'Charles G. Ross, Secretary To The President',
    'White House Press Secretary Robert L. Gibbs'
]

class TranscriptSet(object):

    def __init__(self, transcripts):
        self.transcripts = transcripts

    def to_csv(self, dest, **kwargs):
        import pandas as pd
        passages = flatten([ [ {
            "doc_id": t.doc_id,
            "date": t.date,
            "speaker": (p.speaker or ""),
            "text": (p.text or "")
        } for p in t.passages ]
            for t in self.transcripts ])
        df = pd.DataFrame(passages)
        df.to_csv(dest, index=False, **kwargs)
        
class Transcript(object):

    @classmethod
    def from_url(cls, url):
        html = requests.get(url).content
        return cls(html)

    @classmethod
    def from_path(cls, path):
        with open(path, "rb") as f:
            return cls(f.read())
        
    @classmethod
    def from_dir(cls, directory):
        paths = glob.glob(os.path.join(directory, "*html"))
        docs = list(map(cls.from_path, paths))
        return docs

    def __init__(self, html):
        if type(html) == bytes:
            self.html = html.decode("windows-1251")
        else:
            self.html = html
        self._parse()
        self.passages = self._make_passages()

    def _parse(self):
        self.doc_id = re.search(patterns.doc_id, self.html).group(1)
        cleaned = re.sub(patterns.ptag, "\n", self.html)
        dom = lxml.html.fromstring(cleaned)
        self.president = dom.cssselect("title")[0].text_content().split(":")[0]
        self.text = dom.cssselect(".displaytext")[0].text_content()
        if self.doc_id in fixes.fixers:
            self.text = fixes.fixers[self.doc_id](self.text)
        else: pass
        # This is a pretty aggressive decision to remove all bracketed text
        self.text = re.sub(patterns.bracketed_text, "", self.text)
        self.text = self.text.strip()
        try:
            date_str = dom.cssselect(".docdate")[0].text_content()
            self.date = dt.datetime.strptime(date_str, "%B %d, %Y").date()
        except ValueError:
            sys.stderr.write("!!! CANNOT FIND DATE FOR {0}\n".format(path))
            self.date = None

    def _make_passages(self):
        passages = []
        current_speaker = None
        current_topic = None
        for t in self.text.split("\n"):
            split_text = re.match(self.speaker_pattern, t).groups()
            speaker = split_text[0]
            passage_text = split_text[1].strip()
            if speaker:
                current_speaker = re.sub(self.speaker_cleaner_pattern, "", speaker.title()).strip("-").strip(",").strip(".").strip(":")
                if len(current_speaker.split()) > 6 and current_speaker not in safe_speakers:
                    sys.stderr.write("Found odd speaker: {0} on {1}\n".format(current_speaker, self.date))
                else: pass
            else: pass
            if passage_text and (not speaker) and \
                (len(passage_text.split()) < 14) and \
                (passage_text[-1] not in end_punctuation) and \
                (passage_text[0] not in ["-", '"']) and \
                not any([ nh in passage_text for nh in not_header]):
                current_topic = t
            elif passage_text:
                p = passage.Passage(current_speaker, passage_text, self)
                passages.append(p)
            else: pass
        return passages
    
    def get_word_count(self, include_questions=False):
        return sum([ p.get_word_count() for p in self.passages
            if (include_questions or not p.is_question) ])
    
    def count_occurrences(self, string, include_questions=False, **kwargs):
        return sum([ p.count_occurrences(string, **kwargs) for p in self.passages
            if (include_questions or not p.is_question) ])
