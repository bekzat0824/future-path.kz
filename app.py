import streamlit as st
from futurepath_ai import FuturePathAI

st.set_page_config(page_title="FuturePath.kz", page_icon="🎓", layout="centered")

st.title("🎓 FuturePath.kz")
st.write("Персональный AI-навигатор по поступлению в вузы")

# Боковая панель для управления
st.sidebar.header("⚙️ Настройки ИИ")
demo_mode = st.sidebar.checkbox("🚀 Включить Демо-режим (для питча)", value=False)
user_api_key = st.sidebar.text_input("Gemini API Key:", type="password", help="Вставь ключ AIzaSy...")

# Поля формы
track = st.selectbox("Целевой трек:", ["KZ", "International"])
grade = st.selectbox("Класс:", ["10 класс", "11 класс", "Выпускник"])
budget = st.text_input("Бюджет на обучение:", "Только грант / До $5000 в год")
interests = st.text_area("Интересы и навыки:", "Физика, IT, разработка игр, математика")
level = st.text_input("Текущий уровень:", "ЕНТ 85 баллов / IELTS 6.0")

# Кнопка генерации
if st.button("🚀 Сгенерировать дорожную карту", type="primary"):
    
    # 1. РЕЖИМ ДЕМО (работает мгновенно без API)
    if demo_mode:
        with st.spinner("ИИ подбирает вузы и строит стратегию..."):
            st.success("Ваша дорожная карта готова (Демо-режим)!")
            st.subheader("💡 Рекомендованное направление")
            st.write("**Software Engineering & AI System Architecture**")
            st.write("Высокие показатели по физике и математике идеально подходят для фундаментального IT-образования.")
            
            st.subheader("🏛️ Топ ВУЗов")
            st.info("**Astana IT University (AITU)** (Казахстан) — Шанс на грант: Высокая\n\nПрофиль 'Software Engineering' идеально совпадает с твоими интересами в разработке.")
            st.info("**КБТУ (KBTU)** (Казахстан) — Шанс на грант: Средняя\n\nСильная математическая школа и международные аккредитации.")
            
            st.subheader("📋 Помесячный план")
            st.write("**Сентябрь — Ноябрь**: Усиленная подготовка к ЕНТ по профильным предметам (Математика + Физика).")
            st.write("**Декабрь — Февраль**: Прохождение пробных тестирований, регистрация на олимпиады AITU/KBTU.")
            st.write("**Март — Май**: Финальная сдача ЕНТ (цель 110+ баллов) и подача документов на грант.")
            
            st.subheader("💰 Финансовый совет")
            st.write("При балле ЕНТ 105+ вероятность получения государственного гранта в AITU составляет более 85%.")

    # 2. РЕЖИМ РЕАЛЬНОГО ИИ
    else:
        if not user_api_key:
            st.error("Вставь Gemini API Key в левой боковой панели (Sidebar) или включи 'Демо-режим'!")
        else:
            with st.spinner("Gemini AI генерирует персональный план..."):
                try:
                    ai = FuturePathAI(api_key=user_api_key.strip())
                    user_profile = {
                        "track": track,
                        "grade": grade,
                        "budget": budget,
                        "interests": interests,
                        "current_level": level
                    }
                    data = ai.generate_roadmap(user_profile)
                    
                    if "error" in data:
                        st.error(f"Ошибка от Gemini API: {data['error']}")
                    else:
                        st.success("Ваша дорожная карта готова!")
                        
                        st.subheader("💡 Рекомендованное направление")
                        st.write(f"**{data['student_summary']['recommended_direction']}**")
                        st.write(data['student_summary']['rationale'])
                        
                        st.subheader("🏛️ Топ ВУЗов")
                        for uni in data.get('top_universities', []):
                            st.info(f"**{uni['name']}** ({uni['country']}) — Шанс на грант: {uni['grant_chance']}\n\n{uni['reason']}")
                            
                        st.subheader("📋 Помесячный план")
                        for step in data.get('roadmap_by_months', []):
                            st.write(f"**{step['period']}**: {step['action']}")

                        if "financial_advice" in data:
                            st.subheader("💰 Финансовый совет")
                            st.write(data["financial_advice"])

                except Exception as e:
                    st.error(f"Произошла ошибка: {str(e)}")