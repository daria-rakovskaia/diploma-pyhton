from fastapi import HTTPException
from typing import Dict, Any
from groq import Groq

from app.utils.text_postprocessing import postprocess_text

class PostProcessService:
    """
    Сервис для обработки текста с использованием LLM
    """

    def __init__(self, api_key: str):
        """
        Инициализирует сервис для обработки текста

        :param api_key: Ключ API для аутентификации в Groq
        """
        self.api_key = api_key

    def postprocess_text(
            self,
            data: Dict[str, Any],
            model: str = "llama3-70b-8192"
    ):
        """
        Обрабатывает результат распознавания рукописного кода с помощью LLM

        :param data: json, содержащий распознанный код
        :param model: LLM модель (llama3-70b-8192)
        :return: Обработанный текст + путь к работе
        """
        client = Groq(api_key=self.api_key)
        recognized_code, work_url = postprocess_text(data)
        content = "There is handwritten C# code that was put into OCR system. " \
                  "Postprocess it without adding any new lines or words, " \
                  "correct OCR errors to make the names logical and the code real, " \
                  "correct the code formatting according to C#, including braces, " \
                  "do not miss any lines given, include everything, but do NOT add " \
                  "anything extra, that is not written in the code given, " \
                  "do not explain anything: " \
                  f"{recognized_code} " \
                  "In the answer mark with the word /ocr_code_field at/ the beginning and at " \
                  "the end where the code is typed."
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                model=model,
                temperature=0.0
            )
            return chat_completion.choices[0].message.content.split("ocr_code_field")[1], work_url
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI service error: {e}")
