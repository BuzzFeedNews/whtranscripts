from __future__ import absolute_import
from . import transcript
from . import patterns

class Briefing(transcript.Transcript):
    document_type = "briefing"
    speaker_pattern = patterns.briefing_speaker
    speaker_cleaner_pattern = patterns.briefing_speaker_cleaner
