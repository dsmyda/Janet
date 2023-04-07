class NaturalLanguageQuery:
    
    def __init__(self, nlq: str):
        # check length
        self._nlq = nlq 
        # todo parse into tokens

    def detect_pii(self):
        pass

    def as_text(self):
        return self._nlq
