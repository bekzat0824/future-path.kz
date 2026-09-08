import streamlit as st
import pandas as pd
from futurepath_ai import FuturePathAI

st.set_page_config(page_title="BolashaqZholy.kz", page_icon="🎓", layout="centered")

# --- Генерация .ics файла (Календарь дедлайнов) ---
def create_ics_file(steps):
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//BolashaqZholy.kz//Admissions Roadmap//RU",
        "CALSCALE:GREGORIAN"
    ]
    for idx, step in enumerate(steps, 1):
        period = step.get('period', f'Шаг {idx}') if isinstance(step, dict) else f'Шаг {idx}'
        action = step.get('action', str(step)) if isinstance(step, dict) else str(step)
        ics_lines.extend([
            "BEGIN:VEVENT",
            f"SUMMARY:BolashaqZholy: {period}",
            f"DESCRIPTION:{action}",
            "STATUS:CONFIRMED",
            "END:VEVENT"
        ])
    ics_lines.append("END:VCALENDAR")
    return "\n".join(ics_lines)

# --- Генерация текстового отчета ---
def create_report_txt(user_name, res):
    text = f"=========================================\n"
    text += f" BOLASHAQZHOLY.KZ — ДОРОЖНАЯ КАРТА: {user_name.upper()}\n"
    text += f"=========================================\n\n"
    text += f"📊 Оценка шансов на грант: {res.get('grant_chance_percent', 'N/A')}% ({res.get('grant_status_text', '')})\n"
    if res.get('recommended_direction'):
        text += f"🎯 Рекомендуемое направление: {res.get('recommended_direction')}\n"
    text += "\n-----------------------------------------\n📌 ШАГИ ПОДГОТОВКИ:\n-----------------------------------------\n"
    for s in res.get('steps', []):
        if isinstance(s, dict):
            text += f"• [{s.get('period')}] {s.get('action')}\n"
        else:
            text += f"• {s}\n"
    text += "\n-----------------------------------------\n🎓 РЕКОМЕНДУЕМЫЕ ВУЗЫ:\n-----------------------------------------\n"
    for u in res.get('universities', []):
        if isinstance(u, dict):
            text += f"• {u.get('name')} ({u.get('city')}) | Балл: {u.get('grant_cutoff')} | Грант: {u.get('grant_chance')}\n  Описание: {u.get('description')}\n"
    text += "\n-----------------------------------------\n💡 СОВЕТЫ:\n-----------------------------------------\n"
    for a in res.get('advice', []):
        text += f"• {a}\n"
    return text

# --- Настройка API Ключа ---
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

# --- Боковая панель ---
st.sidebar.header("⚙️ Настройки / Баптаулар")
lang = st.sidebar.selectbox("🌐 Язык / Тіл / Language", ["Русский", "Қазақша", "English"])

def toggle_demo():
    if st.session_state.demo_mode:
        st.session_state.user_name = "Айсултан"

st.sidebar.checkbox("🚀 Демо-режим (для питча)", key="demo_mode", on_change=toggle_demo)

# Полный словарь перевода всего интерфейса
ui_texts = {
    "Русский": {
        "title": "🎓 BolashaqZholy.kz",
        "subtitle": "Персональный AI-навигатор по поступлению в вузы",
        "welcome_hdr": "Привет! Давайте познакомимся 👋",
        "welcome_desc": "Bolashaq Zholy поможет построить пошаговый план, оценить шансы на грант и подобрать идеальный университет.",
        "name_label": "Как тебя зовут?",
        "next_btn": "Начать 🚀",
        "form_hdr": "Анкета абитуриента",
        "gen_btn": "🚀 Определить Bolashaq Zholy",
        "restart_btn": "🔄 Начать заново",
        "chat_hdr": "💬 Задать уточняющий вопрос ИИ",
        "chat_ph": "Спросите что угодно о поступлении...",
        "cal_btn": "📅 Скачать календарь дедлайнов (.ics)",
        "rep_btn": "📄 Скачать полный отчет (.txt)",
        # Поля формы
        "track_lbl": "Трек:",
        "grade_lbl": "Класс / Статус:",
        "undecided_lbl": "🧩 Я ещё не определился с профессией / предметами",
        "inclination_lbl": "Что вам ближе всего?",
        "inclination_opts": ["Логика, цифры, программирование", "Биология, медицина, природа", "Общение, языки, творчество, бизнес"],
        "subj_lbl": "Профильные предметы ЕНТ:",
        "fin_lbl": "Финансовые цели:",
        "fin_opts": ["Рассчитываю только на грант", "Возможно платное обучение", "Зарубежные стипендии"],
        "unt_lbl": "Целевой балл ЕНТ:",
        "ielts_lbl": "Целевой IELTS (0 если не нужен):",
        "sat_lbl": "Целевой SAT (0 если не нужен):",
        "interests_lbl": "Дополнительные интересы и хобби:",
        "interests_ph": "IT, стартапы, технологии"
    },
    "Қазақша": {
        "title": "🎓 BolashaqZholy.kz",
        "subtitle": "Болашаққа жол сілтейтін AI-навигатор",
        "welcome_hdr": "Сәлем! Танысып өтейік 👋",
        "welcome_desc": "Bolashaq Zholy саған дайындық жоспарын құруға, грант мүмкіндігін бағалауға және ЖОО таңдауға көмектеседі.",
        "name_label": "Есімің кім?",
        "next_btn": "Бастау 🚀",
        "form_hdr": "Талапкер анкетасы",
        "gen_btn": "🚀 Болашақ жолын анықтау",
        "restart_btn": "🔄 Қайта бастау",
        "chat_hdr": "💬 AI-ға қосымша сұрақ қою",
        "chat_ph": "Оқуға түсу туралы сұраңыз...",
        "cal_btn": "📅 Күнтізбені жүктеп алу (.ics)",
        "rep_btn": "📄 Толық есепті жүктеу (.txt)",
        # Поля формы
        "track_lbl": "Трек:",
        "grade_lbl": "Сынып / Мәртебе:",
        "undecided_lbl": "🧩 Мамандық немесе пәндерді әлі таңдамадым",
        "inclination_lbl": "Сізге қай бағыт жақынырақ?",
        "inclination_opts": ["Логика, сандар, бағдарламалау", "Биология, медицина, табиғат", "Қарым-қатынас, тілдер, өнер, бизнес"],
        "subj_lbl": "ҰБТ бейіндік пәндері:",
        "fin_lbl": "Қаржылық мақсаттар:",
        "fin_opts": ["Тек грантқа үміттенемін", "Ақылы оқу мүмкіндігі бар", "Шетелдік стипендиялар"],
        "unt_lbl": "ҰБТ мақсатты балы:",
        "ielts_lbl": "Мақсатты IELTS (керек болмаса 0):",
        "sat_lbl": "Мақсатты SAT (керек болмаса 0):",
        "interests_lbl": "Қосымша қызығушылықтар мен хобби:",
        "interests_ph": "IT, стартаптар, технологиялар"
    },
    "English": {
        "title": "🎓 BolashaqZholy.kz",
        "subtitle": "Personal AI Navigator for University Admissions",
        "welcome_hdr": "Hello! Let's get started 👋",
        "welcome_desc": "Bolashaq Zholy will help you build a preparation roadmap, calculate grant odds, and select universities.",
        "name_label": "What is your name?",
        "next_btn": "Start 🚀",
        "form_hdr": "Applicant Form",
        "gen_btn": "🚀 Generate Bolashaq Path",
        "restart_btn": "🔄 Start Over",
        "chat_hdr": "💬 Ask AI a Follow-up Question",
        "chat_ph": "Ask anything about admissions...",
        "cal_btn": "📅 Download Deadlines Calendar (.ics)",
        "rep_btn": "📄 Download Full Report (.txt)",
        # Поля формы
        "track_lbl": "Track:",
        "grade_lbl": "Grade / Status:",
        "undecided_lbl": "🧩 I haven't decided on a career / subjects yet",
        "inclination_lbl": "What field interests you the most?",
        "inclination_opts": ["Logic, numbers, programming", "Biology, medicine, nature", "Communication, languages, arts, business"],
        "subj_lbl": "UNT Elective Subjects:",
        "fin_lbl": "Financial Goals:",
        "fin_opts": ["Relying only on a state grant", "Paid tuition is an option", "International scholarships"],
        "unt_lbl": "Target UNT Score:",
        "ielts_lbl": "Target IELTS (0 if not needed):",
        "sat_lbl": "Target SAT (0 if not needed):",
        "interests_lbl": "Additional Interests & Hobbies:",
        "interests_ph": "IT, startups, tech"
    }
}

t = ui_texts[lang]

st.title(t["title"])
st.caption(t["subtitle"])
st.markdown("---")

# ==========================================
# ОКНО 1: Приветствие
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
            st.warning("Введите имя!")

# ==========================================
# ОКНО 2: Анкета + Профориентация
# ==========================================
elif st.session_state.page == "form":
    st.subheader(f"{t['form_hdr']}: {st.session_state.user_name}")
    
    with st.form("student_form"):
        track = st.selectbox(t["track_lbl"], ["KZ (ЕНТ / Гранты)", "International (Зарубежные вузы)"])
        grade = st.selectbox(t["grade_lbl"], ["10 класс", "11 класс / Колледж"])
        
        # Динамический блок профориентации
        undecided = st.checkbox(t["undecided_lbl"])
        inclination = ""
        if undecided:
            inclination = st.radio(t["inclination_lbl"], t["inclination_opts"])
        
        subject_comb = st.selectbox(
            t["subj_lbl"], 
            [
                "Математика + Физика", "Математика + Информатика", "Математика + География",
                "Биология + Химия", "Биология + География", "История + Иностранный язык",
                "История + ЧОП", "География + Иностранный язык", "Творческий экзамен", "Другое"
            ]
        )
        subjects = subject_comb
        financial_status = st.selectbox(t["fin_lbl"], t["fin_opts"])
        
        target_unt = st.slider(t["unt_lbl"], 50, 140, 115)
        target_ielts = st.number_input(t["ielts_lbl"], 0.0, 9.0, 6.0, step=0.5)
        target_sat = st.number_input(t["sat_lbl"], 0, 1600, 1200, step=10)
        interests = st.text_area(t["interests_lbl"], t["interests_ph"])
        
        submitted = st.form_submit_button(t["gen_btn"])
        
    if submitted:
        st.session_state.user_profile = {
            "name": st.session_state.user_name,
            "track": track,
            "grade": grade,
            "undecided": undecided,
            "inclination": inclination,
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
# ОКНО 3: Результаты и Дорожная карта
# ==========================================
elif st.session_state.page == "roadmap":
    col_t, col_r = st.columns([3, 1])
    col_t.subheader(f"🎓 Карта: {st.session_state.user_name}")
    if col_r.button(t["restart_btn"]):
        st.session_state.page = "welcome"
        st.session_state.chat_history = []
        st.session_state.roadmap_result = None
        st.rerun()

    # Генерация данных или Демо
    if st.session_state.roadmap_result is None:
        if st.session_state.demo_mode:
            st.session_state.roadmap_result = {
                "grant_chance_percent": 85,
                "grant_status_text": "Высокая вероятность получения гранта",
                "recommended_direction": "Software Engineering / Computer Science",
                "steps": [
                    {"period": "Сентябрь - Ноябрь 2026", "action": "Интенсивная подготовка по Математике и Физике."},
                    {"period": "Декабрь 2026", "action": "Пробный ЕНТ. Проверка слабых тем."},
                    {"period": "Январь 2027", "action": "Сдача официального январского ЕНТ."},
                    {"period": "Июль 2027", "action": "Подача документов на конкурс грантов."}
                ],
                "universities": [
                    {"name": "КБТУ", "city": "Алматы", "grant_cutoff": "115+", "tuition": "~1.8 млн ₸", "dorm": "Есть", "grant_chance": "Высокий", "description": "Флагман IT-образования в РК."},
                    {"name": "SDU", "city": "Каскелен", "grant_cutoff": "105+", "tuition": "~1.5 млн ₸", "dorm": "Есть", "grant_chance": "Высокий", "description": "Сильный IT-факультет и англоязычное обучение."},
                    {"name": "Satbayev University", "city": "Алматы", "grant_cutoff": "95+", "tuition": "~1.1 млн ₸", "dorm": "Есть", "grant_chance": "Очень высокий", "description": "Большое количество государственных грантов."}
                ],
                "advice": ["Обязательно участвуйте в мартовском и майском ЕНТ.", "Заранее подготовьте справки 075/у."]
            }
        elif api_key:
            with st.spinner("🤖 ИИ генерирует аналитику и дорожную карту..."):
                ai = FuturePathAI(api_key=api_key)
                st.session_state.roadmap_result = ai.generate_roadmap(st.session_state.user_profile, lang=lang)

    res = st.session_state.roadmap_result

    if res and "error" not in res:
        # 1. Шанс на грант
        chance_pct = res.get("grant_chance_percent", 70)
        status_txt = res.get("grant_status_text", "Средние шансы")
        
        st.markdown("### 📊 Оценка шансов на грант")
        col_m1, col_m2 = st.columns([1, 2])
        col_m1.metric("Вероятность", f"{chance_pct}%")
        col_m2.write(f"**Статус:** {status_txt}")
        st.progress(chance_pct / 100)
        
        if res.get("recommended_direction"):
            st.info(f"🎯 **Рекомендуемое направление:** {res.get('recommended_direction')}")

        st.markdown("---")

        # 2. Сравнительная Таблица Вузов
        if "universities" in res and res["universities"]:
            st.markdown("### ⚔️ Сравнительная матрица вузов")
            unis = res["universities"]
            if isinstance(unis, list) and len(unis) > 0 and isinstance(unis[0], dict):
                df = pd.DataFrame(unis)
                rename_dict = {
                    "name": "Вуз", "city": "Город", "grant_cutoff": "Проходной балл",
                    "tuition": "Стоимость", "dorm": "Общежитие", "grant_chance": "Шанс на грант",
                    "description": "Описание"
                }
                df = df.rename(columns=rename_dict)
                st.dataframe(df, use_container_width=True)
            else:
                for u in unis:
                    st.markdown(f"* {u}")

        # 3. Шаги Подготовки
        if "steps" in res:
            st.markdown("### 📌 Персональные шаги подготовки")
            for step in res["steps"]:
                if isinstance(step, dict):
                    st.markdown(f"* **{step.get('period')}** — {step.get('action')}")
                else:
                    st.markdown(f"* {step}")

        # 4. Скачивание файлов
        st.markdown("### 📥 Экспорт и интеграции")
        col_dl1, col_dl2 = st.columns(2)
        
        ics_data = create_ics_file(res.get("steps", []))
        col_dl1.download_button(
            label=t["cal_btn"],
            data=ics_data,
            file_name="BolashaqZholy_Deadlines.ics",
            mime="text/calendar"
        )
        
        report_data = create_report_txt(st.session_state.user_name, res)
        col_dl2.download_button(
            label=t["rep_btn"],
            data=report_data,
            file_name=f"BolashaqZholy_Report_{st.session_state.user_name}.txt",
            mime="text/plain"
        )

        st.markdown("---")

        # 5. Чат с ИИ
        st.subheader(t["chat_hdr"])
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
                        answer = f"В демо-режиме: {st.session_state.user_name}, с вашей целевой планкой шанс прохождения в КБТУ и SDU превышает 80%!"
                    elif api_key:
                        ai = FuturePathAI(api_key=api_key)
                        answer = ai.ask_followup(st.session_state.user_profile, res, user_question, lang=lang)
                    else:
                        answer = "Ошибка API ключа."
                    st.write(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    else:
        st.error("Ошибка при получении данных от ИИ.")
