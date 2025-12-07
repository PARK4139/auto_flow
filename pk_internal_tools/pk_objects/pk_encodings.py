from enum import Enum



# 제대로 써야하는데. 이래서 명시적이 타입힌팅이 필요하네.
class PkEncoding(Enum):
    CP949 = 'cp949'
    UTF8 = 'utf-8'
    euc_kr = 'euc-kr'

    # def __str__(self):
    #     return self.value # Encoding.CP949.value 해도 되는데, chatGPT 는 __str__()를 override 해서 사용하는 것을 추천
