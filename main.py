from typing import List

import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from model import SuccessResponse, ScoreResponse, QuestionResponse, SGDSResultRequest, SimpleResultRequest
from text_parsing import simple_text_parsing, SGDS_parsing

app = FastAPI()

prefix_router = APIRouter(prefix="/api/survey")

simple_text = '''
1.( ) 전화번호나 사람이름을 기억하기 힘들다.
2.( ) 어떤 일이 언제 일어났는지 기억하지 못할 때가 있다.
3.( ) 며칠 전에 들었던 이야기를 잊는다.
4.( ) 오래 전부터 들었던 이야기를 잊는다.
5.( ) 반복되는 일상생활에 변화가 생겼을 때 금방 적응하기가 힘들다.
6.( ) 본인에게 중요한 사항을 잊을 때가 있다.(예를 들어 배우자 생일, 결혼기념일 등)
7.( ) 다른 사람에게 같은 이야기를 반복 힐 때가 있다.
8.( ) 어떤 일을 해놓고도 잊어버려 다시 반복할 때가 있다.
9.( ) 약속을 해놓고 까먹을 때가 있다.
10.( ) 이야기 도중 방금 자기가 무슨 이야기를 하고 있었는지를 잊을 때가 있다.
11.( ) 약 먹는 시간을 놓치기도 한다.
12.( ) 여러 가지 물건을 사러 갔다가 한두 가지를 빠뜨리기도 한다.
13.( ) 가스 불을 끄는 것들 잊어버린 적이 있다. 또는 음식을 태운 적이 있다.
14.( ) 남에게 같은 질문을 반복 한다.
15.( ) 어떤 일을 해놓고도 했는지 안했는지 몰라 다시 확인해야 한다.
16.( ) 물건을 두고 다니거나 또는 가지고 갈 물건을 놓고 간다.
17.( ) 하고 싶은 말이나 표현이 금방 떠오르지 않는다.
18.( ) 물건 이름이 금방 생각나지 않는다.
19.( ) 개인적인 편지나 사무적인 편지를 쓰기 힘들다.
20.( ) 갈수록 말 수가 감소되는 경향이 있다.
21.( ) 신문이나 잡지를 읽을 때 이야기 줄거리를 파악하지 못한다.
22.( ) 책을 읽을 때 같은 문장을 여러 번 읽어야 이해가 된다.
23.( ) 텔레비전에 나오는 이야기를 따라 가기 힘들다.
24.( ) 자주 보는 친구나 친척을 바로 알아보지 못한다.
25.( ) 물건을 어디에 두고 나중에 어디에 두었는지 몰라 찾게 된다.
26.( ) 전에 가본 장소를 기억하지 못한다.
27.( ) 방향 감각이 떨어졌다.
28.( ) 길을 잃거나 헤맨 적이 있다.
29.( ) 물건을 항상 두는 장소를 망각하고 엉뚱한 곳을 찾는다.
30.( ) 계산능력이 떨어졌다.
31.( ) 돈 관리를 하는데 실수가 있다.
32.( ) 과거에 쓰던 기구 사용이 서툴러졌다.
'''

simple_text_question_list: List[QuestionResponse] = simple_text_parsing(simple_text)

sgds_next_text = '''1. 현재의 생활에 대체적으로 만족하십니까 예 아니오
2. 요즈음 들어 활동량이나 의욕이 많이 떨어지셨습니까? 예 아니오
3. 자신이 헛되이 살고 있다고 느끼십니까? 예 아니오
4. 생활이 지루하게 느껴질 때가 많습니까? 예 아니오
5. 평소에 기분은 상쾌한 편이십니까? 예 아니오
6. 자신에게 불길한 일이 닥칠 것 같아 불안하십니까? 예 아니오
7. 대체로 마음이 즐거운 편이십니까? 예 아니오
8. 절망적이라는 느낌이 자주 드십니까? 예 아니오
9. 바깥에 나가기가 싫고 집에만 있고 싶습니까? 예 아니오
10. 비슷한 나이의 다른 노인들보다 기억력이 더 나쁘다고 느끼십니까? 예 아니오
11. 현재 살아 있다는 것이 즐겁게 생각되십니까? 예 아니오
12. 지금의 내 자신이 아무 쓸모 없는 사람이라고 느끼십니까? 예 아니오
13. 기력이 좋은 편이십니까? 예 아니오
14. 지금 자신의 처지가 아무런 희망도 없다고 느끼십니까? 예 아니오
15. 자신이 다른 사람들의 처지보다 더 못하다고 느끼십니까?'''

sgds_question_list: List[QuestionResponse] = SGDS_parsing(sgds_next_text)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@prefix_router.get("/simple", tags=["치매 간이 진단"])
async def 치매_간이_진단() -> SuccessResponse[List[QuestionResponse]]:
    return SuccessResponse(message="OK", data=simple_text_question_list)


@prefix_router.post("/simple/result", tags=["치매 간이 진단"])
async def 치매_간이_진단_결과_받기(request: SimpleResultRequest) -> SuccessResponse[ScoreResponse]:
    yes_index_list = request.yes_index_list

    score = 0
    for index in yes_index_list:
        score += 1

    if score >= 17:
        result = "비정상"
    else:
        result = "정상"

    return SuccessResponse(
        message="OK",
        data=ScoreResponse(
            score=score,
            status=result
        )
    )


@prefix_router.get("/SGDS", tags=["단축형 노인 우울 척도"])
async def 단축형_노인_우울_척도() -> SuccessResponse[List[QuestionResponse]]:
    return SuccessResponse(message="OK", data=sgds_question_list)


@prefix_router.post("/SGDS/result", tags=["단축형 노인 우울 척도"])
async def 단축형_노인_우울_척도_결과_받기(request: SGDSResultRequest) -> SuccessResponse[ScoreResponse]:
    yes_index_list = request.yes_index_list

    score = 0
    yes_score_list = [2, 3, 4, 6, 8, 9, 10, 12, 14, 15]
    no_score_list = [1, 5, 7, 11, 13]
    # yes_score_list 에 있는 index 는 yes_index_list 에 있으면 score += 1
    # no_score_list 에 있는 index 는 yes_index_list 에 없으면 score += 1
    for index in yes_index_list:
        # index 가 yes_score_list 에 있으면 score += 1
        if index in yes_score_list:
            score += 1

    for index in no_score_list:
        # index 가 no_score_list 에 있으면 score += 1
        if index not in yes_index_list:
            score += 1

    # - 5점이하는 정상
    # - 6~9 중증도 우울
    # - 10점이상은 우울증
    if score <= 5:
        result = "정상"
    elif 6 <= score <= 9:
        result = "중증도 우울"
    else:
        result = "우울증"

    return SuccessResponse(
        message="OK",
        data=ScoreResponse(
            score=score,
            status=result
        )
    )

app.include_router(prefix_router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
