import re
import string

doc_id = re.compile(r"pid=(\d+)")

ptag = re.compile(r"(<p.*?>|<P>|<br>)+")

conference_speaker_subpatterns = [
    r"Q:?\.?[ \-]",
    r"The President[:\.,] ",
    r"THE\.? PRESIDENT[:\.,]",
    r"PRESIDENT [\w\- ]{0,15}[:\.,]",
    r"President [\w\- ]{0,15}[:\.] ",
    r"King [\w\- ]{0,12}[:\.] ",
    r"Chancellor [\w\- ]{0,20}[:\.] ",
    r"Prime Minister [\w\- ]{0,20}[:\.] ",
    r"Director [\w\- ]{0,25}[:\.] ",
    r"GOVERNOR [\w\- ]{0,15}[:\.] ",
    r"Mr\. [\w\- ]{0,25}[:\.] ",
    r"MR\. [\w\- ]{0,25}[:\.] ",
    r"MRS\. [\w\- ]{0,25}[:\.] ",
    r"Merriman Smith, [\w\- ]*: ",
    r"[\w\-]{0,15} [\w\-]{0,15}, United Press: ",
    r"[\w\-]{0,15} [\w\-]{0,15}, United Press International: ",
    r"[\w\-]{0,15} [\w\-]{0,15}, Associated Press: ",
    r"[\w\-]{0,15} [\w\-]{0,15}, Washington Star: ",
    r'White House Press Secretary James F\. "Jay" Carney[:\.] ',
    r'White House Press Secretary James "Jay" Carney[:\.] ',
    r'White House Press Secretary Robert L\. Gibbs[:\.] ',
    r'White House Principal Deputy Press Secretary Joshua R\. Earnest[:\.] ',
    r"White House [\w ]{0,20} [A-Za-z ]{0,25}[:\.] ",
    # Particularly special cases:
    r"Robert Nixon, International News Service: ",
    r"William Hillman, Mutual Broadcasting System: ",
    r"Anthony Leviero, New York Times: ",
    r"Frank Bourgholtzer, National Broadcasting Company: ",
    r"Carrol Linkins, Western Union: ",
    r"Garnett Homer, Washington Evening Star: ",
    r"John Steele, Time Magazine: ",
    r"Marianne Means, King Features Syndicate: ",
    r"Sid Davis, Westinghouse Broadcasting: ",
    r"Peter Lisagor, Chicago Daily News: ",
    r"Forrest Boyd, Mutual Broadcasting System: ",
    r"Robert Pierpoint, Cbs News: ",
    r"Catherine Mackin, Hearst Newspapers: ",
    r"John Scull, Abc News: ",
    r"Richard Wightman, Fairchild Newspapers: ",
    r"Max Frankel, New York Times: ",
    r"Richard Mcgowan, New York Daily News: ",
    r"Carroll Kilpatrick, The Washington Post: ",
    r"Marvin L\. Arrowsmith, Associated Press: ",
    r"Mr\. Hagerty: ",
    r"Secretary General de Hoop Scheffer\. ",
    r"CHARLES G. ROSS, Secretary to the President: ",
    r"Secretary General Lord Robertson\. ",
    r"President Barco Vargas of Colombia\. ",
    r"President Jose Manual Durao Barroso\. ",
    r"DR\. JOHN VAN SCHAICK: ",
    r"EUGENE C. PATTERSON\. ",
    r"PRIME MINISTER MACKENZIE KING: ",
    r"FRANK AUKOFER\. ",
    r"MR\. SHORT\.",
    r"The Chancellor\. ",
    r"REPORTER\. ",
    r"Moderator\. ",
    r"THE PRESIDENT",
    r"THE President\. ",
    r"The Prime Minister\. ",
    r"Q\. [\w\-\., ]{0,25}:"
]

conference_speaker = re.compile(r"^\s*({0})?(.*$)".format(r"|".join(conference_speaker_subpatterns)), re.UNICODE)

conference_speaker_cleaner = re.compile(r"(\.?:? $)")

briefing_speaker = re.compile(r"^\s*(Q |Q: |[A-Z]{2}[^:]*[A-Z]{2}: )?(.*$)", re.UNICODE)
briefing_speaker_cleaner = re.compile(r":? $")

footnote = re.compile(r"\[[1-9][0-9]?\.?\-?\]")
bracketed_text = re.compile(r"[\[\(][^\]\)]*[\]\)]")

punctuation = re.compile(r"[\s{}]+".format(re.escape(string.punctuation)))
