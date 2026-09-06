import streamlit as st
from futurepath_ai import FuturePathAI

st.set_page_config(page_title="FuturePath.kz", page_icon="🎓", layout="centered")

st.title("🎓 FuturePath.kz")
st.write("Персональный AI-навигатор по поступлению в вузы")

# Безопасное получение ключа из секретов Streamlit Cloud с поддержкой разного регистра
cloud_api_key = ""
if "GEMINI_API_KEY" in st.secrets:
    cloud_api_key = st.secrets["GEMINI_API_KEY"]
elif "gemini_api_key" in st.secrets:
    cloud_api_key = st.secrets["gemini_api_key"]

st.sidebar.header("⚙️ Настройки ИИ")

# Инициализация состояния сессии для демо-режима
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

# Инициализация полей формы в session_state
if "track" not in st.session_state:
    st.session_state.track = "KZ (ЕНТ / Гранты)"
if "grade" not in st.session_state:
    st.session_state.grade = "10 класс"
if "subjects" not in st.session_state:
    st.session_state.subjects = ""
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

# Функция автозаполнения или очистки полей при переключении галочки
def toggle_demo():
    if st.session_state.demo_mode:
        # Автозаполнение для презентации (ФизМат, 11 класс)
        st.session_state.track = "KZ (ЕНТ / Гранты)"
        st.session_state.grade = "11 класс / Колледж"
        st.session_state.subjects = "Математика + Физика"
        st.session_state.financial_status = "Среднее, рассчитываем на государственный грант или скидку"
        st.session_state.target_unt = 120
        st.session_state.target_ielts = 6.0
        st.session_state.target_sat = 1200
        st.session_state.interests = "IT, инженерия, программирование"
    else:
        # Очистка полей при выключении демо-режима
        st.session_state.track = "KZ (ЕНТ / Гранты)"
        st.session_state.grade = "10 класс"
        st.session_state.subjects = ""
        st.session_state.financial_status = ""
        st.session_state.target_unt = 110
        st.session_state.target_ielts = 0.0
        st.session_state.target_sat = 0
        st.session_state.interests = ""

# Чекбокс с привязкой к функции автозаполнения
demo_mode = st.sidebar.checkbox(
    "🚀 Включить Демо-режим (для питча)", 
    key="demo_mode", 
    on_change=toggle_demo
)

# Управление ключом API
if not cloud_api_key:
    user_api_key = st.sidebar.text_input("Gemini API Key:", type="password")
else:
    user_api_key = cloud_api_key
    st.sidebar.success("🔒 ИИ-ключ успешно подключен")

# Форма анкеты с привязкой к session_state
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
    subjects = st.text_input(
        "Профильные предметы (например: Математика + Физика)",
        key="subjects"
    )
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
        * **Рекомендации и целевые вузы:**
          1. **Главная цель по ЕНТ:** Набрать 120+ баллов для получения государственного гранта на IT-специальности.
          2. **Рекомендуемые вузы:** 
             * **КБТУ (Казахско-Британский технический университет)** — лучший выбор для IT и программной инженерии.
             * **СДУ (Suleyman Demirel University)** — сильная школа математики и программирования.
             * **Satbayev University** — отличные инженерные гранты.
          3. **План подготовки:** Фокус на сложные задачи второй части математики и разделы механики в физике. Участие в хакатоне **SPARK Startup Battle** для портфолио!
        """)
    elif not cloud_api_key and not user_api_key:
        st.error("⚠️ Внимание: Streamlit Cloud не обнаружил ключ 'GEMINI_API_KEY' в настройках Secrets! Проверьте вкладку Settings -> Secrets в панели управления.")
    else:
        active_key = cloud_api_key if cloud_api_key else user_api_key
        with st.spinner("🤖 ИИ анализирует данные и строит индивидуальный трек..."):
            ai = FuturePathAI(api_key=active_key)
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
                st.json(result)
