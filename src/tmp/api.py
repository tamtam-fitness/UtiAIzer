import asyncio
import json
from functools import reduce

import app.settings as settings
import openai

openai.api_key = settings.OPEN_AP_API_KEY


class ChatGPTClient:
    @classmethod
    def async_call(cls, questions):
        result_dict = asyncio.run(cls(questions).__async_call())
        return result_dict

    def __init__(self, questions) -> None:
        self.__questions = questions

    async def __async_call(self):
        tasks = []
        for question in self.__questions:
            task = asyncio.create_task(self.__ask_chatgpt_async(question))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        result_dict = reduce(lambda x, y: {**x, **y}, results)
        return result_dict

    @staticmethod
    async def __ask_chatgpt_async(question):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            top_p=1,
            temperature=0,
            messages=[
                {"role": "user", "content": question.text},
            ],
        )
        return {question.key: response.choices[0]["message"]["content"].strip()}


from dataclasses import dataclass


@dataclass
class Question:
    key: str
    text: str


class QuestionBuilder:
    templates = NotImplementedError

    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs

    @classmethod
    def call(cls, **kwargs):
        return cls(**kwargs).__call()

    def __call(self):
        return [
            Question(key, self.__make_question_async(key))
            for key in self.templates.keys()
        ]

    def __make_question_async(self, key):
        return self.templates[key].format(**self.kwargs)


class WordQuestionBuilder(QuestionBuilder):
    # WordQuestionは全てのこのワードが全部大事だしなー。

    templates = {
        "pronaunciation": """output only the IPA for "{word}" within 20 characters""",
        "meaning_ja": """Output only the meaning for "{word}" within 20 characters.lang:ja""",
        "meaning_en": """output only the succinct meaning of "{word}" for kids""",
        "pronaunciation_tips": """Output the succinct pronunciation tip of "{word}" not based on IPA without preamble .Capitalize the characters should be emphasized.""",
        "example_sentence": """Output one example sentence with "{word}". Other words are simple.""",
        "making_sentence_tips": """output simple tips for making sentences with "{word}" correctly in terms on nuance and feeling for non-native speaker. Within 110 characters""",
        "synonym": """output "{word}"s one synonym .Then tell the difference between "{word}" and the other for kids within 100 characters""",
    }


class SentenceFeedBackBuilder(QuestionBuilder):
    templates = {
        "grammar_correction": """correct grammar for "{sentence}" within 100 characters""",
    }


# Main program
def main():
    questions = WordQuestionBuilder.call(word="imprudent")
    # questions = SentenceFeedBackBuilder.call(sentence="she no want me to buy the car.")
    resp = ChatGPTCilent.async_call(questions)
    print(resp)


if __name__ == "__main__":
    main()