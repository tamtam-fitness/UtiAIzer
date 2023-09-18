from collections.abc import Iterable

import openai

import logging

import os
import sys

print(os.getcwd())
print(os.getenv("BASE_DIR"))
print(sys.path)

from src.common import app_logger, settings
from src.model.models import Answer, Question

openai.api_key = settings.OPENAI_API_KEY


class OpenAISSEClient:
    @classmethod
    def call(cls, question: Question) -> Iterable[Answer]:
        yield from cls(question).__ask_llm_stream()

    def __init__(self, question: Question) -> None:
        self.__question = question

    def __ask_llm_stream(self) -> Iterable[Answer]:
        # LangChainのstreamはコールバック周りが複雑な印象なので一旦openaiをそのまま使う
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            stream=True,  # SSEを使うための設定
            messages=[
                {"role": "system", "content": "answer based on the following question"},
                {"role": "user", "content": f"{self.__question.value}"},
            ],
        )
        app_logger.info(f"user_content: {self.__question.value}")

        for item in response:
            try:
                content = item["choices"][0]["delta"]["content"]
            except Exception:
                content = ""
            # dict型で返すことでよしなに変換してくれる
            yield Answer(value=content)
        yield Answer(value="[END]")
