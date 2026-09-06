import json
import google.generativeai as genai

class FuturePathAI:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
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

        Верни результат строго в формате JSON со следующими ключами и списками внутри:
        - "steps": список ключевых шагов подготовки
        - "universities": список рекомендуемых вузов с учетом бюджета и баллов (например, КБТУ, СДУ и др.)
        - "advice": полезные советы для поступления и получения грантов
        """
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}
