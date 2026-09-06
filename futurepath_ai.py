import json
import google.generativeai as genai

class FuturePathAI:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-3.6-flash",
            generation_config={"response_mime_type": "application/json"}
        )

    def generate_roadmap(self, user_profile: dict) -> dict:
        system_prompt = """
Ты — умный ИИ-ассистент платформы FuturePath.kz, эксперт по профориентации и поступлению для школьников Казахстана.

КОНТЕКСТ И СПЕЦИФИКА КАЗАХСТАНА:
1. ТРЕК "KZ": Учитывай ЕНТ, пороговые баллы, гранты ("Серпін"). Топ вузы: NU, КБТУ, МУИТ, AITU, КазНУ, ЕНУ, SDU.
2. ТРЕК "International": Учитывай IELTS, SAT, GPA, стипендии (Stipendium Hungaricum, Türkiye Bursları, DSU, Financial Aid в США).

Верни результат СТРОГО В ФОРМАТЕ JSON следующей структуры:
{
  "student_summary": {
    "recommended_direction": "Название направления",
    "rationale": "Обоснование выбора"
  },
  "top_universities": [
    {
      "name": "Название университета",
      "country": "Страна",
      "grant_chance": "Высокая / Средняя / Низкая",
      "reason": "Почему подходит"
    }
  ],
  "required_tests": [
    {
      "test_name": "Название теста",
      "target_score": "Целевой балл",
      "deadline": "Срок сдачи"
    }
  ],
  "roadmap_by_months": [
    {"period": "Сентябрь — Ноябрь", "action": "Шаги"},
    {"period": "Декабрь — Февраль", "action": "Шаги"},
    {"period": "Март — Май", "action": "Шаги"}
  ],
  "financial_advice": "Совет по грантам",
  "free_resources": ["Полезные бесплатные ресурсы"]
}
"""
        user_content = f"Профиль абитуриента: {json.dumps(user_profile, ensure_ascii=False)}"
        full_prompt = f"{system_prompt}\n\n{user_content}"

        try:
            response = self.model.generate_content(full_prompt)
            return json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}