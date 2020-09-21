class AutoCompleteData:
    def __init__(self, completed_sentence, source_text, offset, score=0):
        self.completed_sentence = completed_sentence
        self.source_text = source_text
        self.offset = offset
        self.score = score

    def set_score(self, points_to_decrement):
        self.score -= points_to_decrement

    @staticmethod
    def get_score(word):

        return len(word) * 2