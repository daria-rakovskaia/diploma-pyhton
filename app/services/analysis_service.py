from fastapi import HTTPException
from groq import Groq

class AnalysisService:
    """
    Сервис для интеллектуального анализа кода с использованием LLM
    """

    def __init__(self, api_key: str):
        """
        Инициализирует сервис для интеллектуального анализа кода

        :param api_key: Ключ API для аутентификации в Groq
        """
        self.api_key = api_key

    def analyze_code(
            self,
            task: str,
            code: str,
            model: str = "llama3-70b-8192"
    ):
        """
        Обрабатывает результат интеллектуального анализа кода с помощью LLM

        :param task: Текст задачи
        :param code: Код, подлежащий анализу
        :param model: LLM модель (llama3-70b-8192)
        :return: Результат анализа
        """
        client = Groq(api_key=self.api_key)
        content = "You are an expert code reviewer and software engineer that thinks and never makes mistakes. " \
                  "Below is a programming task description, followed by a code implementation. " \
                  "Analyze the code and determine whether it correctly and completely fulfills the task requirements. " \
                  "Be thorough and precise without suggesting any code: " \
                  "Check for correctness: Does the logic meet the exact requirements of the task? " \
                  "Check for completeness: Does it handle all specified cases, inputs, and edge conditions? " \
                  "Check for efficiency and readability. " \
                  "Highlight any bugs, flaws, or missing parts. " \
                  "Do NOT just summarize the code — analyze it against the task. " \
                  "The answer must be in Russian language. " \
                  "TASK DESCRIPTION: " \
                  f"{task} " \
                  "CODE: " \
                  f"{code}"
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
            return chat_completion.choices[0].message.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI service error: {e}")
