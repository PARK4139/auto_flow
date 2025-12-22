import re
import unicodedata
import logging

# Configure logging for this module
logger = logging.getLogger(__name__)

class KoreanCleaner:
    def __init__(self):
        """
        Initializes the KoreanCleaner.
        """
        logger.debug("KoreanCleaner initialized.")

    def _normalize_english_text(self, text: str) -> str:
        """
        Normalize English text by expanding common contractions and standardizing.
        This is a placeholder for more advanced NLP.
        """
        text = text.replace("can't", "cannot")
        text = text.replace("won't", "will not")
        text = text.replace("don't", "do not")
        text = text.replace("it's", "it is")
        # Add more rules as needed
        logger.debug(f"Normalized English: '{text}'")
        return text

    def _normalize_numbers(self, text: str) -> str:
        """
        Normalize numbers (e.g., "123,456" to "123456").
        This can be expanded for verbalizing numbers.
        """
        text = re.sub(r"(\d),(\d)", r"\1\2", text)  # Remove commas in numbers
        logger.debug(f"Normalized numbers: '{text}'")
        return text

    def normalize_text(self, text: str) -> str:
        """
        Applies a series of normalization steps to the input text.
        """
        if text is None: # Handle None input gracefully
            logger.debug("normalize_text received None, returning empty string.")
            return ""

        logger.info(f"Normalizing text: '{text}'")
        text = text.lower()  # Convert to lowercase
        # text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")  # This line breaks Korean text.
        text = self._normalize_english_text(text)
        text = self._normalize_numbers(text)
        text = re.sub(r"[^\w\s\.\,\?\!\'\- ]", "", text)  # Remove special characters except basic punctuation and spaces
        text = re.sub(r"\s+", " ", text).strip()  # Replace multiple spaces with a single space and strip
        logger.info(f"Text normalized to: '{text}'")
        return text

    def clean_korean(self, text: str) -> str:
        """
        Specifically cleans Korean text.
        This is a placeholder for more advanced Korean NLP (e.g., Josa processing).
        """
        logger.info(f"Cleaning Korean text: '{text}'")
        # Example: remove common Korean honorifics or particles if not desired for TTS/STT
        # For now, simply apply general normalization
        cleaned_text = self.normalize_text(text)
        logger.info(f"Korean text cleaned to: '{cleaned_text}'")
        return cleaned_text

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    cleaner = KoreanCleaner()
    test_texts = [
        "Can't you see, it's 1,234,567 won?",
        "안녕하세요, 제 이름은 김pk입니다. 2025년 12월 9일입니다!",
        "  This is   a test.   ",
        "Él habla español."
    ]
    for txt in test_texts:
        print(f"Original: '{txt}'")
        print(f"Normalized: '{cleaner.normalize_text(txt)}'")
        print(f"Cleaned Korean: '{cleaner.clean_korean(txt)}'")
        print("-" * 30)
