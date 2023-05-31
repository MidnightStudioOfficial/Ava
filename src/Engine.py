import re

music_patterns = [
    (r'play (.*)', ['Playing {} now!', 'Sure, let me play some {} for you.']),
    (r'pause', ['Pausing the music now.', 'Stopping the music.']),
    (r'skip', ['Skipping to the next track.', 'Moving on to the next song.']),
    (r'favorite (?:band|artist)', ['My favorite band is Radiohead.', 'I really like Beyonce.']),
]


class ConversationalEngine():
    def __init__(self, app, lemmatize_data=True):
        self.patterns = {}
        


    def getIntent(self, utterance):
        pass


    def _lemmatize(self, value, tagMap, ignoreStopWords, lemmatizer):
        pass
    





