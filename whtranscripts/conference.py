from __future__ import absolute_import
from . import patterns
from . import transcript

class Conference(transcript.Transcript):
    document_type = "conference"
    speaker_pattern = patterns.conference_speaker
    speaker_cleaner_pattern = patterns.conference_speaker_cleaner
