from typing import List, TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    isSuccess: bool = True
    message: str = None
    data: T = None

    def __init__(self, message: str = None, data: T = None):
        super().__init__(isSuccess=True, message=message, data=data)


class ScoreResponse(BaseModel):
    score: int = None
    status: str = None

    def __init__(self, score: int = None, status: str = None):
        super().__init__(score=score, status=status)


class QuestionResponse(BaseModel):
    index: int = None
    question: str = None

    def __init__(self, index: int = None, question: str = None):
        super().__init__(index=index, question=question)


class SimpleResultRequest(BaseModel):
    yes_index_list: List[int] = Field(..., min_length=0, max_length=32)

    def __init__(self, yes_index_list: List[int] = None):
        super().__init__(yes_index_list=yes_index_list)


class SGDSResultRequest(BaseModel):
    yes_index_list: List[int] = Field(..., min_length=0, max_length=15)

    def __init__(self, yes_index_list: List[int] = None):
        super().__init__(yes_index_list=yes_index_list)
