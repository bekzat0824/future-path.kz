import streamlit as st
from futurepath_ai import FuturePathAI

st.set_page_config(page_title="FuturePath.kz", page_icon="🎓", layout="centered")

st.title("🎓 FuturePath.kz")
st.write("Персональный AI-навигатор по поступлению в вузы")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
elif "gemini_api_key" in st.secrets:
    api_key = st.secrets["gemini_api_key"]
else:
    api_key = None

st.sidebar.header("⚙️ Настройки")

if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

if "track" not in st.session_state:
    st.session_state.track = "KZ (ЕНТ / Гранты)"
if "grade" not in st.session_state:
    st.session_state.grade = "10 класс"
if "subject_comb" not in st.session_state:
    st.session_state.subject_comb = "Математика + Физика"
if "subjects_custom_input" not in st.session_state:
    st.session_state.subjects_custom_input = ""
if "financial_status" not in st.session_state:
    st.session_state.financial_status = ""
if "target_unt" not in st.session_state:
    st.session_state.target_unt = 110
if "target_ielts" not in st.session_state:
    st.session_state.target_ielts = 0.0
if "target_sat" not in st.session_state:
    st.session_state.target_sat = 0
if "interests" not in st.session_state:
    st.session_state.interests = ""

def toggle_demo():
    if st.session_state.demo_mode:
        st.session_state.track = "KZ (ЕНТ / Гранты)"
        st.session_state.grade = "11 класс / Колледж"
        st.session_state.subject_comb = "Математика + Физика"
        st.session_state.subjects_custom_input = ""
        st.session_state.financial_status = "Среднее, рассчитываем на государственный грант или скидку"
        st.session_state.target_unt = 120
        st.session_state.target_ielts = 6.0
        st.session_state.target_sat = 1200
        st.session_state.interests = "IT, инженерия, программирование"
    else:
        st.session_state.track = "KZ (ЕНТ / Гранты)"
        st.session_state.grade = "10 класс"
        st.session_state.subject_comb = "Математика + Физика"
        st.session_state.subjects_custom_input = ""
        st.session_state.financial_status = ""
        st.session_state.target_unt = 110
        st.session_state.target_ielts = 0.0
        st.session_state.target_sat = 0
        st.session_state.interests = ""

demo_mode = st.sidebar.checkbox(
    "🚀 Включить Демо-режим (для питча)", 
    key="demo_mode", 
    on_change=toggle_demo
)

with st.form("student_form"):
    st.subheader("Анкета абитуриента")
    
    track = st.selectbox(
        "Выберите основной трек:", 
        ["KZ (ЕНТ / Гранты)", "International (Зарубежные вузы)"],
        key="track"
    )
    grade = st.selectbox(
        "Класс:", 
        ["10 класс", "11 класс / Колледж"],
        key="grade"
    )
    
    subject_comb = st.selectbox(
        "Профильные предметы ЕНТ", 
        [
            "Математика + Физика",
            "Математика + Информатика",
            "Математика + География",
            "Биология + Химия",
            "Биология + География",
            "История + Иностранный язык",
            "История + Основы права (ЧОП)",
            "География + Иностранный язык",
            "Химия + Физика",
            "Язык и литература",
            "Творческий экзамен",
            "Другое / Пользовательский вариант"
        ],
        key="subject_comb"
    )
    
    if subject_comb == "Другое / Пользовательский вариант":
        subjects = st.text_input(
            "Введите свои профильные предметы вручную:",
            key="subjects_custom_input"
        )
    else:
        subjects = subject_comb

    financial_status = st.text_input(
        "Финансовое состояние / Бюджет на обучение (например: только грант, средний доход)",
        key="financial_status"
    )
    
    st.markdown("---")
    st.subheader("🎯 Целевые баллы экзаменов")
    
    target_unt = st.slider(
        "Желаемый балл ЕНТ", 
        50, 140, 
        key="target_unt"
    )
    target_ielts = st.number_input(
        "Желаемый балл IELTS (если нужен, 0 — если не сдаете)", 
        min_value=0.0, max_value=9.0, step=0.5,
        key="target_ielts"
    )
    target_sat = st.number_input(
        "Желаемый балл SAT (если нужен, 0 — если не сдаете)", 
        min_value=0, max_value=1600, step=10,
        key="target_sat"
    )
    
    st.markdown("---")
    interests = st.text_area(
        "Интересы и будущая профессия (например: IT, инженерия, медицина)",
        key="interests"
    )
    
    submitted = st.form_submit_button("🚀 Сгенерировать дорожную карту")

if submitted:
    if st.session_state.demo_mode:
        st.info("📌 Работает Демо-режим (статический ответ для презентации).")
        st.success("🎉 Ваша дорожная карта готова (Демо)!")
        st.markdown("""
        ### 🎓 Персональный план поступления: ФизМат (FuturePath.kz)
        * **Профиль:** 11 класс | Математика + Физика 
        * **Целевые баллы:** ЕНТ: 120 | IELTS: 6.0 | SAT: 1200
        * **Финансовый статус:** Расчет на государственный грант
        
        #### 📌 Шаги подготовки
        * **Сентябрь - Декабрь** — Углубленное изучение разделов математического анализа и механики в физике.
        * **Январь - Февраль** — Регулярная сдача пробных тестов ЕНТ для отслеживания прогресса (цель — стабильно 120+).
        * **Март - Июнь** — Подготовка к сертификату IELTS до уровня B2 (6.0) для расширения возможностей.

        #### 🎓 Рекомендуемые вузы
        * **КБТУ (Казахско-Британский технический университет)** (Алматы) — лучший выбор для IT и программной инженерии.
        * **СДУ (Suleyman Demirel University)** (Каскелен) — сильная школа математики и программирования.
        * **Satbayev University** (Алматы) — отличные инженерные гранты.

        #### 💡 Полезные советы
        * Участвуйте в хакатоне **SPARK Startup Battle** для усиления портфолио и получения грантовых преимуществ.
        * Следите за сроками подачи документов на государственные гранты в июле.
        """)
    elif not api_key:
        st.error("⚠️ Ошибка конфигурации: API-ключ не найден в настройках Streamlit Secrets.")
    else:
        with st.spinner("🤖 ИИ анализирует данные и строит индивидуальный трек..."):
            ai = FuturePathAI(api_key=api_key)
            user_profile = {
                "track": track,
                "grade": grade,
                "subjects": subjects,
                "financial_status": financial_status,
                "target_unt": target_unt,
                "target_ielts": target_ielts,
                "target_sat": target_sat,
                "interests": interests
            }
            result = ai.generate_roadmap(user_profile)
            
            if "error" in result:
                st.error(f"Ошибка от Gemini API: {result['error']}")
            else:
                st.success("🎉 Ваша дорожная карта готова!")
                
                if "steps" in result and result["steps"]:
                    st.subheader("📌 Шаги подготовки")
                    for step in result["steps"]:
                        if isinstance(step, dict):
                            period = step.get("period", "")
                            action = step.get("action", "")
                            period_str = f"**{period}** — " if period else ""
                            st.markdown(f"* {period_str}{action}")
                        else:
                            st.markdown(f"* {step}")
                
                if "universities" in result and result["universities"]:
                    st.subheader("🎓 Рекомендуемые вузы")
                    for uni in result["universities"]:
                        if isinstance(uni, dict):
                            name = uni.get("name", "Вуз")
                            city = uni.get("city", "")
                            desc = uni.get("description", "")
                            city_str = f" ({city})" if city else ""
                            st.markdown(f"* **{name}**{city_str} — {desc}")
                        else:
                            st.markdown(f"* {uni}")
                
                if "advice" in result and result["advice"]:
                    st.subheader("💡 Полезные советы")
                    for adv in result["advice"]:
                        st.markdown(f"* {adv}")
