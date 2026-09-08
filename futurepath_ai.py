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
        Создай персонализированную дорожную карту поступления в вуз для абитуриента по имени {user_profile.get('name', 'Абитуриент')}.
        Язык ответа: {lang}. Все описания, названия шагов и советы должны быть строго на языке: {lang}.

        Данные абитуриента:
        - Трек: {user_profile.get('track')}
        - Класс: {user_profile.get('grade')}
        - Профильные предметы: {user_profile.get('subjects')}
        - Финансовое состояние: {user_profile.get('financial_status')}
        - Желаемый балл ЕНТ: {user_profile.get('target_unt')}
        - Желаемый балл IELTS: {user_profile.get('target_ielts')}
        - Желаемый балл SAT: {user_profile.get('target_sat')}
        - Интересы: {user_profile.get('interests')}

        Верни результат строго в формате JSON со следующими ключами:
        - "steps": список объектов с полями "period" (временной интервал) и "action" (действие)
        - "universities": список объектов с полями "name" (название), "city" (город), "description" (описание)
        - "advice": список строк с советами
        """
        try:
            response = self.json_model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}

    def ask_followup(self, user_profile: dict, context_roadmap: dict, question: str, lang: str = "Русский"):
        prompt = f"""
        Ты — AI-консультант FuturePath.kz. Отвечай на языке: {lang}.
        Абитуриент {user_profile.get('name')} задал уточняющий вопрос по своей дорожной карте.

        Контекст профиля: {json.dumps(user_profile, ensure_ascii=False)}
        Сгенерированная карта: {json.dumps(context_roadmap, ensure_ascii=False)}

        Вопрос пользователя: {question}

        Ответь кратко, четко и дружелюбно (не более 3-4 предложений).
        """
        try:
            response = self.chat_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Ошибка при ответе: {str(e)}"
