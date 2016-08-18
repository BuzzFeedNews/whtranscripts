import whtranscripts as wht

urls = wht.download.get_urls("briefing", 2013, 2013)

def test_basic():
    assert(len(urls) == 223)

def test_url():
    expected_url = "http://www.presidency.ucsb.edu/ws/index.php?pid=102819"
    url = urls[0]
    assert(url == expected_url)
    doc = wht.Briefing.from_url(url)
    assert(doc.get_word_count() > 1000)
    assert(doc.president == "Barack Obama")
    assert(str(doc.date) == "2013-01-07")

def from_id(id_str):
    url = "http://www.presidency.ucsb.edu/ws/index.php?pid=" + id_str
    return wht.Briefing.from_url(url)

def test_61116():
    b = from_id("61116")
    assert(b.count_occurrences("good") == 3)
    assert(b.count_occurrences("version") == 3)
    assert(b.count_occurrences("version", include_questions=True) == 7)
    assert(sum(map(lambda x: x.is_question, b.passages)) == 45)
    assert(sum(map(lambda x: not x.is_question, b.passages)) == 59)
    assert(b.passages[0].text == "Good morning. Okay, let me give you a couple items. You have the statement on Senator Thurmond, so I won't repeat that, you already have it on the record, it's been distributed on the ground electronically and otherwise.")
    assert(b.passages[-1].text == "I didn't indicate that. I didn't indicate anything one way or another. I just said, he just died so people are now just looking at the arrangements. We'll let you know, of course; but it's too soon to say.")

def test_25032():
    b = from_id("25032")
    assert(b.passages[0].text == "I have two announcements, and then I'll take questions. It has been 65 days since the President requested emergency funding for our troops. Our military leaders have said they need this funding by mid-April to avoid significant disruptions and hardships. Yet the Senate's Majority Leader insists that they will be fine until June, and yesterday said the urgency is only in the President's head.")
    assert(b.passages[-1].text == "Thank you.")
    assert(b.count_occurrences("national security") == 10)
    assert(b.count_occurrences("national security", case_sensitive=True) == 2)

def test_105511():
    b = from_id("105511")
    assert(b.passages[0].text == "Hi, everyone. Thanks for joining on what we know has been a fairly busy Friday for you. Today we're going to do a preview of the President's trip to Europe next week. Our speaker is Deputy National Security Advisor for Strategic Communications, Ben Rhodes. He'll be speaking to you on the record, and there's no embargo on this call.")
    assert(b.passages[-1].text == "Thanks.")

def test_79163():
    b = from_id("79163")
    assert(b.passages[0].text == "Good afternoon, ladies and gentlemen. It's good to be with you again to give you another update on homeland security. As I mentioned to you yesterday the President wants us to continue to update the American people with as much factual information as we can, as often as we can. So, today the senior officials you see here will give you the latest updates from their various areas of responsibility.")
    assert(b.passages[-1].text == "Sometime in December of this year.")
