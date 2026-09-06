import streamlit as st
from futurepath_ai import FuturePathAI

st.set_page_config(page_title="FuturePath.kz", page_icon="🎓", layout="centered")

st.title("🎓 FuturePath.kz")
st.write("Персональный AI-навигатор по поступлению в вузы")

# Пытаемся автоматически достать ключ из секретов Streamlit Cloud
cloud_api_key = ""
if "GEMINI_API_KEY" in st.secrets:
    cloud_api_key = st.secrets["GEMINI_API_KEY"]

st.sidebar.header("⚙️ Настройки ИИ")

# Инициализация состояния сессии для демо-режима
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

# Инициализация полей формы в session_state, если их еще нет
if "track" not in st.session_state:
    st.session_state.track = "KZ (ЕНТ / Гранты)"
if "grade" not in st.session_state:
    st.session_state.grade = "10 класс"
if "subjects" not in st.session_state:
    st.session_state.subjects = ""
if "target_score" not in st.session_state:
    st.session_state.target_score = 110
if "interests" not in st.session_state:
    st.session_state.interests = ""

# Функция автозаполнения или очистки полей при переключении галочки
def toggle_demo():
    if st.session_state.demo_mode:
        # Автозаполнение для презентации (ФизМат, 11 класс)
        st.session_state.track = "KZ (ЕНТ / Гранты)"
        st.session_state.grade = "11 класс / Колледж"
        st.session_state.subjects = "Математика + Физика"
        st.session_state.target_score = 120
        st.session_state.interests = "IT, инженерия, программирование"
    else:
        # Очистка полей при выключении демо-режима
        st.session_state.track = "KZ (ЕНТ / Гранты)"
        st.session_state.grade = "10 класс"
        st.session_state.subjects = ""
        st.session_state.target_score = 110
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

# Форма анкеты с привязкой к session_state (поля сами заполняются и очищаются)
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
    target_score = st.slider(
        "Желаемый балл ЕНТ / Цель по IELTS", 
        50, 140, 
        key="target_score"
    )
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
        * **Профиль:** 11 класс | Математика + Физика (Цель: 120+ баллов)
        * **Рекомендации и целевые вузы:**
          1. **Главная цель по ЕНТ:** Набрать 120+ баллов для получения государственного гранта на IT-специальности.
          2. **Рекомендуемые вузы:** 
             * **КБТУ (Казахско-Британский технический университет)** — лучший выбор для IT и программной инженерии.
             * **СДУ (Suleyman Demirel University)** — сильная школа математики и программирования.
             * **Satbayev University** — отличные инженерные гранты.
          3. **План подготовки:** Фокус на сложные задачи второй части профильной математики и разделы механики в физике. Участие в хакатоне **SPARK Startup Battle** для портфолио!
        """)
    elif not user_api_key:
        st.error("⚠️ Пожалуйста, укажите API-ключ в настройках Secrets или в боковой панели!")
    else:
        with st.spinner("🤖 ИИ анализирует данные и строит индивидуальный трек..."):
            ai = FuturePathAI(api_key=user_api_key)
            user_profile = {
                "track": track,
                "grade": grade,
                "subjects": subjects,
                "target_score": target_score,
                "interests": interests
            }
            result = ai.generate_roadmap(user_profile)
            
            if "error" in result:
                st.error(f"Ошибка от Gemini API: {result['error']}")
            else:
                st.success("🎉 Ваша дорожная карта готова!")
                st.json(result)
