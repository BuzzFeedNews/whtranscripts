import whtranscripts as wht
import requests

def test_parsing():
    from_path = wht.Conference.from_path("test/pages/conferences/99975.html")
    assert(from_path.president == "Barack Obama")

    from_path_b = wht.Briefing.from_path("test/pages/briefings/47646.html")
    assert(from_path_b.president == "William J. Clinton")

    url = "http://www.presidency.ucsb.edu/ws/index.php?pid=99975"
    from_url = wht.Conference.from_url(url)
    assert(from_url.president == "Barack Obama")

    html = requests.get(url).content.decode("windows-1251")
    from_html = wht.Conference(html)
    assert(from_html.president == "Barack Obama")

    from_dir = wht.Conference.from_dir("test/pages/conferences")
    assert(from_dir[0].president == "Barack Obama")
