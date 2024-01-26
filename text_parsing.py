from model import QuestionResponse


def num_str_dict(input_text: tuple):
    """
    Args:
        input_text: "1.( ) 전화번호나 사람이름을 기억하기 힘들다."
    :return:
        {1: "전화번호나 사람이름을 기억하기 힘들다."}
    """
    input_text = input_text.strip()
    input_text = input_text.replace('( ) ', '')
    input_text = input_text.split('.')
    return (input_text[0], input_text[1])


def simple_text_parsing(text: str):
    trim = text.strip()

    trim = trim.split('\n')
    trim = list(map(lambda x: QuestionResponse(num_str_dict(x)[0], num_str_dict(x)[1]), trim))
    return trim


def SGDS_parsing(next_text: str):
    next_text = next_text.strip()
    next_text = next_text.replace(" 예 아니오", "")
    next_text = next_text.split('\n')

    def parse(x):
        x = x.split(".")

        return QuestionResponse(x[0], x[1].strip(), )

    return list(map(lambda x: parse(x), next_text))
