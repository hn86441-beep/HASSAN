import streamlit as st
import requests
import json
from datetime import datetime
import math

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="القرآن الكريم - مصحف هاشم الذكي",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS الإبداعي ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Cairo:wght@300;400;600;700&display=swap');

:root {
    --gold: #C9A84C;
    --dark-green: #1a3a2a;
    --medium-green: #2d6a4f;
    --light-green: #52b788;
    --cream: #fdf8f0;
    --dark-bg: #0d1f16;
    --card-bg: #162a1f;
    --text-light: #e8f5e9;
    --text-muted: #a5d6a7;
    --border: #2d5a3d;
    --shadow: rgba(0,0,0,0.4);
}

/* الوضع المظلم الافتراضي */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a1a0f 0%, #0d2018 50%, #0a1a0f 100%);
    min-height: 100vh;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1f16 0%, #162a1f 100%) !important;
    border-right: 1px solid var(--border);
}

/* إخفاء عناصر Streamlit الافتراضية */
#MainMenu, footer, header {display: none !important;}
[data-testid="stDeployButton"] {display: none;}

/* ==================== رأس التطبيق ==================== */
.app-header {
    background: linear-gradient(135deg, #0d2018 0%, #1a3a2a 50%, #0d2018 100%);
    border: 1px solid var(--gold);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    margin-bottom: 25px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(201, 168, 76, 0.2);
}

.app-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(201,168,76,0.05) 0%, transparent 60%);
    animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 1; }
}

.app-header h1 {
    font-family: 'Amiri', serif;
    font-size: 3rem;
    color: var(--gold);
    text-shadow: 0 0 30px rgba(201,168,76,0.5);
    margin: 0;
    direction: rtl;
}

.app-header p {
    font-family: 'Cairo', sans-serif;
    color: var(--text-muted);
    font-size: 1rem;
    margin: 8px 0 0 0;
    direction: rtl;
}

/* ==================== الزخارف الإسلامية ==================== */
.islamic-divider {
    text-align: center;
    color: var(--gold);
    font-size: 1.5rem;
    margin: 15px 0;
    letter-spacing: 8px;
}

/* ==================== الكروت ==================== */
.feature-card {
    background: linear-gradient(135deg, var(--card-bg), #1e3a2a);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    margin: 10px 0;
    cursor: pointer;
    transition: all 0.3s ease;
    direction: rtl;
    text-align: right;
}

.feature-card:hover {
    border-color: var(--gold);
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(201,168,76,0.2);
}

.feature-card .icon {
    font-size: 2.5rem;
    margin-bottom: 10px;
    display: block;
}

.feature-card h3 {
    color: var(--gold);
    font-family: 'Cairo', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0 0 5px 0;
}

.feature-card p {
    color: var(--text-muted);
    font-family: 'Cairo', sans-serif;
    font-size: 0.85rem;
    margin: 0;
}

/* ==================== آيات القرآن ==================== */
.ayah-container {
    background: linear-gradient(135deg, #0d2018, #162a1f);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 30px;
    margin: 15px 0;
    direction: rtl;
    text-align: right;
    position: relative;
    transition: all 0.3s;
}

.ayah-container:hover {
    border-color: var(--gold);
    box-shadow: 0 4px 20px rgba(201,168,76,0.15);
}

.ayah-number {
    background: linear-gradient(135deg, var(--gold), #a07830);
    color: #0a1a0f;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-family: 'Amiri', serif;
    font-size: 1rem;
    font-weight: 700;
    margin-left: 12px;
    flex-shrink: 0;
}

.ayah-text {
    font-family: 'Amiri', serif;
    font-size: 1.8rem;
    color: #f5f0e8;
    line-height: 2.5;
    margin-bottom: 12px;
}

.ayah-translation {
    font-family: 'Cairo', sans-serif;
    font-size: 0.95rem;
    color: var(--text-muted);
    font-style: italic;
    border-top: 1px solid var(--border);
    padding-top: 12px;
    margin-top: 12px;
}

/* ==================== شريط التنقل الجانبي ==================== */
.nav-button {
    background: linear-gradient(135deg, #162a1f, #1e3a2a);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 12px 15px;
    margin: 5px 0;
    cursor: pointer;
    width: 100%;
    text-align: right;
    direction: rtl;
    color: var(--text-light);
    font-family: 'Cairo', sans-serif;
    font-size: 0.9rem;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 10px;
}

.nav-button:hover, .nav-button.active {
    background: linear-gradient(135deg, var(--medium-green), var(--dark-green));
    border-color: var(--gold);
    color: var(--gold);
}

/* ==================== البسملة ==================== */
.bismillah {
    font-family: 'Amiri', serif;
    font-size: 2.5rem;
    color: var(--gold);
    text-align: center;
    padding: 25px;
    margin: 15px 0;
    text-shadow: 0 0 20px rgba(201,168,76,0.4);
    direction: rtl;
}

/* ==================== الإحصائيات ==================== */
.stat-box {
    background: linear-gradient(135deg, #0d2018, #162a1f);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    direction: rtl;
}

.stat-box .number {
    font-family: 'Amiri', serif;
    font-size: 2.5rem;
    color: var(--gold);
    font-weight: 700;
    display: block;
}

.stat-box .label {
    font-family: 'Cairo', sans-serif;
    color: var(--text-muted);
    font-size: 0.85rem;
}

/* ==================== زر التشغيل ==================== */
.play-button {
    background: linear-gradient(135deg, var(--gold), #a07830);
    color: #0a1a0f;
    border: none;
    border-radius: 50px;
    padding: 10px 25px;
    font-family: 'Cairo', sans-serif;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s;
    font-size: 0.9rem;
}

.play-button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 20px rgba(201,168,76,0.4);
}

/* ==================== بطاقة السورة ==================== */
.surah-card {
    background: linear-gradient(135deg, #0d2018, #162a1f);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 15px 20px;
    margin: 8px 0;
    cursor: pointer;
    transition: all 0.25s;
    direction: rtl;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.surah-card:hover {
    border-color: var(--gold);
    background: linear-gradient(135deg, #162a1f, #1e3a2a);
    transform: translateX(-3px);
}

.surah-number-badge {
    background: rgba(201,168,76,0.15);
    border: 1px solid var(--gold);
    color: var(--gold);
    width: 38px;
    height: 38px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Amiri', serif;
    font-size: 0.9rem;
    flex-shrink: 0;
}

.surah-info h4 {
    color: #f5f0e8;
    font-family: 'Amiri', serif;
    font-size: 1.2rem;
    margin: 0;
}

.surah-info small {
    color: var(--text-muted);
    font-family: 'Cairo', sans-serif;
    font-size: 0.75rem;
}

/* ==================== تبويبات ==================== */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    gap: 5px;
    direction: rtl;
}

.stTabs [data-baseweb="tab"] {
    background: #162a1f !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-muted) !important;
    font-family: 'Cairo', sans-serif !important;
    padding: 8px 20px !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--medium-green), var(--dark-green)) !important;
    border-color: var(--gold) !important;
    color: var(--gold) !important;
}

/* ==================== نمط Focus Mode ==================== */
.focus-mode {
    background: #080f0a;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
}

.focus-ayah {
    font-family: 'Amiri', serif;
    font-size: 2.5rem;
    color: #f5f0e8;
    text-align: center;
    line-height: 3;
    direction: rtl;
    max-width: 900px;
    text-shadow: 0 0 40px rgba(201,168,76,0.2);
}

/* ==================== شريط التقدم ==================== */
.progress-bar {
    background: var(--border);
    border-radius: 10px;
    height: 6px;
    overflow: hidden;
    margin: 10px 0;
}

.progress-fill {
    background: linear-gradient(90deg, var(--gold), var(--light-green));
    height: 100%;
    border-radius: 10px;
    transition: width 0.3s;
}

/* ==================== الختمة ==================== */
.khatma-grid {
    display: grid;
    grid-template-columns: repeat(10, 1fr);
    gap: 5px;
    direction: rtl;
}

.khatma-cell {
    background: #162a1f;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'Cairo', sans-serif;
    font-size: 0.7rem;
    color: var(--text-muted);
}

.khatma-cell.completed {
    background: linear-gradient(135deg, var(--medium-green), var(--dark-green));
    border-color: var(--gold);
    color: var(--gold);
}

.khatma-cell:hover {
    border-color: var(--gold);
}

/* ==================== قسم الأذكار ==================== */
.dhikr-card {
    background: linear-gradient(135deg, #0d2018, #162a1f);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 25px;
    margin: 12px 0;
    direction: rtl;
    text-align: center;
    transition: all 0.3s;
}

.dhikr-card:hover {
    border-color: var(--gold);
    box-shadow: 0 5px 20px rgba(201,168,76,0.15);
}

.dhikr-text {
    font-family: 'Amiri', serif;
    font-size: 1.8rem;
    color: #f5f0e8;
    margin-bottom: 10px;
    line-height: 2;
}

.dhikr-count {
    background: linear-gradient(135deg, var(--gold), #a07830);
    color: #0a1a0f;
    border-radius: 50px;
    padding: 5px 20px;
    font-family: 'Cairo', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    display: inline-block;
}

/* ==================== أوقات الصلاة ==================== */
.prayer-time-card {
    background: linear-gradient(135deg, #0d2018, #162a1f);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 15px 20px;
    margin: 8px 0;
    direction: rtl;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.2s;
}

.prayer-time-card.active {
    border-color: var(--gold);
    background: linear-gradient(135deg, #162a1f, #1e3a2a);
    box-shadow: 0 3px 15px rgba(201,168,76,0.2);
}

.prayer-name {
    font-family: 'Cairo', sans-serif;
    color: var(--text-light);
    font-size: 1rem;
    font-weight: 600;
}

.prayer-name.active {
    color: var(--gold);
}

.prayer-time {
    font-family: 'Amiri', serif;
    color: var(--gold);
    font-size: 1.2rem;
}

/* ==================== مصراع الخريطة الذهنية ==================== */
.mind-map-container {
    background: #080f0a;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 30px;
    min-height: 400px;
    position: relative;
    overflow: hidden;
}

.mind-node {
    background: linear-gradient(135deg, var(--dark-green), var(--medium-green));
    border: 2px solid var(--gold);
    border-radius: 50px;
    padding: 10px 20px;
    display: inline-block;
    margin: 5px;
    color: var(--gold);
    font-family: 'Cairo', sans-serif;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
}

.mind-node:hover {
    background: linear-gradient(135deg, var(--medium-green), var(--light-green));
    color: #0a1a0f;
    transform: scale(1.05);
}

.mind-node.center {
    background: linear-gradient(135deg, var(--gold), #a07830);
    color: #0a1a0f;
    font-size: 1.1rem;
    font-weight: 700;
    padding: 15px 30px;
}

/* ==================== بطاقة الحديث ==================== */
.hadith-card {
    background: linear-gradient(135deg, #0d2018, #162a1f);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 25px;
    margin: 12px 0;
    direction: rtl;
    position: relative;
}

.hadith-card::before {
    content: '❝';
    position: absolute;
    top: 15px;
    right: 20px;
    font-size: 3rem;
    color: rgba(201,168,76,0.2);
    font-family: serif;
    line-height: 1;
}

.hadith-text {
    font-family: 'Amiri', serif;
    font-size: 1.3rem;
    color: #f5f0e8;
    line-height: 2;
    margin-bottom: 12px;
    padding-right: 20px;
}

.hadith-source {
    font-family: 'Cairo', sans-serif;
    font-size: 0.8rem;
    color: var(--gold);
    border-top: 1px solid var(--border);
    padding-top: 10px;
}

/* ==================== AI Assistant ==================== */
.ai-message {
    background: linear-gradient(135deg, #0d2018, #162a1f);
    border: 1px solid var(--border);
    border-radius: 16px 16px 16px 0;
    padding: 15px 20px;
    margin: 10px 0;
    direction: rtl;
    max-width: 80%;
}

.user-message {
    background: linear-gradient(135deg, var(--medium-green), var(--dark-green));
    border: 1px solid var(--gold);
    border-radius: 16px 16px 0 16px;
    padding: 15px 20px;
    margin: 10px 0 10px auto;
    direction: rtl;
    max-width: 80%;
    text-align: right;
}

.message-text {
    font-family: 'Cairo', sans-serif;
    color: var(--text-light);
    font-size: 0.95rem;
    line-height: 1.7;
}

/* ==================== شريط اختيار الشيخ ==================== */
.sheikh-selector {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    direction: rtl;
    margin: 15px 0;
}

.sheikh-btn {
    background: #162a1f;
    border: 1px solid var(--border);
    border-radius: 25px;
    padding: 8px 18px;
    color: var(--text-muted);
    font-family: 'Cairo', sans-serif;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
}

.sheikh-btn.active {
    background: linear-gradient(135deg, var(--gold), #a07830);
    border-color: var(--gold);
    color: #0a1a0f;
    font-weight: 700;
}

/* ==================== Buttons Streamlit ==================== */
.stButton > button {
    background: linear-gradient(135deg, #1e3a2a, #2d6a4f) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-light) !important;
    font-family: 'Cairo', sans-serif !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    border-color: var(--gold) !important;
    color: var(--gold) !important;
    transform: translateY(-2px) !important;
}

/* Primary button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--gold), #a07830) !important;
    color: #0a1a0f !important;
    font-weight: 700 !important;
    border: none !important;
}

/* ==================== Inputs ==================== */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background: #162a1f !important;
    border-color: var(--border) !important;
    color: var(--text-light) !important;
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
}

.stSlider > div > div {
    background: var(--border) !important;
}

/* ==================== وضع التلاوة المركّز ==================== */
.reading-mode-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: #050d08;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ==================== شريط التقدم المصحف ==================== */
.mushaf-progress {
    background: #162a1f;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 15px 20px;
    margin: 10px 0;
    direction: rtl;
}

/* ==================== تأثيرات الزخرفة ==================== */
.ornament {
    text-align: center;
    color: var(--gold);
    font-size: 1.2rem;
    opacity: 0.6;
    margin: 5px 0;
    letter-spacing: 5px;
}

/* ==================== صندوق المشاعر ==================== */
.emotion-tag {
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 20px;
    padding: 5px 14px;
    color: var(--gold);
    font-family: 'Cairo', sans-serif;
    font-size: 0.8rem;
    display: inline-block;
    margin: 3px;
    cursor: pointer;
    transition: all 0.2s;
}

.emotion-tag:hover, .emotion-tag.selected {
    background: rgba(201,168,76,0.25);
    border-color: var(--gold);
}

/* ==================== إشعار ==================== */
.notification {
    background: linear-gradient(135deg, var(--medium-green), var(--dark-green));
    border: 1px solid var(--gold);
    border-radius: 12px;
    padding: 12px 20px;
    margin: 10px 0;
    direction: rtl;
    font-family: 'Cairo', sans-serif;
    color: var(--text-light);
    font-size: 0.9rem;
}

/* ==================== جدول ==================== */
.stDataFrame {
    background: #162a1f !important;
    color: var(--text-light) !important;
    direction: rtl;
}

/* ==================== Scrollbar ==================== */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1f16; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

/* ==================== Logo watermark ==================== */
.watermark {
    position: fixed;
    bottom: 20px;
    left: 20px;
    opacity: 0.15;
    font-family: 'Amiri', serif;
    font-size: 1.5rem;
    color: var(--gold);
    pointer-events: none;
    z-index: 100;
}

</style>
""", unsafe_allow_html=True)

# ==================== تهيئة الجلسة ====================
def init_session():
    defaults = {
        'page': 'home',
        'current_surah': 1,
        'current_ayah': 1,
        'font_size': 2.0,
        'selected_sheikh': 'ar.alafasy',
        'focus_mode': False,
        'bookmarks': [],
        'heart_library': [],
        'khatma_progress': [False] * 114,
        'reading_progress': {},
        'daily_dhikr_count': {},
        'chat_history': [],
        'show_translation': True,
        'show_tafseer': False,
        'dark_mode': True,
        'tajweed_mode': False,
        'listening_mood': None,
        'completed_pages': set(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ==================== البيانات والـ APIs ====================

SHEIKHS = {
    "ar.alafasy": "مشاري راشد العفاسي",
    "ar.abdullahbasfar": "عبد الله بصفر",
    "ar.hudhaify": "علي الحذيفي",
    "ar.minshawi": "محمد صديق المنشاوي",
    "ar.abdurrahmaansudais": "عبد الرحمن السديس",
    "ar.shaatree": "أبو بكر الشاطري",
    "ar.mahermuaiqly": "ماهر المعيقلي",
    "ar.muhammadayyoub": "محمد أيوب",
}

MOODS = {
    "حزن وضيق": [2, 94, 65, 93],
    "فرح وشكر": [55, 36, 67, 1],
    "خوف وقلق": [2, 3, 13, 58],
    "توبة وندم": [39, 4, 25, 110],
    "تأمل وتدبر": [3, 45, 88, 56],
    "قبل النوم": [67, 32, 36, 112],
    "صباح جديد": [78, 87, 1, 36],
    "في المصيبة": [2, 3, 94, 93],
    "طلب الرزق": [67, 65, 73, 20],
    "شفاء المريض": [17, 10, 26, 27],
}

QURAN_DATA = {
    1: {"name": "الفاتحة", "english": "Al-Fatiha", "verses": 7, "type": "مكية", "juz": 1},
    2: {"name": "البقرة", "english": "Al-Baqara", "verses": 286, "type": "مدنية", "juz": 1},
    3: {"name": "آل عمران", "english": "Ali Imran", "verses": 200, "type": "مدنية", "juz": 3},
    4: {"name": "النساء", "english": "An-Nisa", "verses": 176, "type": "مدنية", "juz": 4},
    5: {"name": "المائدة", "english": "Al-Ma'ida", "verses": 120, "type": "مدنية", "juz": 6},
    6: {"name": "الأنعام", "english": "Al-An'am", "verses": 165, "type": "مكية", "juz": 7},
    7: {"name": "الأعراف", "english": "Al-A'raf", "verses": 206, "type": "مكية", "juz": 8},
    8: {"name": "الأنفال", "english": "Al-Anfal", "verses": 75, "type": "مدنية", "juz": 9},
    9: {"name": "التوبة", "english": "At-Tawba", "verses": 129, "type": "مدنية", "juz": 10},
    10: {"name": "يونس", "english": "Yunus", "verses": 109, "type": "مكية", "juz": 11},
    11: {"name": "هود", "english": "Hud", "verses": 123, "type": "مكية", "juz": 11},
    12: {"name": "يوسف", "english": "Yusuf", "verses": 111, "type": "مكية", "juz": 12},
    13: {"name": "الرعد", "english": "Ar-Ra'd", "verses": 43, "type": "مدنية", "juz": 13},
    14: {"name": "إبراهيم", "english": "Ibrahim", "verses": 52, "type": "مكية", "juz": 13},
    15: {"name": "الحجر", "english": "Al-Hijr", "verses": 99, "type": "مكية", "juz": 14},
    16: {"name": "النحل", "english": "An-Nahl", "verses": 128, "type": "مكية", "juz": 14},
    17: {"name": "الإسراء", "english": "Al-Isra", "verses": 111, "type": "مكية", "juz": 15},
    18: {"name": "الكهف", "english": "Al-Kahf", "verses": 110, "type": "مكية", "juz": 15},
    19: {"name": "مريم", "english": "Maryam", "verses": 98, "type": "مكية", "juz": 16},
    20: {"name": "طه", "english": "Ta-Ha", "verses": 135, "type": "مكية", "juz": 16},
    21: {"name": "الأنبياء", "english": "Al-Anbiya", "verses": 112, "type": "مكية", "juz": 17},
    22: {"name": "الحج", "english": "Al-Hajj", "verses": 78, "type": "مدنية", "juz": 17},
    23: {"name": "المؤمنون", "english": "Al-Mu'minun", "verses": 118, "type": "مكية", "juz": 18},
    24: {"name": "النور", "english": "An-Nur", "verses": 64, "type": "مدنية", "juz": 18},
    25: {"name": "الفرقان", "english": "Al-Furqan", "verses": 77, "type": "مكية", "juz": 18},
    36: {"name": "يس", "english": "Ya-Sin", "verses": 83, "type": "مكية", "juz": 22},
    55: {"name": "الرحمن", "english": "Ar-Rahman", "verses": 78, "type": "مدنية", "juz": 27},
    56: {"name": "الواقعة", "english": "Al-Waqi'a", "verses": 96, "type": "مكية", "juz": 27},
    67: {"name": "الملك", "english": "Al-Mulk", "verses": 30, "type": "مكية", "juz": 29},
    78: {"name": "النبأ", "english": "An-Naba", "verses": 40, "type": "مكية", "juz": 30},
    87: {"name": "الأعلى", "english": "Al-A'la", "verses": 19, "type": "مكية", "juz": 30},
    93: {"name": "الضحى", "english": "Ad-Duha", "verses": 11, "type": "مكية", "juz": 30},
    94: {"name": "الشرح", "english": "Ash-Sharh", "verses": 8, "type": "مكية", "juz": 30},
    108: {"name": "الكوثر", "english": "Al-Kawthar", "verses": 3, "type": "مكية", "juz": 30},
    110: {"name": "النصر", "english": "An-Nasr", "verses": 3, "type": "مدنية", "juz": 30},
    112: {"name": "الإخلاص", "english": "Al-Ikhlas", "verses": 4, "type": "مكية", "juz": 30},
    113: {"name": "الفلق", "english": "Al-Falaq", "verses": 5, "type": "مكية", "juz": 30},
    114: {"name": "الناس", "english": "An-Nas", "verses": 6, "type": "مكية", "juz": 30},
}

# Complete all 114 surahs
ALL_SURAHS = {}
surah_names = [
    "الفاتحة","البقرة","آل عمران","النساء","المائدة","الأنعام","الأعراف","الأنفال","التوبة","يونس",
    "هود","يوسف","الرعد","إبراهيم","الحجر","النحل","الإسراء","الكهف","مريم","طه",
    "الأنبياء","الحج","المؤمنون","النور","الفرقان","الشعراء","النمل","القصص","العنكبوت","الروم",
    "لقمان","السجدة","الأحزاب","سبأ","فاطر","يس","الصافات","ص","الزمر","غافر",
    "فصلت","الشورى","الزخرف","الدخان","الجاثية","الأحقاف","محمد","الفتح","الحجرات","ق",
    "الذاريات","الطور","النجم","القمر","الرحمن","الواقعة","الحديد","المجادلة","الحشر","الممتحنة",
    "الصف","الجمعة","المنافقون","التغابن","الطلاق","التحريم","الملك","القلم","الحاقة","المعارج",
    "نوح","الجن","المزمل","المدثر","القيامة","الإنسان","المرسلات","النبأ","النازعات","عبس",
    "التكوير","الانفطار","المطففين","الانشقاق","البروج","الطارق","الأعلى","الغاشية","الفجر","البلد",
    "الشمس","الليل","الضحى","الشرح","التين","العلق","القدر","البينة","الزلزلة","العاديات",
    "القارعة","التكاثر","العصر","الهمزة","الفيل","قريش","الماعون","الكوثر","الكافرون","النصر",
    "المسد","الإخلاص","الفلق","الناس"
]
surah_verses = [7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,110,98,135,112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,83,182,88,75,85,54,53,89,59,37,35,38,29,18,45,60,49,62,55,78,96,29,22,24,13,14,11,11,18,12,12,30,52,52,44,28,28,20,56,40,31,50,40,46,42,29,23,36,25,22,17,19,26,30,20,15,21,11,8,8,19,5,8,8,3,11,4,5,6]

juz_map = [1,1,1,1,1,1,1,1,10,11,11,12,13,13,14,14,15,15,16,16,17,17,18,18,18,19,19,20,20,21,21,21,21,22,22,22,23,23,23,24,24,24,25,25,25,26,26,26,26,26,26,27,27,27,27,27,27,28,28,28,28,28,28,28,28,28,29,29,29,29,29,29,29,29,29,29,29,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30]

for i, name in enumerate(surah_names):
    n = i + 1
    ALL_SURAHS[n] = {
        "name": name,
        "verses": surah_verses[i] if i < len(surah_verses) else 10,
        "type": "مكية" if n not in [2,3,4,5,8,9,13,22,24,33,47,48,49,55,57,58,59,60,61,62,63,64,65,66,76,98,99,110] else "مدنية",
        "juz": juz_map[i] if i < len(juz_map) else 30,
    }

@st.cache_data(ttl=3600)
def get_quran_data(surah, ayah=None):
    try:
        if ayah:
            url = f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}/editions/quran-uthmani,ar.alafasy"
        else:
            url = f"https://api.alquran.cloud/v1/surah/{surah}/editions/quran-uthmani,ar.alafasy"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

@st.cache_data(ttl=3600)
def get_translation(surah, ayah=None, edition="en.sahih"):
    try:
        if ayah:
            url = f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}/{edition}"
        else:
            url = f"https://api.alquran.cloud/v1/surah/{surah}/{edition}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

@st.cache_data(ttl=86400)
def get_prayer_times(lat=30.06, lon=31.24, method=5):
    try:
        now = datetime.now()
        url = f"https://api.aladhan.com/v1/timings/{now.strftime('%d-%m-%Y')}?latitude={lat}&longitude={lon}&method={method}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()['data']['timings']
    except:
        pass
    return None

def get_qibla(lat=30.06, lon=31.24):
    try:
        url = f"https://api.aladhan.com/v1/qibla/{lat}/{lon}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()['data']['direction']
    except:
        pass
    return None

def get_audio_url(surah, ayah, reciter="ar.alafasy"):
    surah_str = str(surah).zfill(3)
    ayah_str = str(ayah).zfill(3)
    reciter_short = reciter.replace("ar.", "")
    url = f"https://cdn.islamic.network/quran/audio/128/{reciter}/{surah_str}{ayah_str}.mp3"
    return url

# ==================== الشريط الجانبي ====================
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding: 15px 0 5px;'>
            <span style='font-size:2.5rem'>🕌</span>
            <h2 style='color:#C9A84C; font-family:Amiri,serif; margin:5px 0; direction:rtl; font-size:1.3rem'>
                مصحف هاشم الذكي
            </h2>
            <p style='color:#a5d6a7; font-family:Cairo,sans-serif; font-size:0.75rem; direction:rtl; margin:0'>
                القرآن الكريم بتجربة فريدة
            </p>
        </div>
        <div class='ornament'>❧ ✦ ❧</div>
        """, unsafe_allow_html=True)

        pages = [
            ("🏠", "home", "الرئيسية"),
            ("📖", "mushaf", "المصحف الشريف"),
            ("🎙️", "audio", "الاستماع والتلاوة"),
            ("🧠", "tajweed", "تصحيح التلاوة بالذكاء الاصطناعي"),
            ("🗺️", "mindmap", "خريطة القصص القرآنية"),
            ("💭", "mood", "القرآن بحسب حالتي"),
            ("📚", "tafseer", "التفسير والتدبر"),
            ("🔍", "search", "البحث بالمقاصد"),
            ("🤖", "ai_assistant", "المساعد القرآني الذكي"),
            ("❤️", "heart", "مكتبة القلب"),
            ("🔖", "bookmarks", "الإشارات المرجعية"),
            ("📿", "khatma", "الختمة"),
            ("🌙", "dhikr", "الأذكار"),
            ("🕌", "prayer", "أوقات الصلاة"),
            ("🧭", "qibla", "اتجاه القبلة"),
            ("📜", "hadith", "الأحاديث الصحيحة"),
            ("⚙️", "settings", "الإعدادات"),
        ]

        for icon, key, label in pages:
            is_active = st.session_state.page == key
            btn_style = "border-color: #C9A84C; color: #C9A84C;" if is_active else ""
            if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()

        st.markdown("""
        <div class='ornament' style='margin-top:20px'>❧ ✦ ❧</div>
        <div style='text-align:center; padding:10px; color:#4a7a5a; font-family:Cairo,sans-serif; font-size:0.75rem; direction:rtl'>
            بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ
        </div>
        """, unsafe_allow_html=True)

# ==================== الصفحة الرئيسية ====================
def render_home():
    st.markdown("""
    <div class='app-header'>
        <div class='ornament'>﴾ ﴿</div>
        <h1>القرآن الكريم</h1>
        <p style='font-size:1.2rem'>مصحف هاشم الذكي — تجربة تلاوة لا مثيل لها</p>
        <div class='ornament'>﴾ ﴿</div>
    </div>
    <div class='bismillah'>بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
    """, unsafe_allow_html=True)

    # إحصائيات
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class='stat-box'><span class='number'>١١٤</span><span class='label'>سورة قرآنية</span></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='stat-box'><span class='number'>٦٢٣٦</span><span class='label'>آية كريمة</span></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='stat-box'><span class='number'>٣٠</span><span class='label'>جزءاً</span></div>""", unsafe_allow_html=True)
    with col4:
        completed = sum(st.session_state.khatma_progress)
        st.markdown(f"""<div class='stat-box'><span class='number'>{completed}</span><span class='label'>سورة أتممتها</span></div>""", unsafe_allow_html=True)

    st.markdown("<div class='islamic-divider'>❧ ✦ ✦ ✦ ❧</div>", unsafe_allow_html=True)

    # الميزات الرئيسية
    st.markdown("""<h3 style='color:#C9A84C;font-family:Cairo,sans-serif;direction:rtl;text-align:right'>✨ الميزات الحصرية</h3>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    features = [
        ("🧠", "تصحيح التلاوة بالذكاء الاصطناعي", "سجّل صوتك وسيصحح لك التجويد ومخارج الحروف فورياً", "tajweed"),
        ("💭", "القرآن بحسب حالتي", "اختر حالتك الوجدانية وسيختار القرآن الآيات المناسبة لك", "mood"),
        ("🗺️", "خريطة القصص القرآنية", "تصفح قصص الأنبياء في خريطة تفاعلية مذهلة", "mindmap"),
        ("🎙️", "ثمانية قراء بدون إنترنت", "استمع لأكثر من 8 مشايخ مع بث مباشر عالي الجودة", "audio"),
        ("🤖", "المساعد القرآني", "اسأل الذكاء الاصطناعي أي سؤال قرآني وسيجيبك فوراً", "ai_assistant"),
        ("❤️", "مكتبة القلب", "احفظ الآيات التي تؤثر فيك مع مشاعرك لتعود إليها", "heart"),
        ("📚", "التفسير التفاعلي", "تفسير ميسّر وسبب النزول والمتشابهات اللفظية", "tafseer"),
        ("📿", "الختمة التفاعلية", "تتبع تقدمك في ختم القرآن الكريم بشكل مرئي", "khatma"),
        ("🌙", "أذكار اليوم", "أذكار الصباح والمساء والنوم بعداد تفاعلي", "dhikr"),
    ]

    cols = [col1, col2, col3]
    for i, (icon, title, desc, page_key) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='feature-card'>
                <span class='icon'>{icon}</span>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"افتح ←", key=f"open_{page_key}_{i}", use_container_width=True):
                st.session_state.page = page_key
                st.rerun()

    st.markdown("<div class='islamic-divider'>❧ ✦ ✦ ✦ ❧</div>", unsafe_allow_html=True)

    # تابع من حيث توقفت
    st.markdown("""<h3 style='color:#C9A84C;font-family:Cairo,sans-serif;direction:rtl;text-align:right'>📖 تابع من حيث توقفت</h3>""", unsafe_allow_html=True)
    last_surah = st.session_state.current_surah
    last_ayah = st.session_state.current_ayah
    surah_info = ALL_SURAHS.get(last_surah, {})
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div class='ayah-container'>
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:10px'>
                <span class='surah-number-badge'>{last_surah}</span>
                <div>
                    <div style='color:#C9A84C;font-family:Amiri,serif;font-size:1.2rem'>سورة {surah_info.get("name","")}</div>
                    <div style='color:#a5d6a7;font-family:Cairo,sans-serif;font-size:0.8rem'>الآية {last_ayah} من {surah_info.get("verses","")}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("▶ تابع القراءة", use_container_width=True):
            st.session_state.page = "mushaf"
            st.rerun()

# ==================== صفحة المصحف ====================
def render_mushaf():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right;font-size:2rem'>📖 المصحف الشريف</h2>""", unsafe_allow_html=True)

    # اختيار السورة
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        surah_options = {v['name']: k for k, v in ALL_SURAHS.items()}
        current_name = ALL_SURAHS.get(st.session_state.current_surah, {}).get('name', 'الفاتحة')
        selected_surah_name = st.selectbox("اختر السورة", list(surah_options.keys()),
                                            index=list(surah_options.keys()).index(current_name) if current_name in surah_options else 0,
                                            key="surah_select")
        st.session_state.current_surah = surah_options[selected_surah_name]

    with col2:
        max_ayah = ALL_SURAHS.get(st.session_state.current_surah, {}).get('verses', 1)
        st.session_state.current_ayah = st.number_input("من الآية", min_value=1, max_value=max_ayah,
                                                          value=min(st.session_state.current_ayah, max_ayah), key="ayah_input")

    with col3:
        font_size = st.slider("حجم الخط", 1.5, 3.5, st.session_state.font_size, 0.1, key="font_slider")
        st.session_state.font_size = font_size

    # خيارات العرض
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        show_trans = st.checkbox("الترجمة", value=st.session_state.show_translation, key="show_trans")
        st.session_state.show_translation = show_trans
    with col2:
        show_tafseer_inline = st.checkbox("التفسير المختصر", value=False, key="show_tafseer_inline")
    with col3:
        focus = st.checkbox("وضع التركيز 🎯", value=st.session_state.focus_mode, key="focus_toggle")
        st.session_state.focus_mode = focus
    with col4:
        if st.button("🔖 إضافة علامة", key="add_bookmark_btn"):
            bookmark = {"surah": st.session_state.current_surah, "ayah": st.session_state.current_ayah,
                       "surah_name": ALL_SURAHS.get(st.session_state.current_surah, {}).get('name', ''), "time": datetime.now().strftime("%Y-%m-%d %H:%M")}
            if bookmark not in st.session_state.bookmarks:
                st.session_state.bookmarks.append(bookmark)
                st.success("✅ تمت إضافة الإشارة المرجعية")

    st.markdown("<div class='islamic-divider'>❧</div>", unsafe_allow_html=True)

    # جلب بيانات السورة
    surah_num = st.session_state.current_surah
    surah_info = ALL_SURAHS.get(surah_num, {})

    # عرض اسم السورة
    if not st.session_state.focus_mode:
        st.markdown(f"""
        <div style='text-align:center; margin:20px 0; padding:20px; background:linear-gradient(135deg,#0d2018,#162a1f); border:1px solid #C9A84C; border-radius:16px'>
            <div style='color:#a5d6a7;font-family:Cairo,sans-serif;font-size:0.85rem;direction:rtl'>{surah_info.get("type","مكية")} • {surah_info.get("verses","?")} آية • الجزء {surah_info.get("juz","?")}</div>
            <div style='color:#C9A84C;font-family:Amiri,serif;font-size:2.5rem;margin:5px 0'>سُورَةُ {surah_info.get("name","")}</div>
        </div>
        """, unsafe_allow_html=True)

        if surah_num != 9:  # لا بسملة في التوبة
            st.markdown("""<div class='bismillah'>بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>""", unsafe_allow_html=True)

    # جلب الآيات
    with st.spinner("جارٍ تحميل الآيات..."):
        data = get_quran_data(surah_num)
        trans_data = get_translation(surah_num) if show_trans else None

    if data and data.get('code') == 200:
        editions = data['data']
        arabic_edition = editions[0] if isinstance(editions, list) else editions

        ayahs = arabic_edition.get('ayahs', [])
        trans_ayahs = []
        if trans_data and trans_data.get('code') == 200:
            trans_ayahs = trans_data['data'].get('ayahs', [])

        # نبدأ من الآية المختارة
        start_idx = st.session_state.current_ayah - 1
        display_ayahs = ayahs[start_idx:start_idx + 20]  # عرض 20 آية
        display_trans = trans_ayahs[start_idx:start_idx + 20] if trans_ayahs else []

        for i, ayah in enumerate(display_ayahs):
            ayah_num = start_idx + i + 1
            ayah_text = ayah.get('text', '')
            trans_text = display_trans[i].get('text', '') if i < len(display_trans) else ''

            if st.session_state.focus_mode:
                # وضع التركيز
                st.markdown(f"""
                <div style='text-align:center; padding:40px 20px; margin:20px 0;'>
                    <div style='font-family:Amiri,serif;font-size:{st.session_state.font_size * 0.7}rem;color:#f5f0e8;line-height:3;direction:rtl'>
                        {ayah_text} ﴿{ayah_num}﴾
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                col_main, col_actions = st.columns([5, 1])
                with col_main:
                    trans_html = f"<div class='ayah-translation'>{trans_text}</div>" if trans_text and show_trans else ""
                    st.markdown(f"""
                    <div class='ayah-container'>
                        <div style='display:flex;align-items:flex-start;gap:12px'>
                            <span class='ayah-number'>{ayah_num}</span>
                            <div class='ayah-text' style='font-size:{st.session_state.font_size}rem'>
                                {ayah_text}
                            </div>
                        </div>
                        {trans_html}
                    </div>
                    """, unsafe_allow_html=True)

                with col_actions:
                    # أزرار الآية
                    audio_url = get_audio_url(surah_num, ayah_num, st.session_state.selected_sheikh)
                    st.markdown(f"""
                    <audio controls style='width:100%;margin-top:10px'>
                        <source src='{audio_url}' type='audio/mpeg'>
                    </audio>
                    """, unsafe_allow_html=True)

                    if st.button("❤️", key=f"heart_{surah_num}_{ayah_num}", help="أضف لمكتبة القلب"):
                        item = {"surah": surah_num, "ayah": ayah_num, "text": ayah_text,
                               "surah_name": surah_info.get('name',''), "mood": "", "time": datetime.now().strftime("%Y-%m-%d")}
                        if item not in st.session_state.heart_library:
                            st.session_state.heart_library.append(item)
                            st.success("❤️")

                    if show_tafseer_inline:
                        with st.expander("📚 تفسير", expanded=False):
                            st.markdown(f"""<div style='color:#a5d6a7;font-family:Cairo,sans-serif;font-size:0.85rem;direction:rtl'>
                            تفسير ميسّر للآية {ayah_num} من سورة {surah_info.get('name','')}
                            </div>""", unsafe_allow_html=True)

        # أزرار التنقل
        st.markdown("<div class='islamic-divider'>❧</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.session_state.current_surah > 1:
                if st.button("⟵ السورة السابقة", use_container_width=True):
                    st.session_state.current_surah -= 1
                    st.session_state.current_ayah = 1
                    st.rerun()
        with col2:
            if st.button("🏠 الرئيسية", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()
        with col3:
            if st.session_state.current_surah < 114:
                if st.button("السورة التالية ⟶", use_container_width=True):
                    st.session_state.current_surah += 1
                    st.session_state.current_ayah = 1
                    st.rerun()
    else:
        st.warning("⚠️ تعذّر تحميل الآيات. تأكد من اتصالك بالإنترنت.")

# ==================== صفحة الاستماع ====================
def render_audio():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>🎙️ مشغّل التلاوة</h2>""", unsafe_allow_html=True)

    # اختيار الشيخ
    st.markdown("""<p style='color:#a5d6a7;font-family:Cairo,sans-serif;direction:rtl;font-size:1rem'>🕌 اختر الشيخ:</p>""", unsafe_allow_html=True)
    sheikh_html = "<div class='sheikh-selector'>"
    for key, name in SHEIKHS.items():
        active_class = "active" if st.session_state.selected_sheikh == key else ""
        sheikh_html += f"<span class='sheikh-btn {active_class}'>{name}</span>"
    sheikh_html += "</div>"
    st.markdown(sheikh_html, unsafe_allow_html=True)

    # اختيار الشيخ من selectbox
    sheikh_names = list(SHEIKHS.values())
    sheikh_keys = list(SHEIKHS.keys())
    current_idx = sheikh_keys.index(st.session_state.selected_sheikh) if st.session_state.selected_sheikh in sheikh_keys else 0
    selected_name = st.selectbox("الشيخ", sheikh_names, index=current_idx, key="sheikh_select_audio")
    st.session_state.selected_sheikh = sheikh_keys[sheikh_names.index(selected_name)]

    st.markdown("<div class='islamic-divider'>❧</div>", unsafe_allow_html=True)

    # اختيار السورة والآية
    col1, col2 = st.columns(2)
    with col1:
        surah_options = {v['name']: k for k, v in ALL_SURAHS.items()}
        current_name = ALL_SURAHS.get(st.session_state.current_surah, {}).get('name', 'الفاتحة')
        sel_name = st.selectbox("السورة", list(surah_options.keys()),
                                 index=list(surah_options.keys()).index(current_name) if current_name in surah_options else 0,
                                 key="audio_surah")
        surah_num = surah_options[sel_name]
        st.session_state.current_surah = surah_num

    with col2:
        max_a = ALL_SURAHS.get(surah_num, {}).get('verses', 1)
        ayah_num = st.number_input("الآية", min_value=1, max_value=max_a,
                                    value=min(st.session_state.current_ayah, max_a), key="audio_ayah")
        st.session_state.current_ayah = ayah_num

    # مشغل الصوت الرئيسي
    audio_url = get_audio_url(surah_num, ayah_num, st.session_state.selected_sheikh)
    surah_info = ALL_SURAHS.get(surah_num, {})

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#0d2018,#162a1f);border:1px solid #C9A84C;border-radius:20px;padding:30px;text-align:center;margin:20px 0'>
        <div style='color:#C9A84C;font-family:Amiri,serif;font-size:2rem;margin-bottom:10px'>
            سورة {surah_info.get("name","")} — الآية {ayah_num}
        </div>
        <div style='color:#a5d6a7;font-family:Cairo,sans-serif;font-size:0.9rem;margin-bottom:20px'>
            🎤 {selected_name}
        </div>
        <audio controls style='width:80%;border-radius:50px' autoplay>
            <source src='{audio_url}' type='audio/mpeg'>
            متصفحك لا يدعم تشغيل الصوت
        </audio>
    </div>
    """, unsafe_allow_html=True)

    # زر "أثرت فيّ"
    st.markdown("""<p style='color:#a5d6a7;font-family:Cairo,sans-serif;direction:rtl;margin-top:20px'>💭 كيف أثرت فيك هذه الآية؟</p>""", unsafe_allow_html=True)
    emotions = ["🥺 أبكتني", "😌 اطمأننت", "💪 قوّت عزيمتي", "🤲 دفعتني للدعاء", "💡 فتحت لي آفاقاً", "❤️ ملأت قلبي", "😔 ذكّرتني بذنوبي", "🌟 أشعلت أملي"]
    cols = st.columns(4)
    for i, emo in enumerate(emotions):
        with cols[i % 4]:
            if st.button(emo, key=f"emo_{i}", use_container_width=True):
                # جلب نص الآية وإضافتها لمكتبة القلب
                item = {"surah": surah_num, "ayah": ayah_num,
                       "surah_name": surah_info.get('name',''), "mood": emo,
                       "time": datetime.now().strftime("%Y-%m-%d")}
                st.session_state.heart_library.append(item)
                st.success(f"✅ تم حفظ الآية في مكتبة القلب بمشاعر: {emo}")

    # تشغيل السورة كاملة
    st.markdown("<div class='islamic-divider'>❧</div>", unsafe_allow_html=True)
    st.markdown("""<h3 style='color:#C9A84C;font-family:Cairo,sans-serif;direction:rtl'>▶ تشغيل السورة كاملة</h3>""", unsafe_allow_html=True)

    # رابط السورة كاملة من Islamic Network
    reciter_id = st.session_state.selected_sheikh.replace("ar.", "")
    full_surah_url = f"https://cdn.islamic.network/quran/audio-surah/128/{reciter_id}/{surah_num}.mp3"
    st.markdown(f"""
    <audio controls style='width:100%;border-radius:50px;margin:10px 0'>
        <source src='{full_surah_url}' type='audio/mpeg'>
    </audio>
    """, unsafe_allow_html=True)

# ==================== صفحة تصحيح التلاوة ====================
def render_tajweed():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>🧠 تصحيح التلاوة بالذكاء الاصطناعي</h2>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='notification'>
        🎯 <strong>كيف يعمل هذا الذكاء؟</strong><br>
        اكتب الآية التي تريد تتدرب عليها، ثم اكتب ما قرأته (بالشكل الذي نطقته) وسيحلل الذكاء الاصطناعي أخطاءك في التجويد ومخارج الحروف والمد والغنة وغيرها.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<p style='color:#C9A84C;font-family:Cairo,sans-serif;direction:rtl'>📖 الآية الصحيحة:</p>""", unsafe_allow_html=True)
        correct_ayah = st.text_area("الآية الصحيحة", placeholder="اكتب أو الصق الآية هنا...",
                                     height=120, key="correct_text",
                                     value="إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ")
    with col2:
        st.markdown("""<p style='color:#C9A84C;font-family:Cairo,sans-serif;direction:rtl'>🎤 ما قرأتَه (بدون تشكيل):</p>""", unsafe_allow_html=True)
        user_reading = st.text_area("ما قرأته", placeholder="اكتب ما قرأته...",
                                     height=120, key="user_text",
                                     value="انا اعطيناك الكوثر")

    col1, col2 = st.columns(2)
    with col1:
        tajweed_level = st.selectbox("مستواك في التجويد", ["مبتدئ", "متوسط", "متقدم"], key="tajweed_level")
    with col2:
        check_types = st.multiselect("ما الذي تريد فحصه؟",
                                      ["أحكام النون الساكنة", "المدود", "الوقف والابتداء", "مخارج الحروف", "الصفات", "التشكيل والضبط"],
                                      default=["أحكام النون الساكنة", "المدود", "مخارج الحروف"],
                                      key="check_types")

    if st.button("🔍 حلّل تلاوتي", use_container_width=True, type="primary", key="analyze_btn"):
        if correct_ayah and user_reading:
            with st.spinner("🧠 جارٍ التحليل بالذكاء الاصطناعي..."):
                prompt = f"""أنت معلم قرآن كريم خبير في علم التجويد. حلّل القراءة التالية وأعطِ تصحيحاً تفصيلياً.

المستوى: {tajweed_level}
الجوانب المطلوب فحصها: {', '.join(check_types)}

الآية الصحيحة: {correct_ayah}
ما قرأه المتعلم: {user_reading}

قدّم تحليلاً شاملاً يتضمن:
1. ✅ الصحيح في قراءته
2. ❌ الأخطاء مع شرح سبب الخطأ
3. 🔊 كيفية النطق الصحيح
4. 📚 القاعدة التجويدية المتعلقة بالخطأ
5. 💡 نصائح للتحسين
6. ⭐ تقييم عام من 10

قدّم الإجابة بالعربية وبأسلوب تشجيعي مع رموز واضحة."""

                try:
                    response = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={"Content-Type": "application/json"},
                        json={"model": "claude-sonnet-4-6", "max_tokens": 1000,
                              "messages": [{"role": "user", "content": prompt}]},
                        timeout=30
                    )
                    if response.status_code == 200:
                        result = response.json()['content'][0]['text']
                        st.markdown(f"""
                        <div class='hadith-card' style='margin-top:20px'>
                            <div style='color:#C9A84C;font-family:Cairo,sans-serif;font-size:1.1rem;margin-bottom:15px;direction:rtl'>
                                🧠 نتيجة التحليل التجويدي
                            </div>
                            <div style='color:#e8f5e9;font-family:Cairo,sans-serif;direction:rtl;line-height:2;white-space:pre-wrap'>
                                {result}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("⚠️ حدث خطأ في الاتصال بالذكاء الاصطناعي")
                except Exception as e:
                    st.error(f"خطأ: {e}")
        else:
            st.warning("⚠️ يرجى إدخال الآية وما قرأته")

    # قائمة أحكام التجويد
    st.markdown("<div class='islamic-divider'>❧</div>", unsafe_allow_html=True)
    st.markdown("""<h3 style='color:#C9A84C;font-family:Cairo,sans-serif;direction:rtl'>📚 أحكام التجويد الأساسية</h3>""", unsafe_allow_html=True)

    tajweed_rules = [
        ("الإظهار الحلقي", "إذا جاءت النون الساكنة أو التنوين قبل حروف الحلق (ء ه ع ح غ خ) تُقرأ بوضوح بدون غنة", "#C9A84C"),
        ("الإدغام", "إذا جاءت النون الساكنة أو التنوين قبل (ي ر م ل و ن) تُدغم فيها", "#52b788"),
        ("الإقلاب", "إذا جاءت النون الساكنة أو التنوين قبل الباء تُقلب إلى ميم مخفاة", "#a0c4ff"),
        ("الإخفاء الحقيقي", "إذا جاءت النون الساكنة أو التنوين قبل 15 حرفاً تُخفى مع الغنة", "#ffb347"),
        ("المد الطبيعي", "مدّ حرف المد بمقدار حركتين طبيعيتين", "#C9A84C"),
        ("المد المتصل", "حرف المد وبعده همزة في كلمة واحدة، يمد 4-5 حركات", "#52b788"),
    ]

    cols = st.columns(2)
    for i, (rule, explanation, color) in enumerate(tajweed_rules):
        with cols[i % 2]:
            st.markdown(f"""
            <div class='ayah-container' style='margin:8px 0'>
                <div style='color:{color};font-family:Amiri,serif;font-size:1.2rem;margin-bottom:8px'>{rule}</div>
                <div style='color:#a5d6a7;font-family:Cairo,sans-serif;font-size:0.85rem'>{explanation}</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== خريطة القصص القرآنية ====================
def render_mindmap():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>🗺️ خريطة القصص القرآنية التفاعلية</h2>""", unsafe_allow_html=True)

    stories = {
        "قصة سيدنا موسى": {
            "icon": "🌊",
            "color": "#52b788",
            "stages": [
                {"stage": "الميلاد والإلقاء في النهر", "surahs": ["طه:38-39", "القصص:7-8"], "lesson": "توكّل الأم على الله"},
                {"stage": "في قصر فرعون", "surahs": ["القصص:9-13", "طه:40"], "lesson": "حفظ الله لأوليائه"},
                {"stage": "قتل القبطي والفرار", "surahs": ["القصص:15-21"], "lesson": "التوبة والاستغفار"},
                {"stage": "في مدين والزواج", "surahs": ["القصص:22-28"], "lesson": "الأمانة والعمل"},
                {"stage": "الرسالة والعصا", "surahs": ["طه:9-24", "النمل:7-12"], "lesson": "الثقة بالله"},
                {"stage": "مواجهة فرعون", "surahs": ["طه:43-76", "الشعراء:16-51"], "lesson": "الشجاعة في الحق"},
                {"stage": "عبور البحر", "surahs": ["البقرة:50", "الشعراء:63-68"], "lesson": "النجاة بالإيمان"},
                {"stage": "ألواح التوراة", "surahs": ["الأعراف:144-154"], "lesson": "شرف الحكمة الإلهية"},
            ]
        },
        "قصة سيدنا يوسف": {
            "icon": "⭐",
            "color": "#C9A84C",
            "stages": [
                {"stage": "الرؤيا وغيرة الإخوة", "surahs": ["يوسف:4-5"], "lesson": "الصبر والكتمان"},
                {"stage": "الإلقاء في البئر", "surahs": ["يوسف:9-18"], "lesson": "الحسد وعواقبه"},
                {"stage": "في مصر وإغراء امرأة العزيز", "surahs": ["يوسف:21-29"], "lesson": "العفة والاستعاذة"},
                {"stage": "السجن والتعبير", "surahs": ["يوسف:36-42"], "lesson": "الدعوة في المحن"},
                {"stage": "تفسير رؤيا الملك", "surahs": ["يوسف:43-49"], "lesson": "العلم نعمة"},
                {"stage": "التمكين في الأرض", "surahs": ["يوسف:54-57"], "lesson": "الكفاءة والأمانة"},
                {"stage": "لقاء الإخوة وعودة البيت", "surahs": ["يوسف:58-93"], "lesson": "العفو والتسامح"},
                {"stage": "لم الشمل واجتماع الأسرة", "surahs": ["يوسف:94-101"], "lesson": "الجزاء الحسن"},
            ]
        },
        "قصة سيدنا إبراهيم": {
            "icon": "🔥",
            "color": "#ff7043",
            "stages": [
                {"stage": "الدعوة لأبيه وقومه", "surahs": ["الأنعام:74-83", "مريم:41-48"], "lesson": "الصدق مع الوالدين"},
                {"stage": "كسر الأصنام", "surahs": ["الأنبياء:51-67"], "lesson": "الشجاعة في نشر الحق"},
                {"stage": "النار والنجاة", "surahs": ["الأنبياء:68-70", "العنكبوت:24"], "lesson": "النار برد وسلام"},
                {"stage": "الهجرة وبناء الكعبة", "surahs": ["إبراهيم:35-41", "البقرة:127"], "lesson": "إحياء شعائر الله"},
                {"stage": "ذبح الولد", "surahs": ["الصافات:100-113"], "lesson": "الفداء والطاعة الكاملة"},
            ]
        },
    }

    selected_story = st.selectbox("اختر قصة نبي",
                                   list(stories.keys()), key="story_select")

    story = stories[selected_story]

    st.markdown(f"""
    <div style='text-align:center;padding:25px;background:linear-gradient(135deg,#080f0a,#0d2018);border:2px solid {story["color"]};border-radius:20px;margin:15px 0'>
        <div style='font-size:3rem'>{story["icon"]}</div>
        <div style='color:{story["color"]};font-family:Amiri,serif;font-size:2rem;margin-top:10px'>{selected_story}</div>
        <div style='color:#a5d6a7;font-family:Cairo,sans-serif;font-size:0.9rem;margin-top:5px'>اضغط على أي مرحلة لمعرفة التفاصيل</div>
    </div>
    """, unsafe_allow_html=True)

    # عرض المراحل كخريطة تسلسلية
    for i, stage_data in enumerate(story["stages"]):
        col1, col2, col3 = st.columns([1, 6, 3])
        with col1:
            st.markdown(f"""
            <div style='text-align:center;padding:15px 0'>
                <div style='background:{story["color"]};color:#0a1a0f;width:35px;height:35px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:Amiri,serif;font-weight:700;font-size:1rem;margin:auto'>{i+1}</div>
                <div style='width:2px;height:40px;background:linear-gradient({story["color"]},transparent);margin:5px auto'></div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            with st.expander(f"📍 {stage_data['stage']}", expanded=False):
                surahs_text = " | ".join([f"📖 {s}" for s in stage_data['surahs']])
                st.markdown(f"""
                <div style='direction:rtl;padding:10px'>
                    <div style='color:{story["color"]};font-family:Cairo,sans-serif;font-size:0.9rem;margin-bottom:8px'>{surahs_text}</div>
                    <div style='color:#f5f0e8;font-family:Cairo,sans-serif;font-size:0.95rem'>💎 الدرس المستفاد: {stage_data["lesson"]}</div>
                </div>
                """, unsafe_allow_html=True)
        with col3:
            if st.button(f"📖 اقرأ الآيات", key=f"read_{selected_story}_{i}", use_container_width=True):
                st.info(f"🔗 الآيات: {', '.join(stage_data['surahs'])}")

    # زر طلب تفاصيل بالذكاء الاصطناعي
    if st.button("🤖 اشرح لي القصة بالتفصيل مع الذكاء الاصطناعي", use_container_width=True, type="primary", key="ai_story"):
        with st.spinner("جارٍ إعداد التفسير..."):
            prompt = f"""اشرح {selected_story} من القرآن الكريم بأسلوب تفاعلي جذاب يتضمن:
1. مقدمة عن شخصية النبي
2. الدروس والعبر من كل مرحلة
3. العلاقة بحياتنا اليوم
4. أبرز الآيات

كن مختصراً ومشوّقاً بالعربية."""
            try:
                response = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"Content-Type": "application/json"},
                    json={"model": "claude-sonnet-4-6", "max_tokens": 1000,
                          "messages": [{"role": "user", "content": prompt}]},
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()['content'][0]['text']
                    st.markdown(f"""
                    <div class='hadith-card'>
                        <div class='hadith-text' style='font-size:1rem;color:#e8f5e9'>{result}</div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"خطأ: {e}")

# ==================== صفحة الحالة الوجدانية ====================
def render_mood():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>💭 القرآن بحسب حالتي</h2>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center;padding:20px;direction:rtl'>
        <p style='color:#a5d6a7;font-family:Cairo,sans-serif;font-size:1rem'>
            أخبرني كيف تشعر الآن، وسأختار لك الآيات الأنسب لحالتك ✨
        </p>
    </div>
    """, unsafe_allow_html=True)

    # شبكة المشاعر
    mood_emojis = {
        "حزن وضيق": "😢", "فرح وشكر": "😊", "خوف وقلق": "😰", "توبة وندم": "🥺",
        "تأمل وتدبر": "🤔", "قبل النوم": "🌙", "صباح جديد": "🌅", "في المصيبة": "💔",
        "طلب الرزق": "🤲", "شفاء المريض": "🏥"
    }

    st.markdown("""<h3 style='color:#a5d6a7;font-family:Cairo,sans-serif;direction:rtl;text-align:right'>كيف تشعر الآن؟</h3>""", unsafe_allow_html=True)

    cols = st.columns(5)
    selected_mood = st.session_state.get('listening_mood')
    for i, (mood, emoji) in enumerate(mood_emojis.items()):
        with cols[i % 5]:
            is_selected = selected_mood == mood
            btn_color = "background:linear-gradient(135deg,#C9A84C,#a07830);color:#0a1a0f;" if is_selected else ""
            if st.button(f"{emoji}\n{mood}", key=f"mood_{mood}", use_container_width=True):
                st.session_state.listening_mood = mood
                st.rerun()

    if st.session_state.listening_mood:
        mood = st.session_state.listening_mood
        emoji = mood_emojis.get(mood, "💚")
        surahs = MOODS.get(mood, [1, 2])

        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#0d2018,#162a1f);border:1px solid #C9A84C;border-radius:16px;padding:25px;margin:20px 0;text-align:center;direction:rtl'>
            <div style='font-size:2rem'>{emoji}</div>
            <div style='color:#C9A84C;font-family:Cairo,sans-serif;font-size:1.2rem;font-weight:700;margin:10px 0'>
                إليك آيات مخصوصة لـ "{mood}"
            </div>
        </div>
        """, unsafe_allow_html=True)

        for surah_num in surahs:
            surah_info = ALL_SURAHS.get(surah_num, {})
            if surah_info:
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"""
                    <div class='surah-card'>
                        <div class='surah-info'>
                            <h4>سورة {surah_info["name"]}</h4>
                            <small>{surah_info["verses"]} آية • {surah_info["type"]}</small>
                        </div>
                        <div class='surah-number-badge'>{surah_num}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("▶ اقرأ", key=f"mood_read_{surah_num}", use_container_width=True):
                        st.session_state.current_surah = surah_num
                        st.session_state.current_ayah = 1
                        st.session_state.page = "mushaf"
                        st.rerun()

        # اقتراح بالذكاء الاصطناعي
        if st.button("🤖 ابحث لي عن المزيد بالذكاء الاصطناعي", use_container_width=True, key="ai_mood"):
            with st.spinner("جارٍ البحث..."):
                prompt = f"""أنا أشعر بـ "{mood}". اقترح لي 5 آيات قرآنية مختارة بعناية مع:
- نص الآية
- اسم السورة ورقمها
- سبب اختيارها لهذه الحالة
- كلمة تشجيع قصيرة

بالعربية وبأسلوب دافئ ومحبب."""
                try:
                    response = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={"Content-Type": "application/json"},
                        json={"model": "claude-sonnet-4-6", "max_tokens": 1000,
                              "messages": [{"role": "user", "content": prompt}]},
                        timeout=30
                    )
                    if response.status_code == 200:
                        result = response.json()['content'][0]['text']
                        st.markdown(f"""
                        <div class='hadith-card'>
                            <div class='hadith-text' style='font-size:1rem;color:#e8f5e9'>{result}</div>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"خطأ: {e}")

# ==================== صفحة التفسير ====================
def render_tafseer():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>📚 التفسير والتدبر</h2>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📖 التفسير الميسّر", "📅 سبب النزول", "🔗 المتشابهات اللفظية", "💎 التدبر والفوائد"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            surah_options = {v['name']: k for k, v in ALL_SURAHS.items()}
            current_name = ALL_SURAHS.get(st.session_state.current_surah, {}).get('name', 'الفاتحة')
            sel = st.selectbox("السورة", list(surah_options.keys()),
                               index=list(surah_options.keys()).index(current_name) if current_name in surah_options else 0,
                               key="tafseer_surah")
            surah_num = surah_options[sel]
        with col2:
            max_a = ALL_SURAHS.get(surah_num, {}).get('verses', 1)
            ayah_num = st.number_input("الآية", min_value=1, max_value=max_a, value=1, key="tafseer_ayah")

        if st.button("📖 اعرض التفسير", use_container_width=True, type="primary", key="show_tafseer_btn"):
            with st.spinner("جارٍ جلب التفسير..."):
                prompt = f"""فسّر الآية {ayah_num} من سورة {sel} بشكل شامل يتضمن:
1. 📝 التفسير الميسّر (بأسلوب واضح)
2. 🔤 معاني المفردات الصعبة
3. 💎 الفوائد والدروس المستفادة
4. 🌟 وجوه الإعجاز في الآية

بالعربية الفصيحة المفهومة."""
                try:
                    response = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={"Content-Type": "application/json"},
                        json={"model": "claude-sonnet-4-6", "max_tokens": 1000,
                              "messages": [{"role": "user", "content": prompt}]},
                        timeout=30
                    )
                    if response.status_code == 200:
                        result = response.json()['content'][0]['text']
                        st.markdown(f"""
                        <div class='hadith-card'>
                            <div style='color:#C9A84C;font-family:Cairo,sans-serif;font-size:1rem;margin-bottom:15px;direction:rtl'>
                                📖 تفسير الآية {ayah_num} من سورة {sel}
                            </div>
                            <div class='hadith-text' style='font-size:1rem;color:#e8f5e9'>{result}</div>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"خطأ: {e}")

    with tab2:
        st.markdown("""<p style='color:#a5d6a7;font-family:Cairo,sans-serif;direction:rtl'>اكتب اسم السورة أو الموضوع للبحث عن سبب النزول:</p>""", unsafe_allow_html=True)
        query = st.text_input("موضوع البحث", placeholder="مثال: سورة الكهف، آية الكرسي، سورة العلق...", key="revelation_query")
        if st.button("🔍 ابحث عن سبب النزول", key="revelation_btn", use_container_width=True):
            if query:
                with st.spinner("جارٍ البحث..."):
                    prompt = f"""أخبرني عن سبب نزول: {query}
                    
اذكر:
1. سبب النزول التفصيلي
2. الحادثة أو الموقف الذي نزلت فيه الآية
3. الدلالة والحكمة من نزولها في هذا السياق
4. المصدر (الصحيح من الروايات)

بالعربية."""
                    try:
                        response = requests.post(
                            "https://api.anthropic.com/v1/messages",
                            headers={"Content-Type": "application/json"},
                            json={"model": "claude-sonnet-4-6", "max_tokens": 1000,
                                  "messages": [{"role": "user", "content": prompt}]},
                            timeout=30
                        )
                        if response.status_code == 200:
                            result = response.json()['content'][0]['text']
                            st.markdown(f"""
                            <div class='hadith-card'>
                                <div class='hadith-text' style='font-size:1rem;color:#e8f5e9'>{result}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"خطأ: {e}")

    with tab3:
        st.markdown("""<p style='color:#a5d6a7;font-family:Cairo,sans-serif;direction:rtl'>ابحث عن الآيات المتشابهة لفظياً:</p>""", unsafe_allow_html=True)
        search_word = st.text_input("كلمة أو عبارة", placeholder="مثال: الصبر، الرزق، التوكل...", key="similar_query")
        if st.button("🔗 ابحث عن المتشابهات", key="similar_btn", use_container_width=True):
            if search_word:
                with st.spinner("جارٍ البحث..."):
                    prompt = f"""ابحث في القرآن الكريم عن الآيات التي تتشابه في ذكر "{search_word}".

اذكر:
1. الآيات التي تذكر هذه الكلمة أو المعنى
2. السياق المختلف لكل آية
3. الفروق الدقيقة بين الآيات المتشابهة
4. الحكمة من تكرارها

بالعربية مع ذكر اسم السورة ورقم الآية."""
                    try:
                        response = requests.post(
                            "https://api.anthropic.com/v1/messages",
                            headers={"Content-Type": "application/json"},
                            json={"model": "claude-sonnet-4-6", "max_tokens": 1000,
                                  "messages": [{"role": "user", "content": prompt}]},
                            timeout=30
                        )
                        if response.status_code == 200:
                            result = response.json()['content'][0]['text']
                            st.markdown(f"""
                            <div class='hadith-card'>
                                <div class='hadith-text' style='font-size:1rem;color:#e8f5e9'>{result}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"خطأ: {e}")

    with tab4:
        st.markdown("""<p style='color:#a5d6a7;font-family:Cairo,sans-serif;direction:rtl'>اكتب موضوعاً أو آية وسيعطيك الذكاء الاصطناعي تدبراً عميقاً:</p>""", unsafe_allow_html=True)
        tadabbur_query = st.text_area("موضوع التدبر أو الآية", placeholder="مثال: ﴿وَعَسَى أَن تَكْرَهُوا شَيْئاً وَهُوَ خَيْرٌ لَّكُمْ﴾", height=100, key="tadabbur_q")
        if st.button("💎 تدبّر معي", key="tadabbur_btn", use_container_width=True, type="primary"):
            if tadabbur_query:
                with st.spinner("جارٍ التدبر..."):
                    prompt = f"""تدبّر معي هذه الآية أو الموضوع القرآني: {tadabbur_query}

قدّم:
1. 🌊 فيض التدبر (أعمق ما في الآية)
2. 💡 كيف تطبّق هذه الآية في حياتك اليومية
3. 🔭 النظرة الكونية التي تفتحها
4. ❓ سؤال للتفكير والتأمل

بأسلوب روحاني مؤثر يلمس القلب."""
                    try:
                        response = requests.post(
                            "https://api.anthropic.com/v1/messages",
                            headers={"Content-Type": "application/json"},
                            json={"model": "claude-sonnet-4-6", "max_tokens": 1000,
                                  "messages": [{"role": "user", "content": prompt}]},
                            timeout=30
                        )
                        if response.status_code == 200:
                            result = response.json()['content'][0]['text']
                            st.markdown(f"""
                            <div class='dhikr-card'>
                                <div class='hadith-text' style='font-size:1rem;color:#e8f5e9;text-align:right'>{result}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"خطأ: {e}")

# ==================== البحث بالمقاصد ====================
def render_search():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>🔍 البحث بالمقاصد والمعاني</h2>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='notification'>
        💡 <strong>البحث الذكي:</strong> لا تحتاج لمعرفة النص الحرفي. ابحث بالمعنى مثلاً: "آيات عن الصبر في الشدة" أو "آيات الرزق والعمل"
    </div>
    """, unsafe_allow_html=True)

    search_query = st.text_input("ابحث بأي كلمة أو معنى أو موضوع",
                                  placeholder="مثال: التوكل على الله، بر الوالدين، الصدق في المعاملة...",
                                  key="main_search")

    col1, col2 = st.columns(2)
    with col1:
        search_type = st.selectbox("نوع البحث", ["بحث معنوي (بالمقاصد)", "بحث نصي (بالكلمة)", "بحث موضوعي"], key="search_type")
    with col2:
        result_count = st.slider("عدد النتائج", 3, 15, 5, key="result_count")

    if st.button("🔍 ابحث", use_container_width=True, type="primary", key="do_search"):
        if search_query:
            with st.spinner("جارٍ البحث في القرآن الكريم..."):
                prompt = f"""أنت محرك بحث قرآني ذكي. ابحث في القرآن الكريم عن: "{search_query}"
نوع البحث: {search_type}

أعطِ {result_count} آيات مناسبة مع:
- نص الآية كاملاً بالتشكيل
- اسم السورة ورقم الآية
- شرح مختصر لعلاقتها بالبحث
- سياق الآية

رتّبها من الأكثر صلة للأقل."""
                try:
                    response = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={"Content-Type": "application/json"},
                        json={"model": "claude-sonnet-4-6", "max_tokens": 1000,
                              "messages": [{"role": "user", "content": prompt}]},
                        timeout=30
                    )
                    if response.status_code == 200:
                        result = response.json()['content'][0]['text']
                        st.markdown(f"""
                        <div class='hadith-card'>
                            <div style='color:#C9A84C;font-family:Cairo,sans-serif;margin-bottom:15px;direction:rtl'>
                                🔍 نتائج البحث عن: {search_query}
                            </div>
                            <div class='hadith-text' style='font-size:1rem;color:#e8f5e9'>{result}</div>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"خطأ: {e}")

    # بحث سريع
    st.markdown("<div class='islamic-divider'>❧</div>", unsafe_allow_html=True)
    st.markdown("""<h3 style='color:#a5d6a7;font-family:Cairo,sans-serif;direction:rtl'>🚀 بحث سريع</h3>""", unsafe_allow_html=True)
    quick_searches = ["آيات الصبر", "فضل العلم", "بر الوالدين", "التوبة والمغفرة", "رزق الله الواسع", "الأمل والتفاؤل", "أسماء الله الحسنى", "يوم القيامة"]
    cols = st.columns(4)
    for i, qs in enumerate(quick_searches):
        with cols[i % 4]:
            if st.button(qs, key=f"qs_{i}", use_container_width=True):
                st.session_state['quick_search'] = qs
                st.rerun()

# ==================== المساعد الذكي ====================
def render_ai_assistant():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>🤖 المساعد القرآني الذكي</h2>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='notification'>
        🌟 <strong>اسألني أي شيء:</strong> تفسير، تجويد، أسئلة دينية، معلومات قرآنية، أحكام شرعية، قصص الأنبياء، وأكثر...
    </div>
    """, unsafe_allow_html=True)

    # عرض تاريخ المحادثة
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f"""
            <div style='display:flex;justify-content:flex-end;margin:10px 0'>
                <div class='user-message'>
                    <div class='message-text'>{msg['content']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='display:flex;justify-content:flex-start;margin:10px 0'>
                <div class='ai-message'>
                    <div style='color:#C9A84C;font-family:Cairo,sans-serif;font-size:0.8rem;margin-bottom:5px'>🤖 المساعد القرآني</div>
                    <div class='message-text'>{msg['content']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # اقتراحات أسئلة
    if not st.session_state.chat_history:
        st.markdown("""<h3 style='color:#a5d6a7;font-family:Cairo,sans-serif;direction:rtl;margin-top:20px'>💡 أسئلة مقترحة:</h3>""", unsafe_allow_html=True)
        suggestions = [
            "ما هي أفضل آيات للقراءة قبل النوم؟",
            "اشرح لي أركان الصلاة",
            "ما الفرق بين الجزء والحزب والربع؟",
            "كيف أحفظ القرآن بسرعة؟",
            "ما معنى البسملة؟",
            "اذكر لي أسماء الله الحسنى مع معانيها",
        ]
        cols = st.columns(2)
        for i, sug in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(sug, key=f"sug_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": sug})
                    with st.spinner("جارٍ التفكير..."):
                        try:
                            response = requests.post(
                                "https://api.anthropic.com/v1/messages",
                                headers={"Content-Type": "application/json"},
                                json={"model": "claude-sonnet-4-6", "max_tokens": 1000,
                                      "system": "أنت مساعد قرآني إسلامي متخصص. أجب باللغة العربية الفصيحة المفهومة. قدّم إجابات دقيقة ومفيدة تستند للقرآن الكريم والسنة النبوية الصحيحة.",
                                      "messages": st.session_state.chat_history},
                                timeout=30
                            )
                            if response.status_code == 200:
                                reply = response.json()['content'][0]['text']
                                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                                st.rerun()
                        except Exception as e:
                            st.error(f"خطأ: {e}")

    # مربع الإدخال
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("اكتب سؤالك هنا...", placeholder="أي سؤال عن القرآن أو الإسلام...", key="ai_input")
    with col2:
        send_btn = st.button("إرسال ✉️", key="send_ai", use_container_width=True, type="primary")

    if send_btn and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("🤖 جارٍ التفكير..."):
            try:
                messages_to_send = st.session_state.chat_history[-10:]  # آخر 10 رسائل
                response = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"Content-Type": "application/json"},
                    json={"model": "claude-sonnet-4-6", "max_tokens": 1000,
                          "system": "أنت مساعد قرآني إسلامي متخصص ذو علم واسع. أجب باللغة العربية الفصيحة المفهومة. قدّم إجابات دقيقة ومفيدة تستند للقرآن الكريم والسنة النبوية الصحيحة. كن ودوداً ومشجعاً.",
                          "messages": messages_to_send},
                    timeout=30
                )
                if response.status_code == 200:
                    reply = response.json()['content'][0]['text']
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.rerun()
            except Exception as e:
                st.error(f"خطأ: {e}")

    if st.session_state.chat_history:
        if st.button("🗑️ مسح المحادثة", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

# ==================== مكتبة القلب ====================
def render_heart():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>❤️ مكتبة القلب</h2>""", unsafe_allow_html=True)

    if not st.session_state.heart_library:
        st.markdown("""
        <div style='text-align:center;padding:60px 20px;direction:rtl'>
            <div style='font-size:4rem'>❤️</div>
            <div style='color:#a5d6a7;font-family:Cairo,sans-serif;font-size:1rem;margin-top:15px'>
                مكتبة القلب فارغة<br>
                أضف الآيات التي تؤثر فيك من المصحف أو مشغل الصوت
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""<p style='color:#a5d6a7;font-family:Cairo,sans-serif;direction:rtl'>{len(st.session_state.heart_library)} آية في مكتبة قلبك</p>""", unsafe_allow_html=True)

        for i, item in enumerate(st.session_state.heart_library):
            col1, col2 = st.columns([5, 1])
            with col1:
                mood_text = f"<div style='display:inline-block;background:rgba(201,168,76,0.15);border:1px solid rgba(201,168,76,0.3);border-radius:20px;padding:3px 12px;color:#C9A84C;font-family:Cairo,sans-serif;font-size:0.8rem;margin-top:8px'>{item.get('mood','')}</div>" if item.get('mood') else ""
                st.markdown(f"""
                <div class='ayah-container'>
                    <div style='color:#C9A84C;font-family:Cairo,sans-serif;font-size:0.85rem;margin-bottom:8px'>
                        📖 سورة {item.get("surah_name","")} — الآية {item.get("ayah","")}
                    </div>
                    <div style='color:#f5f0e8;font-family:Amiri,serif;font-size:1.5rem;direction:rtl;line-height:2'>
                        {item.get("text","الآية")}
                    </div>
                    {mood_text}
                    <div style='color:#4a7a5a;font-family:Cairo,sans-serif;font-size:0.75rem;margin-top:8px'>{item.get("time","")}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"del_heart_{i}", help="حذف"):
                    st.session_state.heart_library.pop(i)
                    st.rerun()
                audio_url = get_audio_url(item.get("surah",1), item.get("ayah",1))
                st.markdown(f"""<audio controls style='width:100%;margin-top:5px'><source src='{audio_url}' type='audio/mpeg'></audio>""", unsafe_allow_html=True)

# ==================== الإشارات المرجعية ====================
def render_bookmarks():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>🔖 الإشارات المرجعية</h2>""", unsafe_allow_html=True)

    if not st.session_state.bookmarks:
        st.markdown("""
        <div style='text-align:center;padding:60px;direction:rtl'>
            <div style='font-size:3rem'>🔖</div>
            <div style='color:#a5d6a7;font-family:Cairo,sans-serif;margin-top:15px'>لا توجد إشارات مرجعية بعد. أضفها أثناء القراءة!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, bm in enumerate(st.session_state.bookmarks):
            col1, col2, col3 = st.columns([4, 2, 1])
            with col1:
                st.markdown(f"""
                <div class='surah-card'>
                    <div class='surah-info'>
                        <h4>سورة {bm.get("surah_name","")} — الآية {bm.get("ayah","")}</h4>
                        <small>⏰ {bm.get("time","")}</small>
                    </div>
                    <div class='surah-number-badge'>{bm.get("surah","")}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("📖 اذهب للآية", key=f"goto_bm_{i}", use_container_width=True):
                    st.session_state.current_surah = bm.get("surah", 1)
                    st.session_state.current_ayah = bm.get("ayah", 1)
                    st.session_state.page = "mushaf"
                    st.rerun()
            with col3:
                if st.button("🗑️", key=f"del_bm_{i}", help="حذف"):
                    st.session_state.bookmarks.pop(i)
                    st.rerun()

# ==================== الختمة ====================
def render_khatma():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>📿 الختمة القرآنية</h2>""", unsafe_allow_html=True)

    completed = sum(st.session_state.khatma_progress)
    percentage = (completed / 114) * 100

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#0d2018,#162a1f);border:1px solid #C9A84C;border-radius:16px;padding:25px;text-align:center;margin-bottom:20px'>
        <div style='color:#C9A84C;font-family:Amiri,serif;font-size:3rem;font-weight:700'>{completed}/114</div>
        <div style='color:#a5d6a7;font-family:Cairo,sans-serif;font-size:0.9rem;margin:8px 0'>سورة أتممت قراءتها</div>
        <div class='progress-bar' style='margin:15px 0'>
            <div class='progress-fill' style='width:{percentage:.1f}%'></div>
        </div>
        <div style='color:#C9A84C;font-family:Cairo,sans-serif'>{percentage:.1f}% من الختمة</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<h3 style='color:#a5d6a7;font-family:Cairo,sans-serif;direction:rtl'>اضغط على السورة لتحديد حالتها:</h3>""", unsafe_allow_html=True)

    # شبكة السور
    cols_per_row = 6
    surah_list = list(ALL_SURAHS.items())

    for row_start in range(0, 114, cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = row_start + j
            if idx < 114:
                surah_num, surah_info = surah_list[idx] if idx < len(surah_list) else (idx+1, {"name": f"سورة {idx+1}"})
                with cols[j]:
                    is_done = st.session_state.khatma_progress[idx] if idx < len(st.session_state.khatma_progress) else False
                    btn_text = f"✅ {surah_info['name']}" if is_done else surah_info['name']
                    btn_type = "primary" if is_done else "secondary"
                    if st.button(btn_text, key=f"khatma_{idx}", use_container_width=True,
                                  help=f"سورة {surah_info['name']} - {surah_info.get('verses','?')} آية"):
                        st.session_state.khatma_progress[idx] = not st.session_state.khatma_progress[idx]
                        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ علّم الكل كمكتمل", use_container_width=True, key="mark_all"):
            st.session_state.khatma_progress = [True] * 114
            st.rerun()
    with col2:
        if st.button("🔄 إعادة ضبط الختمة", use_container_width=True, key="reset_khatma"):
            st.session_state.khatma_progress = [False] * 114
            st.rerun()

# ==================== الأذكار ====================
def render_dhikr():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>🌙 الأذكار والأدعية</h2>""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🌅 أذكار الصباح", "🌙 أذكار المساء", "💤 أذكار النوم"])

    morning_dhikr = [
        {"text": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ", "count": 1, "benefit": "ذكر الصباح الجامع"},
        {"text": "اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ", "count": 1, "benefit": "تفويض الأمر لله"},
        {"text": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "count": 100, "benefit": "تُمحى به الخطايا وإن كانت مثل زبد البحر"},
        {"text": "لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ", "count": 10, "benefit": "كمن أعتق 4 أنفس من ولد إسماعيل"},
        {"text": "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَٰهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ", "count": 1, "benefit": "سيد الاستغفار - من قاله موقناً ومات من يومه دخل الجنة"},
        {"text": "أَعُوذُ بِاللَّهِ مِنَ الشَّيْطَانِ الرَّجِيمِ — آيَةُ الْكُرْسِيِّ", "count": 1, "benefit": "من قالها عند الصباح لم يزل في حفظ الله حتى يمسي"},
    ]

    evening_dhikr = [
        {"text": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ", "count": 1, "benefit": "ذكر المساء الجامع"},
        {"text": "اللَّهُمَّ إِنِّي أَمْسَيْتُ أُشْهِدُكَ وَأُشْهِدُ حَمَلَةَ عَرْشِكَ وَمَلَائِكَتَكَ وَجَمِيعَ خَلْقِكَ، أَنَّكَ أَنْتَ اللَّهُ لَا إِلَٰهَ إِلَّا أَنْتَ وَأَنَّ مُحَمَّداً عَبْدُكَ وَرَسُولُكَ", "count": 4, "benefit": "أعتق الله ربعه من النار"},
        {"text": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ عَدَدَ خَلْقِهِ وَرِضَا نَفْسِهِ وَزِنَةَ عَرْشِهِ وَمِدَادَ كَلِمَاتِهِ", "count": 3, "benefit": "أفضل التسبيح"},
        {"text": "اللَّهُمَّ عَافِنِي فِي بَدَنِي، اللَّهُمَّ عَافِنِي فِي سَمْعِي، اللَّهُمَّ عَافِنِي فِي بَصَرِي، لَا إِلَٰهَ إِلَّا أَنْتَ", "count": 3, "benefit": "دعاء العافية في الجسد"},
    ]

    sleep_dhikr = [
        {"text": "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا", "count": 1, "benefit": "ذكر النوم"},
        {"text": "اللَّهُمَّ قِنِي عَذَابَكَ يَوْمَ تَبْعَثُ عِبَادَكَ", "count": 3, "benefit": "الحفظ من عذاب يوم القيامة"},
        {"text": "سُبْحَانَ اللَّهِ — الحمد لله — الله أكبر", "count": 33, "benefit": "خير من خادم - قاله النبي لفاطمة"},
        {"text": "آيَةُ الْكُرْسِيِّ", "count": 1, "benefit": "حفظ الله ليله ولا يقربه شيطان حتى يصبح"},
        {"text": "قُلْ هُوَ اللَّهُ أَحَدٌ — الفلق — الناس", "count": 3, "benefit": "كفته من كل شيء"},
    ]

    dhikr_tabs = {"🌅 أذكار الصباح": morning_dhikr, "🌙 أذكار المساء": evening_dhikr, "💤 أذكار النوم": sleep_dhikr}

    for tab, dhikr_list in zip([tab1, tab2, tab3], dhikr_tabs.values()):
        with tab:
            for j, dhikr in enumerate(dhikr_list):
                count_key = f"dhikr_count_{tab}_{j}"
                current_count = st.session_state.daily_dhikr_count.get(count_key, 0)

                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"""
                    <div class='dhikr-card'>
                        <div class='dhikr-text'>{dhikr["text"]}</div>
                        <div style='margin:10px 0'>
                            <span class='dhikr-count'>× {dhikr["count"]}</span>
                            <span style='color:#a5d6a7;font-family:Cairo,sans-serif;font-size:0.8rem;margin-right:10px'>{dhikr["benefit"]}</span>
                        </div>
                        <div style='color:#C9A84C;font-family:Cairo,sans-serif;font-size:0.9rem;margin-top:5px'>
                            العدد: {current_count} / {dhikr["count"]}
                        </div>
                        <div class='progress-bar'>
                            <div class='progress-fill' style='width:{min(current_count/dhikr["count"]*100,100):.0f}%'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("سبّح ✋", key=f"dhikr_{tab}_{j}", use_container_width=True, type="primary"):
                        if current_count < dhikr["count"]:
                            st.session_state.daily_dhikr_count[count_key] = current_count + 1
                        else:
                            st.session_state.daily_dhikr_count[count_key] = 0
                        st.rerun()

# ==================== أوقات الصلاة ====================
def render_prayer():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>🕌 أوقات الصلاة</h2>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        lat = st.number_input("خط العرض", value=30.06, format="%.4f", key="lat_input")
    with col2:
        lon = st.number_input("خط الطول", value=31.24, format="%.4f", key="lon_input")
    with col3:
        method = st.selectbox("طريقة الحساب", [
            (4, "أم القرى - مكة المكرمة"),
            (5, "الاتحاد الإسلامي في أمريكا الشمالية"),
            (2, "رابطة العالم الإسلامي"),
            (1, "الهيئة المصرية العامة"),
        ], format_func=lambda x: x[1], key="method_select")

    if st.button("🔄 جلب أوقات الصلاة", use_container_width=True, type="primary", key="get_prayer"):
        with st.spinner("جارٍ جلب أوقات الصلاة..."):
            timings = get_prayer_times(lat, lon, method[0] if method else 5)
            if timings:
                prayers = [
                    ("الفجر", timings.get("Fajr", ""), "🌙"),
                    ("الشروق", timings.get("Sunrise", ""), "🌅"),
                    ("الظهر", timings.get("Dhuhr", ""), "☀️"),
                    ("العصر", timings.get("Asr", ""), "🌤"),
                    ("المغرب", timings.get("Maghrib", ""), "🌇"),
                    ("العشاء", timings.get("Isha", ""), "🌙"),
                ]

                now = datetime.now().strftime("%H:%M")

                for name, time_str, icon in prayers:
                    is_next = False
                    st.markdown(f"""
                    <div class='prayer-time-card {"active" if is_next else ""}'>
                        <div style='display:flex;align-items:center;gap:10px'>
                            <span style='font-size:1.3rem'>{icon}</span>
                            <span class='prayer-name {"active" if is_next else ""}'>{name}</span>
                        </div>
                        <span class='prayer-time'>{time_str}</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style='text-align:center;margin-top:20px;color:#a5d6a7;font-family:Cairo,sans-serif;font-size:0.85rem;direction:rtl'>
                    📅 التاريخ: {datetime.now().strftime("%Y-%m-%d")} | ⏰ الوقت الحالي: {now}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("⚠️ تعذّر جلب أوقات الصلاة. تأكد من الإنترنت.")

# ==================== القبلة ====================
def render_qibla():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>🧭 اتجاه القبلة</h2>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("خط العرض", value=30.06, format="%.4f", key="qibla_lat")
    with col2:
        lon = st.number_input("خط الطول", value=31.24, format="%.4f", key="qibla_lon")

    if st.button("🧭 احسب اتجاه القبلة", use_container_width=True, type="primary", key="get_qibla"):
        with st.spinner("جارٍ الحساب..."):
            direction = get_qibla(lat, lon)
            if direction:
                st.markdown(f"""
                <div style='text-align:center;padding:40px;background:linear-gradient(135deg,#0d2018,#162a1f);border:2px solid #C9A84C;border-radius:20px;margin:20px 0'>
                    <div style='font-size:5rem;transform:rotate({direction}deg);display:inline-block;transition:transform 1s'>🧭</div>
                    <div style='color:#C9A84C;font-family:Amiri,serif;font-size:2rem;margin-top:15px'>اتجاه القبلة</div>
                    <div style='color:#f5f0e8;font-family:Cairo,sans-serif;font-size:1.5rem;margin:10px 0'>{direction:.2f}°</div>
                    <div style='color:#a5d6a7;font-family:Cairo,sans-serif;font-size:0.9rem'>من الشمال باتجاه عقارب الساعة</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("⚠️ تعذّر حساب اتجاه القبلة")

# ==================== الأحاديث ====================
def render_hadith():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>📜 الأحاديث النبوية الصحيحة</h2>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔍 ابحث عن حديث", "📚 أحاديث مختارة"])

    with tab1:
        search_term = st.text_input("ابحث عن حديث", placeholder="مثال: حديث عن الصدق، البر والرحم، طلب العلم...", key="hadith_search")
        if st.button("🔍 ابحث", use_container_width=True, type="primary", key="do_hadith_search"):
            if search_term:
                with st.spinner("جارٍ البحث..."):
                    prompt = f"""ابحث عن الأحاديث النبوية الصحيحة المتعلقة بـ: "{search_term}"

أعطِ 3-5 أحاديث فقط مؤكدة من صحيح البخاري أو مسلم أو سنن الترمذي أو غيرها من كتب الحديث الموثوقة، مع:
- نص الحديث كاملاً
- الراوي والمصدر (مثل: رواه البخاري برقم ...)
- درجة صحته
- الفائدة المستخلصة

لا تذكر أحاديث ضعيفة أو موضوعة."""
                    try:
                        response = requests.post(
                            "https://api.anthropic.com/v1/messages",
                            headers={"Content-Type": "application/json"},
                            json={"model": "claude-sonnet-4-6", "max_tokens": 1000,
                                  "messages": [{"role": "user", "content": prompt}]},
                            timeout=30
                        )
                        if response.status_code == 200:
                            result = response.json()['content'][0]['text']
                            st.markdown(f"""
                            <div class='hadith-card'>
                                <div class='hadith-text' style='font-size:1rem;color:#e8f5e9'>{result}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"خطأ: {e}")

    with tab2:
        # أحاديث ثابتة من صحيح البخاري ومسلم
        hadiths = [
            {"text": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى", "source": "صحيح البخاري — رقم 1 | عن عمر بن الخطاب رضي الله عنه"},
            {"text": "الدِّينُ النَّصِيحَةُ. قُلْنَا: لِمَنْ؟ قَالَ: لِلَّهِ وَلِكِتَابِهِ وَلِرَسُولِهِ وَلِأَئِمَّةِ الْمُسْلِمِينَ وَعَامَّتِهِمْ", "source": "صحيح مسلم — رقم 55 | عن تميم الداري رضي الله عنه"},
            {"text": "مَنْ كَانَ يُؤْمِنُ بِاللَّهِ وَالْيَوْمِ الآخِرِ فَلْيَقُلْ خَيْرًا أَوْ لِيَصْمُتْ", "source": "صحيح البخاري — رقم 6136 | عن أبي هريرة رضي الله عنه"},
            {"text": "لاَ يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ", "source": "صحيح البخاري — رقم 13 | عن أنس بن مالك رضي الله عنه"},
            {"text": "مَنْ سَلَكَ طَرِيقًا يَطْلُبُ فِيهِ عِلْمًا سَلَكَ اللَّهُ بِهِ طَرِيقًا مِنْ طُرُقِ الْجَنَّةِ", "source": "صحيح مسلم — رقم 2699 | عن أبي هريرة رضي الله عنه"},
            {"text": "اتَّقِ اللَّهِ حَيْثُمَا كُنْتَ، وَأَتْبِعِ السَّيِّئَةَ الْحَسَنَةَ تَمْحُهَا، وَخَالِقِ النَّاسَ بِخُلُقٍ حَسَنٍ", "source": "سنن الترمذي — رقم 1987 | عن أبي ذر رضي الله عنه"},
        ]

        for h in hadiths:
            st.markdown(f"""
            <div class='hadith-card'>
                <div class='hadith-text'>{h["text"]}</div>
                <div class='hadith-source'>📚 {h["source"]}</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== الإعدادات ====================
def render_settings():
    st.markdown("""<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl;text-align:right'>⚙️ الإعدادات</h2>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""<h3 style='color:#a5d6a7;font-family:Cairo,sans-serif;direction:rtl'>📖 إعدادات المصحف</h3>""", unsafe_allow_html=True)

        font_size = st.slider("حجم الخط", 1.2, 3.5, st.session_state.font_size, 0.1, key="settings_font")
        st.session_state.font_size = font_size

        st.session_state.show_translation = st.toggle("إظهار الترجمة", value=st.session_state.show_translation, key="toggle_trans")

        sheikh_names = list(SHEIKHS.values())
        sheikh_keys = list(SHEIKHS.keys())
        current_idx = sheikh_keys.index(st.session_state.selected_sheikh) if st.session_state.selected_sheikh in sheikh_keys else 0
        selected_name = st.selectbox("الشيخ الافتراضي للتلاوة", sheikh_names, index=current_idx, key="default_sheikh")
        st.session_state.selected_sheikh = sheikh_keys[sheikh_names.index(selected_name)]

    with col2:
        st.markdown("""<h3 style='color:#a5d6a7;font-family:Cairo,sans-serif;direction:rtl'>🎨 إعدادات المظهر</h3>""", unsafe_allow_html=True)

        st.session_state.focus_mode = st.toggle("وضع التركيز الافتراضي", value=st.session_state.focus_mode, key="toggle_focus")

        st.markdown("""<p style='color:#a5d6a7;font-family:Cairo,sans-serif;direction:rtl;font-size:0.9rem;margin-top:20px'>
        🌟 عرض معلومات التطبيق:
        </p>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='ayah-container' style='margin-top:10px'>
            <div style='color:#C9A84C;font-family:Amiri,serif;font-size:1.2rem;margin-bottom:10px'>مصحف هاشم الذكي</div>
            <div style='color:#a5d6a7;font-family:Cairo,sans-serif;font-size:0.85rem;line-height:2;direction:rtl'>
                ✅ الاستماع بصوت 8 مشايخ<br>
                ✅ تصحيح التلاوة بالذكاء الاصطناعي<br>
                ✅ خريطة القصص القرآنية<br>
                ✅ القرآن بحسب الحالة الوجدانية<br>
                ✅ التفسير والتدبر<br>
                ✅ البحث بالمقاصد<br>
                ✅ مكتبة القلب<br>
                ✅ الختمة التفاعلية<br>
                ✅ الأذكار مع العداد<br>
                ✅ أوقات الصلاة والقبلة<br>
                ✅ الأحاديث الصحيحة<br>
                ✅ المساعد القرآني الذكي
            </div>
        </div>
        """, unsafe_allow_html=True)

    # إعادة ضبط
    st.markdown("<div class='islamic-divider'>❧</div>", unsafe_allow_html=True)
    if st.button("🔄 إعادة ضبط جميع البيانات", use_container_width=True, key="reset_all"):
        for key in list(st.session_state.keys()):
            if key not in ['page']:
                del st.session_state[key]
        st.success("✅ تم إعادة ضبط جميع البيانات")
        st.rerun()

# ==================== التشغيل الرئيسي ====================
render_sidebar()

page = st.session_state.page
if page == 'home':
    render_home()
elif page == 'mushaf':
    render_mushaf()
elif page == 'audio':
    render_audio()
elif page == 'tajweed':
    render_tajweed()
elif page == 'mindmap':
    render_mindmap()
elif page == 'mood':
    render_mood()
elif page == 'tafseer':
    render_tafseer()
elif page == 'search':
    render_search()
elif page == 'ai_assistant':
    render_ai_assistant()
elif page == 'heart':
    render_heart()
elif page == 'bookmarks':
    render_bookmarks()
elif page == 'khatma':
    render_khatma()
elif page == 'dhikr':
    render_dhikr()
elif page == 'prayer':
    render_prayer()
elif page == 'qibla':
    render_qibla()
elif page == 'hadith':
    render_hadith()
elif page == 'settings':
    render_settings()

# علامة مائية
st.markdown("""<div class='watermark'>﴿ القرآن الكريم ﴾</div>""", unsafe_allow_html=True)
