import json
import google.generativeai as genai

class FuturePathAI:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-3.6-flash",
            generation_config={"response_mime_type": "application/json"}
        )

    def generate_roadmap(self, user_profile: dict):
        prompt = f"""
        Создай персонализированную дорожную карту поступления в вуз для абитуриента в формате JSON.
        Данные абитуриента:
        - Трек: {user_profile.get('track')}
        - Класс: {user_profile.get('grade')}
        - Профильные предметы: {user_profile.get('subjects')}
        - Финансовое состояние / Бюджет: {user_profile.get('financial_status')}
        - Желаемый балл ЕНТ: {user_profile.get('target_unt')}
        - Желаемый балл IELTS: {user_profile.get('target_ielts')}
        - Желаемый балл SAT: {user_profile.get('target_sat')}
        - Интересы: {user_profile.get('interests')}

        Верни результат строго в формате JSON со следующими ключами:
        - "steps": список объектов (словарей), где у каждого объекта есть поля:
          * "period": временной интервал (например, "Сентябрь - Декабрь")
          * "action": описание конкретных действий и задач на этот период
        - "universities": список объектов (словарей), где у каждого объекта есть поля:
          * "name": название вуза
          * "city": город
          * "description": краткое описание/условия поступления
        - "advice": список строк с полезными советами для поступления и получения грантов
        """
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}
