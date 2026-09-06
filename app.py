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
demo_mode = st.sidebar.checkbox("🚀 Включить Демо-режим (для питча)", value=False)

# Если ключа нет в облаке — даем поле для ручного ввода. Если ключ есть — скрываем его, чтобы пользователи не путались
if not cloud_api_key:
    user_api_key = st.sidebar.text_input("Gemini API Key:", type="password")
else:
    user_api_key = cloud_api_key
    st.sidebar.success("🔒 ИИ-ключ успешно подключен")

# Основная форма сбора данных
with st.form("student_form"):
    st.subheader("Анкета абитуриента")
    
    track = st.selectbox("Выберите основной трек:", ["KZ (ЕНТ / Гранты)", "International (Зарубежные вузы)"])
    grade = st.selectbox("Класс:", ["10 класс", "11 класс / Колледж"])
    subjects = st.text_input("Профильные предметы (например: Математика + Физика)")
    target_score = st.slider("Желаемый балл ЕНТ / Цель по IELTS", 50, 140, 110)
    interests = st.text_area("Интересы и будущая профессия (например: IT, инженерия, медицина)")
    
    submitted = st.form_submit_button("🚀 Сгенерировать дорожную карту")

if submitted:
    if demo_mode:
        st.info("📌 Работает Демо-режим (статический ответ для презентации).")
        st.success("🎉 Ваша дорожная карта готова (Демо)!")
        st.markdown("""
        ### 🎓 Индивидуальный план поступления (FuturePath.kz)
        * **Выбранный трек:** Казахстанские вузы (ЕНТ / Гранты)
        * **Рекомендуемые шаги:**
          1. **Подготовка к ЕНТ:** Фокус на профильные предметы, цель — 115+ баллов.
          2. **Портфолио:** Участие в олимпиадах и хакатонах (SPARK Startup Battle).
          3. **Подача документов:** Сбор пакета документов на грант в июле.
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
