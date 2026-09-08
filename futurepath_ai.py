import json
import google.generativeai as genai

class FuturePathAI:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.json_model = genai.GenerativeModel(
            model_name="gemini-3.6-flash",
            generation_config={"response_mime_type": "application/json"}
        )
        self.chat_model = genai.GenerativeModel(model_name="gemini-3.6-flash")

    def generate_roadmap(self, user_profile: dict, lang: str = "Русский"):
        prompt = f"""
        Ты — главная аналитическая система FuturePath.kz. Создай детальный план поступления для {user_profile.get('name', 'Абитуриент')}.
        Язык ответа: {lang}.

        Данные абитуриента:
        - Трек: {user_profile.get('track')}
        - Класс: {user_profile.get('grade')}
        - Не определился с профессией: {user_profile.get('undecided')}
        - Предпочтения/Склонности: {user_profile.get('inclination')}
        - Профильные предметы: {user_profile.get('subjects')}
        - Финансовый статус: {user_profile.get('financial_status')}
        - Баллы ЕНТ (цель): {user_profile.get('target_unt')}
        - IELTS: {user_profile.get('target_ielts')}, SAT: {user_profile.get('target_sat')}
        - Интересы: {user_profile.get('interests')}

        Верни результат СТРОГО в формате JSON со следующей структурой:
        {{
            "grant_chance_percent": 80,
            "grant_status_text": "Высокий шанс на грант",
            "recommended_direction": "Рекомендуемое направление (если не определился)",
            "steps": [
                {{"period": "Сентябрь - Октябрь 2026", "action": "Описание шага"}}
            ],
            "universities": [
                {{
                    "name": "Название ВУЗа",
                    "city": "Город",
                    "grant_cutoff": "Проходной балл (например: 110+)",
                    "tuition": "Стоимость (платное)",
                    "dorm": "Есть/Нет",
                    "grant_chance": "Высокий/Средний/Низкий",
                    "description": "Краткое описание"
                }}
            ],
            "advice": ["Совет 1", "Совет 2"]
        }}
        """
        try:
            response = self.json_model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}

    def ask_followup(self, user_profile: dict, context_roadmap: dict, question: str, lang: str = "Русский"):
        prompt = f"""
        Ты — AI-консультант FuturePath.kz. Отвечай на языке: {lang}.
        Абитуриент {user_profile.get('name')} задал уточняющий вопрос.

        Контекст профиля: {json.dumps(user_profile, ensure_ascii=False)}
        Карта: {json.dumps(context_roadmap, ensure_ascii=False)}
        Вопрос: {question}

        Ответь кратко и полезно (3-4 предложения).
        """
        try:
            response = self.chat_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Ошибка: {str(e)}"
