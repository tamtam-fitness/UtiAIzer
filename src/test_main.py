from service import WordQuestionBuilder, OpenAISSEClient
from model.models import EnglishWord

question = WordQuestionBuilder.call(key="collocation", word=EnglishWord(value="fart"))
answers = OpenAISSEClient.call(question)
result_str = ""
for answer in answers:
    result_str += answer.value

breakpoint()