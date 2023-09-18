from model.models import EnglishWord, Question

Key = str


class QuestionBuilderBase:
    templates: dict[Key, str] = {}

    def __init__(self, key: str, word: EnglishWord) -> None:
        self._key = key
        self._word = word

    @classmethod
    def call(cls, key: Key, word: EnglishWord) -> Question:
        return cls(key=key, word=word).__make_question()

    def __make_question(self) -> Question:
        question_value = self.templates[self._key].format(word=self._word.value)
        return Question(value=question_value)


class WordQuestionBuilder(QuestionBuilderBase):
    templates = {
        "meaning": """output the meaning of "{word}" shortly within 80 characters""",
        "origin": """output word derivation of "{word}" within 100 characters""",
        "pronunciation": """output only the IPA for "{word}" within 20 characters""",
        "pronunciation_tip": """Output the pronunciation tip of "{word}" not based on IPA without preamble .Capitalize the characters should be emphasized. e.g: OHN-lee""",  # noqa
        "example_sentence": """Using "{word}, output one example sentence within 70 characters".""",
        "making_sentence_tips": """output tips for making sentences using "{word}" in terms on nuance and feeling for non-native speaker. Within 80 characters""",  # noqa
        "synonym": """output "{word}"s one synonym .Then tell the difference between "{word}" and the other within 100 characters""",  # noqa
        "antonym": """output "{word}"s one antonym .""",
        "collocation": """output "{word}"s collocations 7 times following grammer, separated with "|" . e.g: "{word} noun|{word} verb" """,  # noqa
    }
