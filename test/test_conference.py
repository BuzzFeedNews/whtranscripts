import whtranscripts as wht
import six

urls = wht.download.get_urls("conference", 2013, 2013)

def test_basic():
    assert(len(urls) == 22)

def test_url():
    doc = wht.conference.Conference.from_url("http://www.presidency.ucsb.edu/ws/index.php?pid=57090")
    assert(doc.get_word_count() > 1000)
    assert(doc.president == "William J. Clinton")
    assert(str(doc.date) == "1999-02-19")
    assert(len(doc.passages) == 54)
    assert(doc.passages[-1].text == "Thank you very much.")
    assert(doc.passages[-1].speaker == "President Clinton")

def test_csv():
    urls = wht.download.get_urls("conference", 2013, 2013)
    transcripts = map(wht.conference.Conference.from_url, urls)
    t_set = wht.TranscriptSet(transcripts)
    t_set.to_csv(six.StringIO(), encoding="utf-8")
