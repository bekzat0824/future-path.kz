import streamlit as st
from futurepath_ai import FuturePathAI

st.set_page_config(page_title="FuturePath.kz", page_icon="🎓", layout="centered")

# --- Получение API ключа ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
elif "gemini_api_key" in st.secrets:
    api_key = st.secrets["gemini_api_key"]
else:
    api_key = None

# --- Настройки сессии ---
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "roadmap_result" not in st.session_state:
    st.session_state.roadmap_result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Боковая панель: Язык и Режим ---
st.sidebar.header("⚙️ Настройки / Settings")
lang = st.sidebar.selectbox("🌐 Язык / Тіл / Language", ["Русский", "Қазақша", "English"])

def toggle_demo():
    if st.session_state.demo_mode:
        st.session_state.user_name = "Айсултан"
        st.session_state.track = "KZ (ЕНТ / Гранты)"
        st.session_state.grade = "11 класс / Колледж"
        st.session_state.subject_comb = "Математика + Физика"
        st.session_state.financial_status = "Рассчитываем на грант"
        st.session_state.target_unt = 120
        st.session_state.target_ielts = 6.0
        st.session_state.target_sat = 1200
        st.session_state.interests = "IT, разработка ПО"

st.sidebar.checkbox("🚀 Демо-режим (для питча)", key="demo_mode", on_change=toggle_demo)

# Словари для мультиязычности UI
ui_texts = {
    "Русский": {
        "title": "🎓 FuturePath.kz",
        "subtitle": "Персональный AI-навигатор по поступлению в вузы",
        "welcome_hdr": "Привет! Давайте познакомимся 👋",
        "welcome_desc": "Я помогу тебе построить пошаговый план подготовки, выбрать профильные предметы и подобрать подходящие университеты.",
        "name_label": "Как тебя зовут?",
        "next_btn": "Начать 🚀",
        "form_hdr": "Анкета абитуриента",
        "gen_btn": "🚀 Сгенерировать дорожную карту",
        "restart_btn": "🔄 Заполнить заново",
        "chat_hdr": "💬 Задать уточняющий вопрос ИИ",
        "chat_ph": "Например: Каковы шансы получить грант с 110 баллами?"
    },
    "Қазақша": {
        "title": "🎓 FuturePath.kz",
        "subtitle": "Оқуға түсуге арналған жеке AI-навигатор",
        "welcome_hdr": "Сәлем! Танысып өтейік 👋",
        "welcome_desc": "Мен саған дайындық жоспарын құруға, пәндерді таңдауға және ЖОО табуға көмектесемін.",
        "name_label": "Есімің кім?",
        "next_btn": "Бастау 🚀",
        "form_hdr": "Талапкер анкетасы",
        "gen_btn": "🚀 Жол картасын жасау",
        "restart_btn": "🔄 Қайта толтыру",
        "chat_hdr": "💬 AI-ға қосымша сұрақ қою",
        "chat_ph": "Мысалы: 110 баллмен грант алу мүмкіндігі қандай?"
    },
    "English": {
        "title": "🎓 FuturePath.kz",
        "subtitle": "Personal AI Navigator for University Admissions",
        "welcome_hdr": "Hello! Let's get to know you 👋",
        "welcome_desc": "I will help you build a step-by-step preparation plan, select subjects, and find the right universities.",
        "name_label": "What is your name?",
        "next_btn": "Start 🚀",
        "form_hdr": "Applicant Form",
        "gen_btn": "🚀 Generate Roadmap",
        "restart_btn": "🔄 Start Over",
        "chat_hdr": "💬 Ask AI a Follow-up Question",
        "chat_ph": "Example: What are the chances for a scholarship with 110 points?"
    }
}

t = ui_texts[lang]

st.title(t["title"])
st.caption(t["subtitle"])
st.markdown("---")

# ==========================================
# ОКНО 1: Приветствие и знакомство
# ==========================================
if st.session_state.page == "welcome":
    st.subheader(t["welcome_hdr"])
    st.write(t["welcome_desc"])
    
    name_input = st.text_input(t["name_label"], value=st.session_state.user_name)
    
    if st.button(t["next_btn"]):
        if name_input.strip():
            st.session_state.user_name = name_input.strip()
            st.session_state.page = "form"
            st.rerun()
        else:
            st.warning("Пожалуйста, введите имя!")

# ==========================================
# ОКНО 2: Заполнение анкеты
# ==========================================
elif st.session_state.page == "form":
    st.subheader(f"{t['form_hdr']} ({st.session_state.user_name})")
    
    with st.form("student_form"):
        track = st.selectbox("Трек:", ["KZ (ЕНТ / Гранты)", "International (Зарубежные вузы)"], key="track")
        grade = st.selectbox("Класс / Статус:", ["10 класс", "11 класс / Колледж"], key="grade")
        
        subject_comb = st.selectbox(
            "Профильные предметы ЕНТ:", 
            [
                "Математика + Физика", "Математика + Информатика", "Математика + География",
                "Биология + Химия", "Биология + География", "История + Иностранный язык",
                "История + Основы права (ЧОП)", "География + Иностранный язык", "Химия + Физика",
                "Язык и литература", "Творческий экзамен", "Другое / Пользовательский вариант"
            ],
            key="subject_comb"
        )
        
        subjects = st.text_input("Ваш вариант предметов:", key="subjects_custom") if subject_comb == "Другое / Пользовательский вариант" else subject_comb
        financial_status = st.text_input("Бюджет / Финансовые цели:", key="financial_status")
        
        target_unt = st.slider("Желаемый балл ЕНТ:", 50, 140, key="target_unt")
        target_ielts = st.number_input("Целевой IELTS (0 если не сдаете):", 0.0, 9.0, step=0.5, key="target_ielts")
        target_sat = st.number_input("Целевой SAT (0 если не сдаете):", 0, 1600, step=10, key="target_sat")
        interests = st.text_area("Интересы и специальности:", key="interests")
        
        submitted = st.form_submit_button(t["gen_btn"])
        
    if submitted:
        st.session_state.user_profile = {
            "name": st.session_state.user_name,
            "track": track,
            "grade": grade,
            "subjects": subjects,
            "financial_status": financial_status,
            "target_unt": target_unt,
            "target_ielts": target_ielts,
            "target_sat": target_sat,
            "interests": interests
        }
        st.session_state.page = "roadmap"
        st.rerun()

# ==========================================
# ОКНО 3: Дорожная карта + Чат с ИИ
# ==========================================
elif st.session_state.page == "roadmap":
    col1, col2 = st.columns([3, 1])
    col1.subheader(f"🎓 Карта для: {st.session_state.user_name}")
    if col2.button(t["restart_btn"]):
        st.session_state.page = "welcome"
        st.session_state.chat_history = []
        st.session_state.roadmap_result = None
        st.rerun()

    # Генерация или загрузка из состояния
    if st.session_state.roadmap_result is None:
        if st.session_state.demo_mode:
            st.session_state.roadmap_result = {
                "steps": [
                    {"period": "Сентябрь - Декабрь", "action": "Подготовка по Математике и Физике, закрытие слабых тем."},
                    {"period": "Январь - Март", "action": "Сдача январского ЕНТ, интенсивный прореш тестов НЦТ."}
                ],
                "universities": [
                    {"name": "КБТУ", "city": "Алматы", "description": "Топовый технический вуз, сильный IT-факультет."},
                    {"name": "Satbayev University", "city": "Алматы", "description": "Большое количество государственных грантов."}
                ],
                "advice": ["Следите за сроками подачи документов на грант в июле.", "Участвуйте в олимпиадах для получения скидок."]
            }
        elif api_key:
            with st.spinner("🤖 ИИ генерирует персональный план..."):
                ai = FuturePathAI(api_key=api_key)
                st.session_state.roadmap_result = ai.generate_roadmap(st.session_state.user_profile, lang=lang)

    res = st.session_state.roadmap_result

    if res and "error" not in res:
        # Шаги
        if "steps" in res:
            st.subheader("📌 Шаги подготовки")
            for step in res["steps"]:
                if isinstance(step, dict):
                    st.markdown(f"* **{step.get('period', '')}** — {step.get('action', '')}")
                else:
                    st.markdown(f"* {step}")
        
        # Вузы
        if "universities" in res:
            st.subheader("🎓 Рекомендуемые вузы")
            for uni in res["universities"]:
                if isinstance(uni, dict):
                    city = f" ({uni.get('city')})" if uni.get("city") else ""
                    st.markdown(f"* **{uni.get('name')}**{city} — {uni.get('description')}")
                else:
                    st.markdown(f"* {uni}")

        # Советы
        if "advice" in res:
            st.subheader("💡 Полезные советы")
            for adv in res["advice"]:
                st.markdown(f"* {adv}")

        st.markdown("---")
        # --- Блок мини-чата с ИИ ---
        st.subheader(t["chat_hdr"])
        
        # Отображение истории вопросов
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        user_question = st.chat_input(t["chat_ph"])
        if user_question:
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.write(user_question)
                
            with st.chat_message("assistant"):
                with st.spinner("..."):
                    if st.session_state.demo_mode:
                        answer = f"В демо-режиме: Уважаемый(ая) {st.session_state.user_name}, с баллами {st.session_state.user_profile.get('target_unt')} у вас высокие шансы на получение гранта в выбранных вузах!"
                    elif api_key:
                        ai = FuturePathAI(api_key=api_key)
                        answer = ai.ask_followup(st.session_state.user_profile, res, user_question, lang=lang)
                    else:
                        answer = "Ошибка API ключа."
                    st.write(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    else:
        st.error("Ошибка получения данных от ИИ. Проверьте настройки ключа.")
