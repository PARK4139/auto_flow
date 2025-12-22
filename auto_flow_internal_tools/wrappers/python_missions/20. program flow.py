import logging

from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
from pk_internal_tools.pk_functions.get_text_cyan import get_text_cyan
from pk_internal_tools.pk_functions.get_text_white import get_text_white
from pk_internal_tools.pk_objects.pk_system_not_organized import PK_UNDERLINE_SHORT, PK_UNDERLINE_HALF

step = 1     # 이거는 어디에 넣어둘까?
total_step = 100

def _speak(msg):
    print(rf"[{step}/{total_step}]")
    ensure_spoken(msg)

def _guide_to_press_enter():
    keep_going_guide_msg = f"계속 진행하려면 엔터를 눌러주세요"
    _speak(keep_going_guide_msg)

def _divide_contents(text):
    _line_spliter = "================="
    print(f"{_line_spliter} {text} {_line_spliter} ")


def _print(text):
    print(text)

_guide_to_press_enter()


# pk_* -> 비대칭 컬러풀 로깅스타일 : 스타일리쉬한 느낌
_print(rf"{get_text_cyan("강사 소개 및 인사" )} ({get_text_white("")})")
_speak(f"안녕하세요 7년차 개발자 박정훈입니다.")
_speak(f"프로그래밍 독학을 시작했던 저는 프로그래밍은 학습은 어렵고 길다고만 생각했습니다.")
_speak(f"chatGPT가 나오기 전까지는요!")
_speak(f"AI에게 질의와 피드백을 동반한 학습방식은, 이제 수준높은 교수님을 앞에 두고 수업을 듣는 것과 동일하다고 생각합니다.")
# _speak(f"제 전산 업무 자동화 기초 수업에 오신걸 환영해요.")
_speak(f"제 컴퓨터 업무 자동화 기초 수업에 오신걸 환영해요.")
_speak(f"제 목표는 chatGPT 에게 물어보는고 방법을 얻고 피드백을 내 컴퓨터 업무에 적용하고")
# _speak(f"거두절미하고, 일반인들을 위한 강의를 바로 시작합니다.")
# _speak(f"일반인들을 위한 강의를 바로 시작합니다.")
_speak(f"일반인들을 위한 강의를 시작하겠습니다.")
_print(rf"{get_text_cyan("강의 특징" )} ({get_text_white("")})")
# _speak(f"게임같은 강의")
_speak(f"cli 기반 수업진행")
_speak(f"수업 자동화")
_speak(f"ㅎㅎ")
_speak(f"하하")
_print(rf"{get_text_cyan("강의 설명" )} ({get_text_white("")})")
_speak(f"이 수업은 기초 프로그래밍 수업입니다.")
# _speak(f"수업컨셉은 탑다운 방식으로 귀납적인으로 이해를 돕는 것입니다. ")
_speak(f"수업은 강의 단위로 진행이 되며")
_speak(f"하나의 강의는 예제/해석/미션/제안 순으로 구성이 되어 진행이 됩니다.")
_print(rf"{get_text_cyan("강의에서 얻을 수 있는것" )} ({get_text_white("")})")
_speak(f"`cli 인터페이스`의 이해")
_speak(f"`업무자동화`의 이해")
_speak(f"`프로그래밍의 기본흐름`의 이해")
_speak(f"`파이썬 기본 문법`의 이해")
_print(rf"{get_text_cyan("업무_자동화_강의_1강" )} : ({get_text_white("일에 대한 기본 흐름 이해 -> 프로그램의 기본 흐름 이해")})")
# 예제 : 1에서3까지_출력하기.py
# print(1)
# print(2)
# print(3)
#
# 해석 :
# 위의 프로그램은 `1에서3까지_출력하기` 하는 목표를 가진 제 예제 *프로그램 이었습니다.
# *프로그램 : .py .bin .exe .excel 확장자로 끝나는 것들
#
#
# 미션 : 1에서10까지_출력하기.py 프로그램을 만들어 보세요.
#
# 제안(미션해결방법제안) :
# print : 파이썬 언어에서 print 는 파이썬 인터프리터를 통해 파이썬환경 콘솔에 문자 또는 숫자를 출력하기 위한 도구(함수)





# 프로그램 흐름 : 순차진행을 한다
_guide_to_press_enter()


_speak(f"흐름제어")  # 주석

'''
    이곳이 어떤것을 작성하여도 프로그램에 영향을 주지않아요.
'''

_speak(f"프로그램을 만드는 도구")  # IDE 기본사용.   inspection 기능으로 학습효율 극대화
_guide_to_press_enter()

_speak(f"흐름끊기")  # 주석
_guide_to_press_enter()

_speak(f"직선흐름")  # print  psutil
_guide_to_press_enter()

_speak(f"둥근흐름")  # for / while # loop 문
_guide_to_press_enter()

_speak(f"흐름들")
_guide_to_press_enter()




_speak(f"프로그램 흐름 예측해보기")
_guide_to_press_enter()

_speak(f"프로그램 의도 파악하여 복붙해보기")
_guide_to_press_enter()

_speak(f"프로그램 흐름 복붙하여 실험해보기")
_guide_to_press_enter()

_speak("프로그램 만들기")  # 학습자의 컴퓨터 자동화 튜토리얼 만르기
_guide_to_press_enter()


# TODO :  ver_cpp  ver_arduino 도 필요
# 프로그램 흐름 만들기
# for idx, _ in enumerate([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]):
#     print()

# minutes = ensure_value_completed_2025_10_12_0000(key_hint='minutes=', values=[1, 3, 5])



# 실습미션 : 콘솔에 1에서 10000 까지 정수를 수직방향으로 출력

# 실습미션 : 콘솔에 1에서 10000 까지 정수를 수평방향으로 출력



# 꿀팁 튜토리얼 : 메모
# 당신은 메모를 어떻게 하시나요?
# 의사 코드(pseudo code) 를 아시나요?
# 의사 코드(pseudo code) 의 이해
# 저는 메모를 `의사 코드`로 작성을 합니다.



# 꿀팁 튜토리얼 : 핫리로더
# `핫리로더 모드` 사용법
# 기대효과 : `핫리로더 모드` 사용 -> 편리한 개발


# `핫리로더 모드` 사용 주의사항.
# 시스템 파일을 건들거나 로직을 넣을 때는 매우 신중해야합니다.
# 개발자의 의사결정 로직을 넣어 사용하는 것도 방법입니다.
# 영향이 있을만한 코드를 돌릴때는 장치와 데이터의 손실을 유할발 수 있읍니다.




# ## 절차지향 기반으로 프로그램 flow 만들기
#
# ## OOP 기반으로 프로그램 flow 만들기
#
# ## 객체 정보 출력 커스텀
# -> object 객체의 내부의 정보들 궁금함 -> object 객체의 특별함수, object.__str__ 와 object.__repr__ 의 활용 -> object 객체의 내부의 정보들 출력
#
# # 사전학습내용
# # object.__str__
# 사용자용
#
# # object.__repr__
# 개발자용
# 공식 문서 표현: “unambiguous representation”
#
# __repr__ →  str 반환 # __repr__ return type은 반드시 str
# __str__ →  str 반환
#
# custom_object.__str__   # object.__str__  를 custom_object.__str__ 로 오버라이딩
# custom_object.__repr__  # object.__repr__ 를 custom_object.__repr__ 로 오버라이딩
#
# # 커스텀 호출
# print(custom_object)  # custom_object.__str__()가 없으면 → custom_object.__repr__() 호출
# print(custom_object.__repr__())
#
#
#
#
#
#
# ## 객체 기능 커스텀
# -> custom_object 의 기능을 커스텀하고 싶음 -> 부모가 없음. -> `함수 재정의`
# -> custom_object 의 기능을 커스텀하고 싶음 -> 부모가 없음. -> `오버로딩`
# -> custom_object 의 기능을 커스텀하고 싶음 -> 부모가 있음. -> `오버라이딩`
# # 사전학습내용
# # def 판별_오버로딩_or_오버라이딩()
#     '''
#     n. 언어별로 `오버로딩 지원 유무`가 다르다.
#     C++ / Java / C# -> `오버로딩 지원`
#     Python / JavaScript -> `오버로딩 미지원`
#     파이썬은 시그니처가 다른경우, `후자의 함수로 재정의` 되어, 전자의 함수를 사용할 수 없다. 이는 오버로딩 이라고 부르지 않는다.
#     오버로딩은 시그니처가 다른경우 별개의 함수 공존하는데,
#
#     n. `오버라이딩`은 좀더 제약적이다
#     '''
#     if not 두 함수명 동일
#         return False
#     if 상속관계의 두 클래스에서 함수 재정의
#         if 매개변수, 반환 타입이 모두 같음:
#             return '오버라이딩'
#     return '오버로딩'