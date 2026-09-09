import json
import google.generativeai as genai

class FuturePathAI:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.json_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={"response_mime_type": "application/json"}
        )
        self.chat_model = genai.GenerativeModel(model_name="gemini-2.5-flash")

    def generate_roadmap(self, user_profile: dict, lang: str = "Русский"):
        prompt = f"""
        Ты — главная аналитическая система платформы BolashaqZholy.kz. Создай детальную персональную карту поступления для {user_profile.get('name', 'Абитуриент')}.
        Язык ответа: {lang}. Все описания, названия шагов, курсы, отзывы и советы должны быть строго на языке: {lang}.

        Данные абитуриента:
        - Трек: {user_profile.get('track')}
        - Класс: {user_profile.get('grade')}
        - Не определился с профессией: {user_profile.get('undecided')}
        - Склонности/Предпочтения: {user_profile.get('inclination')}
        - Профильные предметы: {user_profile.get('subjects')}
        - Финансовый статус: {user_profile.get('financial_status')}
        - Сельская квота: {user_profile.get('rural_quota')}
        - Гранты от акимата: {user_profile.get('akimat_grant')}
        - Желаемые города: {user_profile.get('preferred_cities')}
        - Желаемые ВУЗы: {user_profile.get('target_unis')}
        - Текущий (пробный) балл ЕНТ: {user_profile.get('current_unt')}
        - Желаемый (целевой) балл ЕНТ: {user_profile.get('target_unt')}
        - Целевой IELTS: {user_profile.get('target_ielts')}, SAT: {user_profile.get('target_sat')}
        - Дополнительные интересы: {user_profile.get('interests')}

        Инструкции:
        1. Проанализируй разницу между текущим баллом ({user_profile.get('current_unt')}) и желаемым баллом ЕНТ ({user_profile.get('target_unt')}). Оцени реальный шанс абитуриента преодолеть этот разрыв и пройти в указанные целевые ВУЗы ({user_profile.get('target_unis')}).
        2. Обязательно учти влияние сельской квоты ({user_profile.get('rural_quota')}) и возможность целевых грантов акимата ({user_profile.get('akimat_grant')}) при расчете шансов и подборе вузов.
        3. Подбери 2-3 рекомендуемых курса/интенсива для закрытия пробелов.
        4. Сформируй каталог реальных инсайтов и отзывов студентов о предложенных вузах и условиях проживания в общежитиях.

        Верни результат СТРОГО в формате JSON со следующей структурой:
        {{
            "grant_chance_percent": 85,
            "grant_status_text": "Высокая вероятность получения гранта",
            "recommended_direction": "Рекомендуемое направление (если не определился)",
            "steps": [
                {{"period": "Сентябрь - Ноябрь", "action": "Описание шага"}}
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
            "university_reviews": [
                {{
                    "name": "Название ВУЗа",
                    "dorm_rating": "4.5/5",
                    "study_rating": "4.8/5",
                    "review_text": "Инсайт или реальный отзыв студента об условиях в общежитии и атмосфере в вузе."
                }}
            ],
            "recommended_courses": [
                {{
                    "title": "Название курса / Интенсива",
                    "provider": "Провайдер или платформа",
                    "reason": "Почему этот курс полезен"
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
        Ты — AI-консультант BolashaqZholy.kz. Отвечай на языке: {lang}.
        Абитуриент {user_profile.get('name')} задал уточняющий вопрос.

        Контекст профиля: {json.dumps(user_profile, ensure_ascii=False)}
        Карта: {json.dumps(context_roadmap, ensure_ascii=False)}
        Вопрос: {question}

        Ответь кратко, четко и дружелюбно (3-4 предложения).
        """
        try:
            response = self.chat_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Ошибка: {str(e)}"
