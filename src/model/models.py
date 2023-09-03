from pydantic import BaseModel, Field, validator


class EnglishWord(BaseModel):
    value: str = Field(max_length=20)

    @validator("value")
    def is_english(cls, v):
        try:
            v.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError("English only")
        return v


class Question(BaseModel):
    value: str


class Answer(BaseModel):
    value: str
