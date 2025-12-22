import logging
import re


class AnsiStrippingFormatter(logging.Formatter):
    """로그 메시지에서 ANSI 이스케이프 코드를 제거하는 포맷터"""

    # ANSI 이스케이프 코드를 제거하기 위한 정규식
    ANSI_ESCAPE_PATTERN = re.compile(r'\x1b\[[0-9;]*m')

    def format(self, record):
        # 먼저 기본 포맷터로 메시지를 포맷합니다.
        # 이렇게 하면 %(message)s 부분이 처리됩니다.
        formatted_message = super().format(record)

        # 포맷된 메시지에서 ANSI 이스케이프 코드와 NUL 바이트를 제거합니다.
        cleaned_message = self.ANSI_ESCAPE_PATTERN.sub('', formatted_message)
        return cleaned_message.replace('\x00', '')