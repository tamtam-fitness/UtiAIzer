from src.model.models import Question, EnglishWord

Key = str


class QuestionBuilderBase:
    templates = NotImplementedError

    def __init__(self, key: str, word: EnglishWord) -> None:
        self._key = key
        self._word = word

    @classmethod
    def call(cls, key: Key, word: EnglishWord):
        return cls(key=key, word=word).__make_question()

    def __make_question(self):
        question_value = self.templates[self._key].format(word=self._word.value)
        return Question(value=question_value)

class WordQuestionBuilder(QuestionBuilderBase):
    templates = {
        "meaning": """output only the succinct meaning of "{word}" for kids""",
        "origin": """output word roots of "{word}" for kids shortly""",
        "pronunciation": """output only the IPA for "{word}" within 20 characters""",
        "pronunciation_tip": """Output the succinct pronunciation tip of "{word}" not based on IPA without preamble .Capitalize the characters should be emphasized.""",
        "example_sentence": """Using "{word}, output one example sentence". Other words are easy for kids.""",
        "making_sentence_tips": """output simple tips for making sentences with "{word}" correctly in terms on nuance and feeling for non-native speaker. Within 110 characters""",
        "synonym": """output "{word}"s one synonym .Then tell the difference between "{word}" and the other for kids within 100 characters""",
        "collocation" : """output "{word}"s collocations 6 times, separated with "|" . example : "apple pie|apple crisp" """,
    }
