from pydantic import BaseModel, Field, validator


class NotEnglishError(ValueError):
    pass


class EnglishWord(BaseModel):
    value: str = Field(max_length=30)

    @validator("value")
    def is_english(cls, v: str) -> str:
        try:
            v.encode("ascii")
        except UnicodeEncodeError:
            raise NotEnglishError("English only") from None
        return v


class Question(BaseModel):
    value: str


class Answer(BaseModel):
    value: str
