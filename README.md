# whtranscripts — White House Transcript Fetcher/Parser

`whtranscripts` helps you fetch and parse transcripts from the [American Presidency Project](http://www.presidency.ucsb.edu/)'s press-briefing and presidential-news-conference transcripts.

## Installation

`whtranscripts` is a Python library. To install it, run:

```sh
pip install whtranscripts
```

## Downloading Transcripts

To download the HTML of all news-conference transcripts:

```sh
mkdir ~/Downloads/conference-transcripts
python -m "whtranscripts.download" -t conference --dest ~/Downloads/conference-transcripts/
```

For press-briefings:

```sh
mkdir ~/Downloads/another-dir
python -m "whtranscripts.download" -t briefing --dest ~/Downloads/another-dir/
```


You can also limit downloads to a particular year-range, e.g., from 2001 *through* 2008:

```sh
python -m "whtranscripts.download" -t conference --dest ~/Downloads/conference-transcripts/ --start 2001 --end 2008
```

## Parsing Transcripts

You can load single transcripts from a file, URL, or the HTML itself. From a file:

```python
import whtranscripts
transcript = whtranscripts.Conference.from_path("test/pages/conferences/99975.html")
```

Alternatively, for a briefing:

```python
import whtranscripts
transcript = whtranscripts.Briefing.from_path("test/pages/briefings/47646.html")
```

From a URL:

```python
import whtranscripts
url = "http://www.presidency.ucsb.edu/ws/index.php?pid=99975"
transcript = whtranscripts.Conference.from_url(url)
```

Directly from American Presidency Project HTML:

```python
import whtranscripts
import requests
url = "http://www.presidency.ucsb.edu/ws/index.php?pid=99975"
html = requests.get(url).content
transcript = whtranscripts.Conference(html)
```

You can also load multiple at once, from a directory:

```python
import whtranscripts
transcripts = whtranscripts.Conference.from_dir("test/pages/conferences")
```

*Note: The files you want to parse from directory must end in `.html`*

## Analyzing Transcripts

Each `Conference` and `Briefing` has the following attributes:

- `doc_id`: The document ID assigned to it by the American Presidency Project.
- `date`: The date the conference or briefing took place.
- `president`: The U.S. president at the time of the briefing.
- `passages`: A list of `Passage` objects.

Each `Passage` object has the following attributes:

- `speaker`: The person who spoke the passage.
- `is_question`: `False` if the speaker was an government official/guest, `True` if they were someone from the audience.
- `text`: What was said.
- `transcript`: A pointer back to the parent transcript in which this passage can be found.
- `tokens`: All of the tokens in the passage (using NLTK's word_tokenize module). Requires NLTK to be installed.

Each `Passage` object also has the following methods:

- `get_word_count`: Returns the total word count of the passage, found by splitting on spaces.
- `count_occurrences`: Returns the total number of occurences of a string. Note: This method catches strings inside of words. So *go* will match twice on "I wish I could go somewhere a long time ago." (*go* and *ago*.) By default, this is *not* case sensitive. Pass `case_sensitive=True` to make the search case sensitive.
- `count_token_occurrences`: Similar to `count_occurrences`, but uses "tokens" generated by [NLTK](http://www.nltk.org/). Will raise an error if NLTK is not installed.

## Exporting Transcripts

You can export transcripts as CSVs, using the `TranscriptSet` class:

```python
import whtranscripts
urls = whtranscripts.download.get_urls("conference", 2013, 2013)
transcripts = map(whtranscripts.conference.Conference.from_url, urls)
t_set = whtranscripts.TranscriptSet(transcripts)
t_set.to_csv(sys.stdout)
```
