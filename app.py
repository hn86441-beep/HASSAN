import streamlit as st
import requests
from datetime import datetime
import json
import math

st.set_page_config(
    page_title="مصحف هاشم الذكي",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════
#  CSS الكامل
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@300;400;600;700;900&display=swap');

:root{
  --gold:#C9A84C; --gold2:#e8c86a;
  --bg:#070f0a; --bg2:#0d1f16; --bg3:#122018; --card:#162a1f;
  --border:#2a4a35; --border2:#3d6b50;
  --text:#e8f5e9; --muted:#7fb899; --dim:#4a7060;
  --green:#2d6a4f; --lgreen:#52b788;
}

*{box-sizing:border-box; margin:0; padding:0;}

[data-testid="stAppViewContainer"]{
  background: radial-gradient(ellipse at 20% 0%, #0d2a1a 0%, #070f0a 60%) !important;
  min-height:100vh;
}
[data-testid="stSidebar"]{
  background: linear-gradient(180deg,#0a1a0f,#0d1f16) !important;
  border-right:1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child{padding-top:0 !important;}
#MainMenu,footer,header,[data-testid="stDeployButton"]{display:none !important;}
[data-testid="stMainBlockContainer"]{padding:1rem 1.5rem !important;}

/* ── Sidebar nav ── */
.nav-item{
  display:flex; align-items:center; gap:10px;
  padding:10px 14px; margin:2px 0;
  border-radius:10px; cursor:pointer;
  border:1px solid transparent;
  font-family:'Cairo',sans-serif; font-size:.88rem;
  color:var(--muted); direction:rtl;
  transition:all .2s;
}
.nav-item:hover{background:var(--card); border-color:var(--border); color:var(--text);}
.nav-item.active{
  background:linear-gradient(135deg,#1a3d2a,#0f2a1a);
  border-color:var(--gold); color:var(--gold);
}
.nav-item .ni{font-size:1.1rem; min-width:22px;}

/* ── Streamlit buttons override ── */
.stButton>button{
  background:var(--card) !important; border:1px solid var(--border) !important;
  border-radius:10px !important; color:var(--muted) !important;
  font-family:'Cairo',sans-serif !important; transition:all .2s !important;
  padding:8px 16px !important;
}
.stButton>button:hover{border-color:var(--gold) !important; color:var(--gold) !important; background:#1a3328 !important;}
.stButton>button[kind="primary"]{
  background:linear-gradient(135deg,var(--gold),#a07828) !important;
  color:#050e08 !important; font-weight:700 !important; border:none !important;
}
.stButton>button[kind="primary"]:hover{opacity:.9 !important; transform:translateY(-1px) !important;}

/* ── Inputs ── */
.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stSelectbox>div>div>div{
  background:var(--card) !important; border-color:var(--border) !important;
  color:var(--text) !important; font-family:'Cairo',sans-serif !important;
  border-radius:10px !important;
}
.stSelectbox>div>div>div{direction:rtl !important;}
label{color:var(--muted) !important; font-family:'Cairo',sans-serif !important;}
.stSlider>div>div>div{background:var(--border) !important;}
.stSlider>div>div>div>div{background:var(--gold) !important;}
.stCheckbox>label{color:var(--muted) !important;}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{background:transparent; gap:5px;}
.stTabs [data-baseweb="tab"]{
  background:var(--card) !important; border:1px solid var(--border) !important;
  border-radius:10px !important; color:var(--muted) !important;
  font-family:'Cairo',sans-serif !important;
}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,#1a3d2a,#0f2a1a) !important;
  border-color:var(--gold) !important; color:var(--gold) !important;
}

/* ── Page header ── */
.pg-header{
  background:linear-gradient(135deg,#0d2018,#162a1f,#0d2018);
  border:1px solid var(--gold); border-radius:18px;
  padding:28px 30px; text-align:center; margin-bottom:22px;
  box-shadow:0 6px 30px rgba(201,168,76,.15);
  position:relative; overflow:hidden;
}
.pg-header::after{
  content:''; position:absolute; inset:0;
  background:radial-gradient(circle at 50% 0%,rgba(201,168,76,.06),transparent 60%);
}
.pg-header h1{font-family:'Amiri',serif; font-size:2.4rem; color:var(--gold); direction:rtl;}
.pg-header p{font-family:'Cairo',sans-serif; color:var(--muted); font-size:.9rem; direction:rtl; margin-top:5px;}

/* ── Bismillah ── */
.bismillah{
  font-family:'Amiri',serif; font-size:2.2rem; color:var(--gold);
  text-align:center; padding:18px; direction:rtl;
  text-shadow:0 0 20px rgba(201,168,76,.35);
}

/* ── Surah header ── */
.surah-hdr{
  background:linear-gradient(135deg,#0d2018,#1a3328);
  border:1px solid var(--gold); border-radius:16px;
  padding:20px; text-align:center; margin:12px 0;
}
.surah-hdr .sname{font-family:'Amiri',serif; font-size:2.2rem; color:var(--gold);}
.surah-hdr .smeta{font-family:'Cairo',sans-serif; font-size:.8rem; color:var(--muted); margin-top:6px;}

/* ── Ayah card ── */
.ayah-card{
  background:linear-gradient(135deg,#0d2018,#142418);
  border:1px solid var(--border); border-radius:14px;
  padding:18px 22px; margin:8px 0;
  transition:border-color .2s, box-shadow .2s;
  direction:rtl; position:relative;
}
.ayah-card:hover{border-color:var(--border2); box-shadow:0 3px 16px rgba(201,168,76,.1);}
.ayah-card.highlight{border-color:var(--gold); box-shadow:0 0 20px rgba(201,168,76,.2);}
.ayah-num{
  display:inline-flex; align-items:center; justify-content:center;
  background:linear-gradient(135deg,var(--gold),#9a7020);
  color:#050e08; width:34px; height:34px; border-radius:50%;
  font-family:'Amiri',serif; font-size:.85rem; font-weight:700;
  float:left; margin-right:14px; flex-shrink:0;
}
.ayah-text{
  font-family:'Amiri',serif; color:#f5f0e8;
  line-height:2.6; display:block;
}
.ayah-trans{
  font-family:'Cairo',sans-serif; font-size:.85rem; color:var(--muted);
  border-top:1px solid var(--border); padding-top:10px; margin-top:10px;
}
.ayah-actions{
  display:flex; gap:6px; margin-top:10px; justify-content:flex-start;
}
.aa-btn{
  background:rgba(255,255,255,.04); border:1px solid var(--border);
  border-radius:8px; padding:5px 12px;
  color:var(--muted); font-family:'Cairo',sans-serif; font-size:.78rem;
  cursor:pointer; transition:all .2s;
}
.aa-btn:hover{border-color:var(--gold); color:var(--gold);}

/* ── Surah list item ── */
.sl-item{
  display:flex; align-items:center; justify-content:space-between;
  padding:12px 16px; margin:4px 0;
  background:var(--card); border:1px solid var(--border);
  border-radius:12px; cursor:pointer; direction:rtl;
  transition:all .2s;
}
.sl-item:hover{border-color:var(--gold); background:#1a3328;}
.sl-num{
  background:rgba(201,168,76,.12); border:1px solid rgba(201,168,76,.3);
  color:var(--gold); width:34px; height:34px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-family:'Amiri',serif; font-size:.85rem; flex-shrink:0;
}
.sl-name{font-family:'Amiri',serif; font-size:1.15rem; color:var(--text);}
.sl-meta{font-family:'Cairo',sans-serif; font-size:.72rem; color:var(--muted);}

/* ── Card generic ── */
.g-card{
  background:var(--card); border:1px solid var(--border);
  border-radius:14px; padding:20px; margin:8px 0;
  direction:rtl;
}
.g-card h3{font-family:'Cairo',sans-serif; color:var(--gold); margin-bottom:10px;}
.g-card p{font-family:'Cairo',sans-serif; color:var(--muted); font-size:.88rem; line-height:1.8;}

/* ── Stats row ── */
.stat-box{
  background:var(--card); border:1px solid var(--border);
  border-radius:12px; padding:18px; text-align:center; direction:rtl;
}
.stat-box .num{font-family:'Amiri',serif; font-size:2rem; color:var(--gold); display:block;}
.stat-box .lbl{font-family:'Cairo',sans-serif; font-size:.78rem; color:var(--muted);}

/* ── Progress bar ── */
.pbar{background:var(--border); border-radius:10px; height:7px; overflow:hidden; margin:8px 0;}
.pfill{height:100%; border-radius:10px; background:linear-gradient(90deg,var(--gold),var(--lgreen));}

/* ── Audio player custom ── */
.audio-wrap{
  background:linear-gradient(135deg,#0d2018,#162a1f);
  border:1px solid var(--gold); border-radius:18px;
  padding:24px; text-align:center; margin:14px 0;
}
.audio-wrap .aw-title{font-family:'Amiri',serif; font-size:1.8rem; color:var(--gold); direction:rtl;}
.audio-wrap .aw-meta{font-family:'Cairo',sans-serif; font-size:.85rem; color:var(--muted); margin:6px 0 16px;}
audio{width:90%; border-radius:40px; outline:none; margin-top:8px;}
audio::-webkit-media-controls-panel{background:#162a1f;}

/* ── Dhikr card ── */
.dhikr-card{
  background:var(--card); border:1px solid var(--border);
  border-radius:16px; padding:22px; margin:10px 0;
  direction:rtl; text-align:center;
  transition:border-color .2s;
}
.dhikr-card:hover{border-color:var(--border2);}
.dhikr-text{font-family:'Amiri',serif; font-size:1.5rem; color:#f0ebe0; line-height:2.2; margin-bottom:10px;}
.dhikr-badge{
  background:linear-gradient(135deg,var(--gold),#9a7020);
  color:#050e08; border-radius:30px; padding:4px 16px;
  font-family:'Cairo',sans-serif; font-size:.78rem; font-weight:700;
  display:inline-block; margin-bottom:8px;
}
.dhikr-benefit{font-family:'Cairo',sans-serif; font-size:.78rem; color:var(--dim);}
.dhikr-counter{
  font-family:'Amiri',serif; font-size:2rem; color:var(--gold);
  margin:8px 0;
}

/* ── Prayer time card ── */
.pt-card{
  display:flex; justify-content:space-between; align-items:center;
  background:var(--card); border:1px solid var(--border);
  border-radius:12px; padding:14px 20px; margin:6px 0; direction:rtl;
  transition:all .2s;
}
.pt-card.now{border-color:var(--gold); background:#1a3328; box-shadow:0 2px 14px rgba(201,168,76,.15);}
.pt-name{font-family:'Cairo',sans-serif; color:var(--text); font-size:.95rem;}
.pt-name.now{color:var(--gold); font-weight:700;}
.pt-time{font-family:'Amiri',serif; color:var(--gold); font-size:1.2rem;}

/* ── Hadith card ── */
.hadith-card{
  background:var(--card); border:1px solid var(--border);
  border-radius:16px; padding:24px; margin:10px 0; direction:rtl;
  position:relative; overflow:hidden;
}
.hadith-card::before{
  content:'"'; position:absolute; top:8px; right:16px;
  font-size:5rem; color:rgba(201,168,76,.08); font-family:serif; line-height:1;
}
.hadith-text{font-family:'Amiri',serif; font-size:1.25rem; color:#f0ebe0; line-height:2.2; margin-bottom:12px;}
.hadith-src{font-family:'Cairo',sans-serif; font-size:.78rem; color:var(--gold); border-top:1px solid var(--border); padding-top:10px;}

/* ── AI chat ── */
.chat-u{
  background:linear-gradient(135deg,var(--green),#1a3a28);
  border:1px solid var(--border2); border-radius:16px 16px 0 16px;
  padding:12px 18px; margin:8px 0 8px 15%; direction:rtl;
}
.chat-a{
  background:var(--card); border:1px solid var(--border);
  border-radius:16px 16px 16px 0;
  padding:12px 18px; margin:8px 15% 8px 0; direction:rtl;
}
.chat-lbl{font-family:'Cairo',sans-serif; font-size:.72rem; color:var(--dim); margin-bottom:4px;}
.chat-txt{font-family:'Cairo',sans-serif; color:var(--text); font-size:.9rem; line-height:1.8; white-space:pre-wrap;}

/* ── Mind map ── */
.mm-stage{
  background:var(--card); border:1px solid var(--border);
  border-radius:12px; padding:14px 18px; margin:6px 0;
  direction:rtl; cursor:pointer; transition:all .2s;
}
.mm-stage:hover{border-color:var(--gold); background:#1a3328;}
.mm-stage-num{
  background:linear-gradient(135deg,var(--gold),#9a7020);
  color:#050e08; width:28px; height:28px; border-radius:50%;
  display:inline-flex; align-items:center; justify-content:center;
  font-family:'Cairo',sans-serif; font-size:.78rem; font-weight:700;
  margin-left:10px;
}

/* ── Khatma grid ── */
.khatma-wrap{display:flex; flex-wrap:wrap; gap:4px; direction:rtl;}
.k-cell{
  background:var(--card); border:1px solid var(--border);
  border-radius:8px; width:calc(100%/8 - 4px); padding:7px 4px;
  text-align:center; cursor:pointer; transition:all .15s;
  font-family:'Cairo',sans-serif; font-size:.65rem; color:var(--muted);
}
.k-cell.done{background:linear-gradient(135deg,#1a3d2a,#0f2a1a); border-color:var(--gold); color:var(--gold);}
.k-cell:hover{border-color:var(--border2);}

/* ── Mood button ── */
.mood-btn{
  background:var(--card); border:2px solid var(--border);
  border-radius:16px; padding:14px 10px; text-align:center;
  cursor:pointer; transition:all .2s; margin:4px 0;
  font-family:'Cairo',sans-serif; direction:rtl;
}
.mood-btn.sel{border-color:var(--gold); background:#1a3328;}
.mood-btn .mi{font-size:1.6rem; display:block; margin-bottom:4px;}
.mood-btn .ml{font-size:.78rem; color:var(--muted);}
.mood-btn.sel .ml{color:var(--gold);}

/* ── Tajweed result ── */
.tj-result{
  background:var(--card); border:1px solid var(--gold);
  border-radius:14px; padding:20px; margin-top:16px; direction:rtl;
}
.tj-result h4{font-family:'Cairo',sans-serif; color:var(--gold); margin-bottom:12px;}
.tj-result p{font-family:'Cairo',sans-serif; color:var(--text); font-size:.9rem; line-height:2; white-space:pre-wrap;}

/* ── Info boxes ── */
.info-box{
  background:rgba(82,183,136,.08); border:1px solid rgba(82,183,136,.25);
  border-radius:10px; padding:12px 16px; margin:8px 0;
  font-family:'Cairo',sans-serif; color:var(--text); font-size:.85rem;
  direction:rtl; line-height:1.8;
}
.warn-box{
  background:rgba(201,168,76,.08); border:1px solid rgba(201,168,76,.25);
  border-radius:10px; padding:12px 16px; margin:8px 0;
  font-family:'Cairo',sans-serif; color:var(--text); font-size:.85rem; direction:rtl;
}

/* ── Divider ornament ── */
.orn{text-align:center; color:var(--gold); letter-spacing:8px; margin:12px 0; opacity:.7; font-size:.9rem;}

/* ── Scrollbar ── */
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--border2); border-radius:3px;}
::-webkit-scrollbar-thumb:hover{background:var(--gold);}

/* ── Spinner ── */
.stSpinner>div{border-top-color:var(--gold) !important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  بيانات السور الكاملة (114 سورة)
# ══════════════════════════════════════════════════════════════
SURAH_NAMES = [
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
SURAH_VERSES = [7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,110,98,135,
                112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,83,182,88,75,85,
                54,53,89,59,37,35,38,29,18,45,60,49,62,55,78,96,29,22,24,13,
                14,11,11,18,12,12,30,52,52,44,28,28,20,56,40,31,50,40,46,42,
                29,23,36,25,22,17,19,26,30,20,15,21,11,8,8,19,5,8,8,3,
                11,4,5,6]
SURAH_TYPE = ["مكية" if i+1 not in {2,3,4,5,8,9,13,22,24,33,47,48,49,55,57,58,59,60,61,62,63,64,65,66,76,98,99,110} else "مدنية" for i in range(114)]
SURAH_JUZ  = [1,1,1,1,1,1,1,1,10,11,11,12,13,13,14,14,15,15,16,16,17,17,18,18,18,19,19,20,20,21,21,21,21,22,22,22,23,23,23,24,24,24,25,25,25,26,26,26,26,26,26,27,27,27,27,27,27,28,28,28,28,28,28,28,28,28,29,29,29,29,29,29,29,29,29,29,29,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30]

def surah_info(n):  # n 1-based
    i = n-1
    return {"name": SURAH_NAMES[i], "verses": SURAH_VERSES[i], "type": SURAH_TYPE[i], "juz": SURAH_JUZ[i]}

SHEIKHS = {
    "ar.alafasy":            "مشاري راشد العفاسي",
    "ar.abdullahbasfar":     "عبد الله بصفر",
    "ar.hudhaify":           "علي الحذيفي",
    "ar.minshawi":           "محمد صديق المنشاوي",
    "ar.abdurrahmaansudais": "عبد الرحمن السديس",
    "ar.shaatree":           "أبو بكر الشاطري",
    "ar.mahermuaiqly":       "ماهر المعيقلي",
    "ar.muhammadayyoub":     "محمد أيوب",
}
SHEIKH_CDN = {
    "ar.alafasy":"Alafasy_128kbps",
    "ar.abdullahbasfar":"Abdullah_Basfar_192kbps",
    "ar.hudhaify":"Hudhaify_128kbps",
    "ar.minshawi":"Minshawy_Murattal_128kbps",
    "ar.abdurrahmaansudais":"Abdurrahmaan_As-Sudais_192kbps",
    "ar.shaatree":"Abu_Bakr_Ash-Shaatree_128kbps",
    "ar.mahermuaiqly":"MaherAlMuaiqly128kbps",
    "ar.muhammadayyoub":"Muhammad_Ayyoub_128kbps",
}

MOODS = {
    "😢 حزن وضيق":    [94, 93, 65, 2],
    "😊 فرح وشكر":    [55, 36, 1, 17],
    "😰 خوف وقلق":    [13, 3, 2, 58],
    "🥺 توبة وندم":   [39, 25, 4, 110],
    "🤔 تدبر وتأمل":  [45, 88, 56, 67],
    "🌙 قبل النوم":   [67, 32, 36, 112],
    "🌅 صباح جديد":   [78, 87, 1, 36],
    "💔 في المصيبة":  [2, 3, 94, 93],
    "🤲 طلب الرزق":   [67, 65, 73, 20],
    "🏥 شفاء المريض": [17, 10, 26, 27],
}

# ══════════════════════════════════════════════════════════════
#  تهيئة الجلسة
# ══════════════════════════════════════════════════════════════
def init():
    defs = {
        "page": "home",
        "cur_surah": 1, "cur_ayah": 1,
        "font_size": 1.9,
        "sheikh": "ar.alafasy",
        "show_trans": True, "show_tafseer": False,
        "bookmarks": [], "heart": [],
        "khatma": [False]*114,
        "dhikr_cnt": {},
        "chat": [],
        "mood_sel": None,
    }
    for k,v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()

# ══════════════════════════════════════════════════════════════
#  Helper: API calls
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=86400, show_spinner=False)
def fetch_surah(n):
    try:
        r = requests.get(f"https://api.alquran.cloud/v1/surah/{n}/editions/quran-uthmani,en.sahih", timeout=12)
        if r.status_code == 200: return r.json()["data"]
    except: pass
    return None

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_prayer(lat, lon, method=5):
    try:
        d = datetime.now().strftime("%d-%m-%Y")
        r = requests.get(f"https://api.aladhan.com/v1/timings/{d}?latitude={lat}&longitude={lon}&method={method}", timeout=10)
        if r.status_code == 200: return r.json()["data"]["timings"]
    except: pass
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_qibla(lat, lon):
    try:
        r = requests.get(f"https://api.aladhan.com/v1/qibla/{lat}/{lon}", timeout=10)
        if r.status_code == 200: return r.json()["data"]["direction"]
    except: pass
    return None

def audio_url(surah, ayah, sheikh="ar.alafasy"):
    cdn = SHEIKH_CDN.get(sheikh, "Alafasy_128kbps")
    s = str(surah).zfill(3); a = str(ayah).zfill(3)
    return f"https://verses.quran.com/{cdn}/{s}{a}.mp3"

def surah_audio_url(surah, sheikh="ar.alafasy"):
    cdn = SHEIKH_CDN.get(sheikh, "Alafasy_128kbps")
    s = str(surah).zfill(3)
    return f"https://download.quranicaudio.com/quran/{cdn.lower().replace('_128kbps','').replace('_192kbps','')}/{s}.mp3"

def claude_ask(prompt, system="أنت مساعد قرآني إسلامي عالم. أجب بالعربية بأسلوب واضح ودقيق.", history=None):
    msgs = []
    if history:
        msgs = [{"role": m["role"], "content": m["content"]} for m in history[-8:]]
    msgs.append({"role": "user", "content": prompt})
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json"},
            json={"model": "claude-sonnet-4-6", "max_tokens": 1000,
                  "system": system, "messages": msgs},
            timeout=35
        )
        if r.status_code == 200:
            return r.json()["content"][0]["text"]
    except Exception as e:
        return f"⚠️ خطأ: {e}"
    return "⚠️ لم يتم الاتصال بالخادم"

# ══════════════════════════════════════════════════════════════
#  Sidebar navigation
# ══════════════════════════════════════════════════════════════
PAGES = [
    ("🏠","home","الرئيسية"),
    ("📖","mushaf","المصحف الشريف"),
    ("🎙️","audio","مشغّل التلاوة"),
    ("🎤","tajweed","تصحيح التلاوة بالذكاء"),
    ("🗺️","mindmap","خريطة القصص القرآنية"),
    ("💭","mood","القرآن بحسب حالتي"),
    ("📚","tafseer","التفسير والتدبر"),
    ("🔍","search","البحث القرآني الذكي"),
    ("🤖","ai","المساعد القرآني"),
    ("❤️","heart","مكتبة القلب"),
    ("🔖","bookmarks","الإشارات المرجعية"),
    ("📿","khatma","تتبع الختمة"),
    ("🌙","dhikr","الأذكار"),
    ("🕌","prayer","أوقات الصلاة"),
    ("🧭","qibla","اتجاه القبلة"),
    ("📜","hadith","الأحاديث الصحيحة"),
    ("⚙️","settings","الإعدادات"),
]

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:18px 0 10px'>
      <div style='font-size:2.4rem'>🕌</div>
      <div style='font-family:Amiri,serif;font-size:1.3rem;color:#C9A84C;direction:rtl'>مصحف هاشم الذكي</div>
      <div style='font-family:Cairo,sans-serif;font-size:.72rem;color:#4a7060;direction:rtl;margin-top:4px'>القرآن الكريم بتجربة لا مثيل لها</div>
    </div>
    <div class='orn'>❧ ✦ ❧</div>
    """, unsafe_allow_html=True)

    cur = st.session_state.page
    for icon, key, label in PAGES:
        active = "active" if cur == key else ""
        # Use st.button for proper navigation
        if st.button(f"{icon}  {label}", key=f"nav_{key}",
                     use_container_width=True,
                     type="primary" if cur == key else "secondary"):
            st.session_state.page = key
            st.rerun()

    st.markdown("""
    <div class='orn' style='margin-top:16px'>❧ ✦ ❧</div>
    <div style='text-align:center;color:#2a4a35;font-family:Amiri,serif;font-size:.9rem;padding:8px'>
    بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  ① الرئيسية
# ══════════════════════════════════════════════════════════════
def pg_home():
    st.markdown("""
    <div class='pg-header'>
      <div class='orn'>﴾ ﴿</div>
      <h1>القرآن الكريم</h1>
      <p>مصحف هاشم الذكي — تجربة متكاملة ومبتكرة</p>
      <div class='orn'>﴾ ﴿</div>
    </div>
    <div class='bismillah'>بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    stats = [("١١٤","سورة"),("٦٢٣٦","آية"),("٣٠","جزءاً"),(str(sum(st.session_state.khatma)),"سورة أتممتها")]
    for col,(n,l) in zip([c1,c2,c3,c4],stats):
        with col:
            st.markdown(f"<div class='stat-box'><span class='num'>{n}</span><span class='lbl'>{l}</span></div>", unsafe_allow_html=True)

    st.markdown("<div class='orn' style='margin:20px 0'>❧ ✦ ✦ ✦ ❧</div>", unsafe_allow_html=True)

    feats = [
        ("📖","المصحف الشريف","اقرأ القرآن بخط عثماني مع ترجمة وتفسير فوري","mushaf"),
        ("🎙️","الاستماع لـ 8 مشايخ","استمع للقرآن بصوت أفضل القراء بجودة عالية","audio"),
        ("🎤","تصحيح التلاوة","الذكاء الاصطناعي يصحح تجويدك ومخارج حروفك","tajweed"),
        ("🗺️","خريطة القصص","تصفح قصص الأنبياء في خريطة تفاعلية بصرية","mindmap"),
        ("💭","القرآن لحالتي","آيات مختارة بذكاء حسب حالتك الوجدانية","mood"),
        ("🤖","المساعد الذكي","اسأل أي سؤال قرآني وتلقَّ إجابة علمية فورية","ai"),
        ("❤️","مكتبة القلب","احفظ الآيات المؤثرة مع مشاعرك وارجع إليها","heart"),
        ("📿","الختمة","تابع تقدمك في ختم القرآن الكريم سورة سورة","khatma"),
        ("📜","الأحاديث الصحيحة","أحاديث النبي ﷺ من البخاري ومسلم مع البحث","hadith"),
    ]
    cols = st.columns(3)
    for i,(icon,title,desc,pg) in enumerate(feats):
        with cols[i%3]:
            st.markdown(f"""
            <div class='g-card' style='min-height:130px'>
              <div style='font-size:1.8rem;margin-bottom:8px'>{icon}</div>
              <h3 style='font-size:.95rem'>{title}</h3>
              <p>{desc}</p>
            </div>""", unsafe_allow_html=True)
            if st.button("افتح", key=f"h_open_{pg}", use_container_width=True):
                st.session_state.page = pg
                st.rerun()

    st.markdown("<div class='orn' style='margin:20px 0'>❧</div>", unsafe_allow_html=True)
    si = surah_info(st.session_state.cur_surah)
    c1,c2 = st.columns([4,1])
    with c1:
        st.markdown(f"""
        <div class='g-card'>
          <div style='color:#C9A84C;font-family:Cairo,sans-serif;font-size:.8rem;margin-bottom:6px'>📖 تابع من حيث توقفت</div>
          <div style='font-family:Amiri,serif;font-size:1.3rem;color:#f0ebe0;direction:rtl'>سورة {si["name"]} — الآية {st.session_state.cur_ayah}</div>
          <div style='font-family:Cairo,sans-serif;font-size:.75rem;color:#4a7060;margin-top:4px'>{si["type"]} · {si["verses"]} آية · الجزء {si["juz"]}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        if st.button("▶ تابع", use_container_width=True, type="primary"):
            st.session_state.page = "mushaf"; st.rerun()

# ══════════════════════════════════════════════════════════════
#  ② المصحف
# ══════════════════════════════════════════════════════════════
def pg_mushaf():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>📖 المصحف الشريف</h2>", unsafe_allow_html=True)

    # controls row
    c1,c2,c3,c4 = st.columns([3,1,1,2])
    with c1:
        opts = {SURAH_NAMES[i]: i+1 for i in range(114)}
        cur_name = SURAH_NAMES[st.session_state.cur_surah-1]
        sel = st.selectbox("السورة", list(opts.keys()),
                           index=st.session_state.cur_surah-1, key="ms_surah")
        if opts[sel] != st.session_state.cur_surah:
            st.session_state.cur_surah = opts[sel]
            st.session_state.cur_ayah = 1
    with c2:
        max_a = SURAH_VERSES[st.session_state.cur_surah-1]
        a_val = st.number_input("من آية", 1, max_a,
                                 min(st.session_state.cur_ayah, max_a), key="ms_ayah")
        st.session_state.cur_ayah = int(a_val)
    with c3:
        fs = st.slider("الخط", 1.4, 3.2, st.session_state.font_size, 0.1, key="ms_font")
        st.session_state.font_size = fs
    with c4:
        tr = st.checkbox("الترجمة", st.session_state.show_trans, key="ms_tr")
        st.session_state.show_trans = tr
        tf = st.checkbox("تفسير مختصر", st.session_state.show_tafseer, key="ms_tf")
        st.session_state.show_tafseer = tf

    sn = st.session_state.cur_surah
    si = surah_info(sn)

    st.markdown(f"""
    <div class='surah-hdr'>
      <div class='smeta'>{si["type"]} · {si["verses"]} آية · الجزء {si["juz"]}</div>
      <div class='sname'>سُورَةُ {si["name"]}</div>
    </div>
    """, unsafe_allow_html=True)
    if sn != 9:
        st.markdown("<div class='bismillah'>بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>", unsafe_allow_html=True)

    with st.spinner("جارٍ تحميل الآيات…"):
        data = fetch_surah(sn)

    if not data:
        st.error("⚠️ تعذّر تحميل السورة. تحقق من الاتصال بالإنترنت.")
        return

    ar_ayahs  = data[0]["ayahs"]
    en_ayahs  = data[1]["ayahs"] if len(data) > 1 else []
    start = st.session_state.cur_ayah - 1
    show_n = 15  # عرض 15 آية

    for i, ayah in enumerate(ar_ayahs[start:start+show_n]):
        an = start + i + 1
        txt = ayah["text"]
        en  = en_ayahs[start+i]["text"] if en_ayahs and start+i < len(en_ayahs) else ""

        tr_html = f"<div class='ayah-trans'>{en}</div>" if tr and en else ""
        tf_html = ""
        if tf:
            tf_html = f"<div class='ayah-trans' style='color:#6a9a7a;font-style:normal'>💡 للحصول على التفسير اضغط زر التفسير أدناه</div>"

        aud = audio_url(sn, an, st.session_state.sheikh)

        col_txt, col_act = st.columns([5,1])
        with col_txt:
            st.markdown(f"""
            <div class='ayah-card'>
              <div style='display:flex;align-items:flex-start;gap:12px'>
                <span class='ayah-num'>{an}</span>
                <span class='ayah-text' style='font-size:{st.session_state.font_size}rem'>{txt}</span>
              </div>
              {tr_html}{tf_html}
            </div>""", unsafe_allow_html=True)
        with col_act:
            # Audio per ayah
            st.markdown(f"""
            <audio controls style='width:100%;height:32px;margin-top:12px'>
              <source src='{aud}' type='audio/mpeg'>
            </audio>""", unsafe_allow_html=True)
            if st.button("❤️", key=f"heart_{sn}_{an}", help="مكتبة القلب"):
                entry = {"surah":sn,"ayah":an,"text":txt,"surah_name":si["name"],
                         "mood":"","time":datetime.now().strftime("%Y-%m-%d")}
                if entry not in st.session_state.heart:
                    st.session_state.heart.append(entry)
                    st.toast("✅ أُضيفت لمكتبة القلب")
            if st.button("🔖", key=f"bm_{sn}_{an}", help="إشارة مرجعية"):
                bm = {"surah":sn,"ayah":an,"surah_name":si["name"],
                      "time":datetime.now().strftime("%Y-%m-%d %H:%M")}
                if bm not in st.session_state.bookmarks:
                    st.session_state.bookmarks.append(bm)
                    st.toast("✅ أُضيفت إشارة مرجعية")
            if tf:
                if st.button("📚", key=f"tf_{sn}_{an}", help="تفسير"):
                    with st.spinner("جارٍ التفسير…"):
                        res = claude_ask(f"فسّر الآية {an} من سورة {si['name']} تفسيراً ميسراً موجزاً لا يتجاوز 5 أسطر.")
                    st.info(res)

    # navigation
    st.markdown("<div class='orn'>❧</div>", unsafe_allow_html=True)
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:
        if sn > 1:
            if st.button("⟵ السورة السابقة", use_container_width=True):
                st.session_state.cur_surah -= 1; st.session_state.cur_ayah=1; st.rerun()
    with c2:
        if start > 0:
            if st.button("▲ آيات سابقة", use_container_width=True):
                st.session_state.cur_ayah = max(1, start-show_n+1); st.rerun()
    with c3:
        if st.button("🏠 الرئيسية", use_container_width=True):
            st.session_state.page="home"; st.rerun()
    with c4:
        if start+show_n < SURAH_VERSES[sn-1]:
            if st.button("▼ آيات تالية", use_container_width=True):
                st.session_state.cur_ayah = start+show_n+1; st.rerun()
    with c5:
        if sn < 114:
            if st.button("السورة التالية ⟶", use_container_width=True):
                st.session_state.cur_surah += 1; st.session_state.cur_ayah=1; st.rerun()

    # حفظ الموضع
    st.session_state.cur_ayah = int(a_val)

# ══════════════════════════════════════════════════════════════
#  ③ مشغّل التلاوة
# ══════════════════════════════════════════════════════════════
def pg_audio():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>🎙️ مشغّل التلاوة</h2>", unsafe_allow_html=True)

    # اختيار الشيخ
    sk_names = list(SHEIKHS.values())
    sk_keys  = list(SHEIKHS.keys())
    cur_idx  = sk_keys.index(st.session_state.sheikh) if st.session_state.sheikh in sk_keys else 0
    sel_name = st.selectbox("🕌 اختر الشيخ / القارئ", sk_names, index=cur_idx, key="aud_sheikh")
    st.session_state.sheikh = sk_keys[sk_names.index(sel_name)]

    # اختيار السورة والآية
    c1,c2 = st.columns(2)
    with c1:
        sel_s = st.selectbox("السورة", SURAH_NAMES,
                              index=st.session_state.cur_surah-1, key="aud_surah")
        sn = SURAH_NAMES.index(sel_s)+1
        st.session_state.cur_surah = sn
    with c2:
        max_a = SURAH_VERSES[sn-1]
        an = st.number_input("الآية", 1, max_a,
                              min(st.session_state.cur_ayah, max_a), key="aud_ayah")
        st.session_state.cur_ayah = int(an)

    si = surah_info(sn)
    aud = audio_url(sn, int(an), st.session_state.sheikh)

    # مشغل الآية الواحدة
    st.markdown(f"""
    <div class='audio-wrap'>
      <div class='aw-title'>سورة {si["name"]} — الآية {int(an)}</div>
      <div class='aw-meta'>🎤 {sel_name} &nbsp;|&nbsp; {si["type"]} · الجزء {si["juz"]}</div>
      <audio controls autoplay style='width:85%;border-radius:40px'>
        <source src='{aud}' type='audio/mpeg'>
        متصفحك لا يدعم تشغيل الصوت
      </audio>
    </div>""", unsafe_allow_html=True)

    # مشغل السورة كاملة
    st.markdown("<div class='orn'>❧</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='g-card' style='text-align:center'>
      <h3 style='margin-bottom:12px'>▶ تشغيل سورة {si["name"]} كاملة</h3>
      <p style='margin-bottom:14px'>استمع للسورة كاملة بصوت {sel_name}</p>
      <audio controls style='width:88%;border-radius:40px'>
        <source src='https://download.quranicaudio.com/quran/{SHEIKH_CDN.get(st.session_state.sheikh,"Alafasy_128kbps")}/{str(sn).zfill(3)}.mp3' type='audio/mpeg'>
      </audio>
      <div style='font-family:Cairo,sans-serif;font-size:.72rem;color:#4a7060;margin-top:10px'>
        ⓘ إذا لم يعمل الصوت الكامل جرّب الاستماع آية آية من المصحف
      </div>
    </div>""", unsafe_allow_html=True)

    # مشاعر أثناء الاستماع
    st.markdown("<div class='orn'>❧</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7fb899;font-family:Cairo,sans-serif;direction:rtl'>💭 كيف أثرت فيك هذه الآية؟ اضغط لتحفظها في مكتبة القلب:</p>", unsafe_allow_html=True)
    emotions = ["🥺 أبكتني","😌 اطمأننت","💪 قوّت عزيمتي","🤲 دفعتني للدعاء","💡 فتحت لي آفاقاً","❤️ ملأت قلبي"]
    cols = st.columns(3)
    for i,emo in enumerate(emotions):
        with cols[i%3]:
            if st.button(emo, key=f"emo_{i}", use_container_width=True):
                with st.spinner("جارٍ جلب نص الآية…"):
                    data = fetch_surah(sn)
                if data:
                    txt = data[0]["ayahs"][int(an)-1]["text"]
                else:
                    txt = f"الآية {int(an)}"
                entry = {"surah":sn,"ayah":int(an),"text":txt,
                         "surah_name":si["name"],"mood":emo,
                         "time":datetime.now().strftime("%Y-%m-%d")}
                st.session_state.heart.append(entry)
                st.toast(f"✅ حُفظت في مكتبة القلب: {emo}")

# ══════════════════════════════════════════════════════════════
#  ④ تصحيح التلاوة بالذكاء الاصطناعي
# ══════════════════════════════════════════════════════════════
def pg_tajweed():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>🎤 تصحيح التلاوة بالذكاء الاصطناعي</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
      🎯 <strong>كيف يعمل التصحيح؟</strong><br>
      ١- اختر الآية التي تريد التدرب عليها<br>
      ٢- اكتب ما قرأته كما نطقته (بدون تشكيل أو بتشكيل ناقص)<br>
      ٣- سيحلل الذكاء الاصطناعي أخطاءك في التجويد ومخارج الحروف والمد والغنة وكل أحكام التلاوة
    </div>""", unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        sel_s = st.selectbox("السورة", SURAH_NAMES,
                              index=st.session_state.cur_surah-1, key="tj_surah")
        sn = SURAH_NAMES.index(sel_s)+1
        max_a = SURAH_VERSES[sn-1]
    with c2:
        an = st.number_input("رقم الآية", 1, max_a, 1, key="tj_ayah")

    # جلب نص الآية تلقائياً
    correct_text = ""
    if st.button("📖 جلب نص الآية", key="fetch_ayah_btn"):
        with st.spinner("جارٍ جلب الآية…"):
            d = fetch_surah(sn)
        if d:
            correct_text = d[0]["ayahs"][int(an)-1]["text"]
            st.session_state["tj_correct"] = correct_text
            st.success(f"✅ تم جلب الآية: {correct_text[:60]}…")

    c1,c2 = st.columns(2)
    with c1:
        st.markdown("<p style='color:#C9A84C;font-family:Cairo,sans-serif;direction:rtl'>📖 الآية الصحيحة (أو أكتبها يدوياً):</p>", unsafe_allow_html=True)
        correct = st.text_area("الآية الصحيحة",
                                value=st.session_state.get("tj_correct",""),
                                height=130, key="tj_correct_input",
                                placeholder="اكتب أو الصق نص الآية هنا…")
    with c2:
        st.markdown("<p style='color:#C9A84C;font-family:Cairo,sans-serif;direction:rtl'>🎤 ما قرأته (اكتب نطقك كما قرأت):</p>", unsafe_allow_html=True)
        reading = st.text_area("ما قرأته",
                                height=130, key="tj_reading",
                                placeholder="اكتب ما قرأته بالضبط، مثلاً: الحمد لله رب العالمين…")

    c1,c2 = st.columns(2)
    with c1:
        level = st.selectbox("مستواك في التجويد", ["مبتدئ","متوسط","متقدم"], key="tj_level")
    with c2:
        aspects = st.multiselect("ما الذي تريد فحصه؟",
                                  ["مخارج الحروف","أحكام النون الساكنة والتنوين","المدود","الوقف والابتداء","الصفات","التشكيل"],
                                  default=["مخارج الحروف","أحكام النون الساكنة والتنوين","المدود"],
                                  key="tj_aspects")

    if st.button("🔍 صحّح تلاوتي الآن", use_container_width=True, type="primary", key="tj_go"):
        if not correct.strip():
            st.warning("⚠️ أدخل نص الآية أولاً (اضغط 'جلب نص الآية' أو اكتبه يدوياً)")
        elif not reading.strip():
            st.warning("⚠️ اكتب ما قرأته لنتمكن من التصحيح")
        else:
            with st.spinner("🧠 الذكاء الاصطناعي يحلّل تلاوتك…"):
                prompt = f"""أنت معلم قرآن كريم خبير في علم التجويد. المتعلم مستواه: {level}.

الآية الصحيحة: {correct}
ما قرأه المتعلم: {reading}
الجوانب المطلوب فحصها: {', '.join(aspects)}

قدّم تحليلاً تفصيلياً دقيقاً يتضمن:

✅ **ما أجاده المتعلم:**
[اذكر ما قرأه صحيحاً]

❌ **الأخطاء مع شرحها:**
[لكل خطأ: الكلمة الخاطئة → الصواب → القاعدة التجويدية → كيفية النطق الصحيح]

📚 **القواعد التجويدية المتعلقة بهذه الآية:**
[اذكر الأحكام التجويدية الموجودة في الآية]

💡 **نصائح للتحسين:**
[نصائح عملية محددة]

⭐ **التقييم: __ /١٠**

كن دقيقاً وتشجيعياً."""
                res = claude_ask(prompt, system="أنت معلم قرآن كريم خبير في علم التجويد. تحلّل التلاوة بدقة وتقدم تصحيحاً شاملاً بالعربية.")
            st.markdown(f"""
            <div class='tj-result'>
              <h4>🧠 نتيجة التحليل التجويدي — سورة {sel_s} الآية {int(an)}</h4>
              <p>{res}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='orn' style='margin:20px 0'>❧</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#7fb899;font-family:Cairo,sans-serif;direction:rtl'>📚 مرجع سريع لأحكام التجويد</h3>", unsafe_allow_html=True)
    rules = [
        ("الإظهار الحلقي","النون الساكنة أو التنوين + حروف الحلق (ء ه ع ح غ خ) → تُقرأ واضحة بلا غنة","#C9A84C"),
        ("الإدغام بغنة","النون الساكنة + (ي ن م و) → تُدغم مع غنة","#52b788"),
        ("الإدغام بلا غنة","النون الساكنة + (ر ل) → تُدغم بلا غنة","#7fb899"),
        ("الإقلاب","النون الساكنة + الباء → تُقلب ميماً مع إخفاء","#a0c4ff"),
        ("الإخفاء الحقيقي","النون الساكنة + 15 حرفاً → تُخفى مع غنة","#ffb347"),
        ("المد الطبيعي","حرف المد بلا سبب → حركتان","#C9A84C"),
        ("المد المتصل","حرف المد + همزة في كلمة → 4-5 حركات واجب","#52b788"),
        ("المد المنفصل","حرف المد + همزة في كلمة تالية → 4-5 حركات جائز","#7fb899"),
    ]
    c1,c2 = st.columns(2)
    for i,(r,e,col) in enumerate(rules):
        with (c1 if i%2==0 else c2):
            st.markdown(f"""
            <div class='g-card' style='margin:5px 0'>
              <div style='color:{col};font-family:Amiri,serif;font-size:1.1rem;margin-bottom:6px'>{r}</div>
              <p style='font-size:.8rem'>{e}</p>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  ⑤ خريطة القصص القرآنية
# ══════════════════════════════════════════════════════════════
def pg_mindmap():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>🗺️ خريطة القصص القرآنية التفاعلية</h2>", unsafe_allow_html=True)

    STORIES = {
        "سيدنا موسى عليه السلام 🌊": {
            "color":"#52b788",
            "stages":[
                {"t":"الميلاد والإلقاء في النهر","refs":["طه:38-39","القصص:7-8"],"l":"توكّل الأم على الله وحسن الظن به"},
                {"t":"النشأة في قصر فرعون","refs":["القصص:9-13","طه:40"],"l":"حفظ الله لأوليائه في أحلك الأماكن"},
                {"t":"قتل القبطي والفرار","refs":["القصص:15-21"],"l":"التوبة والعودة إلى الله والهروب من الظلم"},
                {"t":"في مدين والزواج","refs":["القصص:22-28"],"l":"الأمانة في العمل والعطاء دون انتظار"},
                {"t":"الرسالة وآية العصا","refs":["طه:9-24","النمل:7-12"],"l":"الثقة المطلقة بالله عند تلقي المهمة الكبرى"},
                {"t":"مواجهة فرعون","refs":["طه:43-76","الشعراء:16-51"],"l":"الشجاعة في قول الحق ومواجهة الطغيان"},
                {"t":"عبور البحر والنجاة","refs":["البقرة:50","الشعراء:63-68"],"l":"النجاة تأتي من حيث لا يُتوقع عند ذروة الأزمة"},
                {"t":"ألواح التوراة","refs":["الأعراف:144-154"],"l":"شرف الحكمة الإلهية والمسؤولية تجاهها"},
            ]},
        "سيدنا يوسف عليه السلام ⭐": {
            "color":"#C9A84C",
            "stages":[
                {"t":"الرؤيا وغيرة الإخوة","refs":["يوسف:4-5"],"l":"الصبر والكتمان عند الحسد"},
                {"t":"الإلقاء في البئر","refs":["يوسف:9-18"],"l":"الحسد وعواقبه الوخيمة على صاحبه"},
                {"t":"بيعه في مصر","refs":["يوسف:19-22"],"l":"الله يُدبّر حتى في المصائب"},
                {"t":"إغراء امرأة العزيز","refs":["يوسف:21-29"],"l":"العفة والاستعاذة بالله عند الفتنة"},
                {"t":"السجن وتعبير الرؤى","refs":["يوسف:36-42"],"l":"الدعوة في المحن واستثمار كل موقف"},
                {"t":"تفسير رؤيا الملك","refs":["يوسف:43-49"],"l":"العلم نعمة تُستثمر لخير الناس"},
                {"t":"التمكين والعدل","refs":["يوسف:54-57"],"l":"الكفاءة والأمانة طريق للمكانة"},
                {"t":"لمّ الشمل والعفو","refs":["يوسف:58-101"],"l":"العفو والتسامح مع من أساء"},
            ]},
        "سيدنا إبراهيم عليه السلام 🔥": {
            "color":"#ff7043",
            "stages":[
                {"t":"الدعوة لأبيه وقومه","refs":["الأنعام:74-83","مريم:41-48"],"l":"الصدق مع الوالدين حتى في الدعوة"},
                {"t":"كسر الأصنام","refs":["الأنبياء:51-67"],"l":"الشجاعة في نشر الحق ومواجهة الشرك"},
                {"t":"النار والنجاة المعجزة","refs":["الأنبياء:68-70","العنكبوت:24"],"l":"برود النار على من اصطفاه الله"},
                {"t":"الهجرة وبناء الكعبة","refs":["إبراهيم:35-41","البقرة:127"],"l":"إحياء شعائر الله والدعاء للذرية"},
                {"t":"رؤيا ذبح الولد","refs":["الصافات:100-113"],"l":"الطاعة الكاملة لله والفداء العظيم"},
            ]},
        "سيدنا نوح عليه السلام 🚢": {
            "color":"#64b5f6",
            "stages":[
                {"t":"الدعوة ألف سنة إلا خمسين","refs":["نوح:1-20","العنكبوت:14"],"l":"الصبر في الدعوة على مدى قرون"},
                {"t":"بناء السفينة","refs":["هود:36-38","المؤمنون:27"],"l":"الطاعة المطلقة حتى في غير الأوان"},
                {"t":"الطوفان وهلاك الكافرين","refs":["هود:40-48"],"l":"العدل الإلهي ونهاية الطغيان"},
                {"t":"الاستواء على الجودي","refs":["هود:44"],"l":"الأمل بعد البلاء ورحمة الله"},
            ]},
    }

    story_name = st.selectbox("🗺️ اختر قصة نبي كريم", list(STORIES.keys()), key="mm_story")
    story = STORIES[story_name]
    col = story["color"]

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#080f0a,#0d2018);border:2px solid {col};border-radius:18px;
         padding:22px;text-align:center;margin:12px 0'>
      <div style='color:{col};font-family:Amiri,serif;font-size:1.8rem'>{story_name}</div>
      <div style='color:#4a7060;font-family:Cairo,sans-serif;font-size:.78rem;margin-top:6px'>
        اضغط على أي مرحلة لعرض تفاصيلها
      </div>
    </div>""", unsafe_allow_html=True)

    for idx, s in enumerate(story["stages"]):
        with st.expander(f"{'○' if idx==0 else '●'} المرحلة {idx+1}: {s['t']}", expanded=(idx==0)):
            refs_html = " &nbsp;|&nbsp; ".join([f"📖 {r}" for r in s["refs"]])
            st.markdown(f"""
            <div style='direction:rtl;padding:8px'>
              <div style='color:{col};font-family:Cairo,sans-serif;font-size:.85rem;margin-bottom:8px'>{refs_html}</div>
              <div style='color:#e8f5e9;font-family:Cairo,sans-serif;font-size:.92rem'>
                💎 <strong>الدرس:</strong> {s["l"]}
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"🤖 اشرح هذه المرحلة بالتفصيل", key=f"mm_ai_{idx}"):
                with st.spinner("جارٍ الشرح…"):
                    res = claude_ask(f"اشرح مرحلة '{s['t']}' من {story_name} شرحاً وافياً مثيراً للاهتمام مع الدروس والعبر، بأسلوب سردي جذاب. الآيات: {', '.join(s['refs'])}")
                st.info(res)

    st.markdown("<div class='orn'>❧</div>", unsafe_allow_html=True)
    if st.button("🤖 اشرح لي القصة كاملة بأسلوب مؤثر", use_container_width=True, type="primary", key="mm_full"):
        with st.spinner("جارٍ إعداد القصة…"):
            res = claude_ask(f"""اسرد {story_name} من القرآن الكريم بأسلوب شيّق مؤثر يشمل:
- أبرز المحطات
- الدروس والعبر
- الآيات الأكثر تأثيراً في هذه القصة
- كيف نطبق هذه الدروس في حياتنا اليوم
اكتب بأسلوب أدبي جميل بالعربية.""")
        st.markdown(f"<div class='hadith-card'><div class='hadith-text' style='font-size:.95rem'>{res}</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  ⑥ القرآن بحسب حالتي
# ══════════════════════════════════════════════════════════════
def pg_mood():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>💭 القرآن بحسب حالتي</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7fb899;font-family:Cairo,sans-serif;direction:rtl;text-align:center;margin-bottom:16px'>أخبرني كيف تشعر الآن وسأختار لك الآيات الأنسب ✨</p>", unsafe_allow_html=True)

    moods = list(MOODS.keys())
    cols = st.columns(5)
    for i,m in enumerate(moods):
        with cols[i%5]:
            sel_style = "border:2px solid #C9A84C;background:#1a3328;" if st.session_state.mood_sel==m else ""
            st.markdown(f"<div class='mood-btn' style='{sel_style}'><span class='mi'>{m.split()[0]}</span><span class='ml'>{' '.join(m.split()[1:])}</span></div>", unsafe_allow_html=True)
            if st.button("اختر", key=f"mood_sel_{i}", use_container_width=True):
                st.session_state.mood_sel = m; st.rerun()

    if st.session_state.mood_sel:
        mood = st.session_state.mood_sel
        surah_list = MOODS[mood]
        st.markdown(f"""
        <div class='g-card' style='text-align:center;margin:16px 0'>
          <div style='font-size:2rem'>{mood.split()[0]}</div>
          <div style='color:#C9A84C;font-family:Cairo,sans-serif;font-size:1.1rem;font-weight:700;margin-top:8px'>
            إليك سور مختارة لـ "{' '.join(mood.split()[1:])}"
          </div>
        </div>""", unsafe_allow_html=True)

        for sn in surah_list:
            si = surah_info(sn)
            c1,c2,c3 = st.columns([4,1,1])
            with c1:
                st.markdown(f"""
                <div class='sl-item'>
                  <div>
                    <div class='sl-name'>سورة {si["name"]}</div>
                    <div class='sl-meta'>{si["type"]} · {si["verses"]} آية · الجزء {si["juz"]}</div>
                  </div>
                  <div class='sl-num'>{sn}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                if st.button("📖 اقرأ", key=f"md_r_{sn}", use_container_width=True):
                    st.session_state.cur_surah=sn; st.session_state.cur_ayah=1
                    st.session_state.page="mushaf"; st.rerun()
            with c3:
                if st.button("🎙️ استمع", key=f"md_a_{sn}", use_container_width=True):
                    st.session_state.cur_surah=sn; st.session_state.cur_ayah=1
                    st.session_state.page="audio"; st.rerun()

        st.markdown("<div class='orn'>❧</div>", unsafe_allow_html=True)
        if st.button("🤖 اقترح لي آيات إضافية بالذكاء الاصطناعي", use_container_width=True, type="primary", key="mood_ai"):
            with st.spinner("جارٍ الاختيار…"):
                res = claude_ask(f"""أنا أشعر بـ "{' '.join(mood.split()[1:])}" الآن.
اقترح لي 5 آيات قرآنية مختارة بعناية مع:
- نص الآية كاملاً
- السورة ورقم الآية
- لماذا اخترتها لهذه الحالة تحديداً
- كلمة دعم وتشجيع
أجب بأسلوب دافئ وروحاني.""")
            st.markdown(f"<div class='hadith-card'><div class='hadith-text' style='font-size:.95rem'>{res}</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  ⑦ التفسير والتدبر
# ══════════════════════════════════════════════════════════════
def pg_tafseer():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>📚 التفسير والتدبر</h2>", unsafe_allow_html=True)

    t1,t2,t3,t4 = st.tabs(["📖 التفسير الميسّر","📅 سبب النزول","🔗 المتشابهات","💎 التدبر"])

    with t1:
        c1,c2 = st.columns(2)
        with c1:
            sel_s = st.selectbox("السورة",SURAH_NAMES,index=st.session_state.cur_surah-1,key="tf1_s")
            sn=SURAH_NAMES.index(sel_s)+1
        with c2:
            an=st.number_input("الآية",1,SURAH_VERSES[sn-1],1,key="tf1_a")
        if st.button("📖 اعرض التفسير الميسّر",use_container_width=True,type="primary",key="tf1_go"):
            with st.spinner("جارٍ التفسير…"):
                res=claude_ask(f"""فسّر الآية {int(an)} من سورة {sel_s} تفسيراً ميسراً شاملاً يتضمن:
١- **المعنى الإجمالي** بأسلوب واضح مفهوم
٢- **معاني المفردات الصعبة**
٣- **الفوائد والدروس** المستخلصة
٤- **وجه الإعجاز** إن وُجد
أجب بالعربية الفصيحة المفهومة.""")
            st.markdown(f"<div class='tj-result'><h4>📖 تفسير الآية {int(an)} من سورة {sel_s}</h4><p>{res}</p></div>",unsafe_allow_html=True)

    with t2:
        q=st.text_input("موضوع البحث",placeholder="مثال: سورة العلق، الآية الأولى، آية الكرسي…",key="tf2_q")
        if st.button("🔍 ابحث عن سبب النزول",use_container_width=True,type="primary",key="tf2_go"):
            if q:
                with st.spinner("جارٍ البحث…"):
                    res=claude_ask(f"""أذكر سبب نزول: {q}
اذكر:
- الحادثة أو الموقف الذي نزلت فيه
- المصدر (البخاري أو مسلم أو غيرهما)
- الحكمة من نزولها في هذا السياق
التزم بالروايات الصحيحة فقط.""")
                st.markdown(f"<div class='hadith-card'><div class='hadith-text' style='font-size:.95rem'>{res}</div></div>",unsafe_allow_html=True)

    with t3:
        w=st.text_input("كلمة أو عبارة قرآنية",placeholder="مثال: الصبر، الرحمة، التوكل…",key="tf3_w")
        if st.button("🔗 ابحث عن المتشابهات اللفظية",use_container_width=True,type="primary",key="tf3_go"):
            if w:
                with st.spinner("جارٍ البحث…"):
                    res=claude_ask(f"""ابحث في القرآن الكريم عن الآيات المتشابهة في ذكر "{w}".
اذكر:
- الآيات بنصها مع السورة والرقم
- السياق المختلف لكل آية
- الفروق الدقيقة بين الاستخدامات
- الحكمة من التكرار""")
                st.markdown(f"<div class='hadith-card'><div class='hadith-text' style='font-size:.95rem'>{res}</div></div>",unsafe_allow_html=True)

    with t4:
        q=st.text_area("آية أو موضوع للتدبر",placeholder="مثال: ﴿وَعَسَى أَن تَكْرَهُوا شَيْئاً وَهُوَ خَيْرٌ لَّكُمْ﴾",height=90,key="tf4_q")
        if st.button("💎 تدبّر معي",use_container_width=True,type="primary",key="tf4_go"):
            if q:
                with st.spinner("جارٍ التدبر…"):
                    res=claude_ask(f"""تدبّر هذه الآية أو الموضوع: {q}
قدّم:
١- أعمق ما في الآية من معانٍ
٢- كيف تطبّقها في حياتك اليومية تطبيقاً عملياً
٣- النظرة الكونية التي تفتحها على الوجود
٤- سؤال للتأمل والتفكر
أجب بأسلوب روحاني مؤثر يلمس القلب.""")
                st.markdown(f"<div class='tj-result'><h4>💎 التدبر</h4><p>{res}</p></div>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  ⑧ البحث القرآني
# ══════════════════════════════════════════════════════════════
def pg_search():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>🔍 البحث القرآني الذكي</h2>", unsafe_allow_html=True)
    st.markdown("<div class='info-box'>💡 ابحث بالمعنى والموضوع، لا تحتاج لمعرفة النص الحرفي</div>", unsafe_allow_html=True)

    q=st.text_input("ابحث بأي كلمة أو معنى",placeholder="مثال: آيات عن الصبر في البلاء، الأمل بعد اليأس…",key="s_q")
    c1,c2=st.columns(2)
    with c1:
        stype=st.selectbox("نوع البحث",["بحث معنوي (بالمقاصد)","بحث بالكلمة","بحث موضوعي"],key="s_type")
    with c2:
        n_res=st.slider("عدد النتائج",3,12,5,key="s_n")

    if st.button("🔍 ابحث الآن",use_container_width=True,type="primary",key="s_go"):
        if q:
            with st.spinner("جارٍ البحث في القرآن الكريم…"):
                res=claude_ask(f"""أنت محرك بحث قرآني ذكي. ابحث عن: "{q}" ({stype})
أعطِ {n_res} آيات مع:
- نص الآية كاملاً بالتشكيل
- اسم السورة ورقم الآية بين قوسين مربعين
- شرح موجز لعلاقتها بالبحث
رتّبها من الأكثر صلة للأقل.""")
            st.markdown(f"<div class='hadith-card'><div style='color:#C9A84C;font-family:Cairo,sans-serif;margin-bottom:12px;direction:rtl'>نتائج البحث عن: {q}</div><div class='hadith-text' style='font-size:.95rem'>{res}</div></div>",unsafe_allow_html=True)

    st.markdown("<div class='orn'>❧</div>",unsafe_allow_html=True)
    st.markdown("<p style='color:#7fb899;font-family:Cairo,sans-serif;direction:rtl'>🚀 بحث سريع:</p>",unsafe_allow_html=True)
    quick=["آيات الصبر والثبات","فضل العلم والتعلم","بر الوالدين","التوبة والمغفرة","الرزق والبركة","الأمل والتفاؤل","العدل والقسط","الرحمة بالخلق"]
    cols=st.columns(4)
    for i,qk in enumerate(quick):
        with cols[i%4]:
            if st.button(qk,key=f"qk_{i}",use_container_width=True):
                with st.spinner("جارٍ البحث…"):
                    res=claude_ask(f"ابحث في القرآن عن أبرز 4 آيات تتعلق بـ '{qk}' مع النص والسورة والفائدة.")
                st.markdown(f"<div class='hadith-card'><div class='hadith-text' style='font-size:.95rem'>{res}</div></div>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  ⑨ المساعد الذكي
# ══════════════════════════════════════════════════════════════
def pg_ai():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>🤖 المساعد القرآني الذكي</h2>", unsafe_allow_html=True)
    st.markdown("<div class='info-box'>🌟 اسألني أي شيء: تفسير، تجويد، أحكام شرعية، قصص أنبياء، حكمة، دعاء…</div>",unsafe_allow_html=True)

    # عرض المحادثة
    for msg in st.session_state.chat:
        if msg["role"]=="user":
            st.markdown(f"<div class='chat-u'><div class='chat-lbl'>أنت</div><div class='chat-txt'>{msg['content']}</div></div>",unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-a'><div class='chat-lbl'>🤖 المساعد القرآني</div><div class='chat-txt'>{msg['content']}</div></div>",unsafe_allow_html=True)

    if not st.session_state.chat:
        st.markdown("<p style='color:#4a7060;font-family:Cairo,sans-serif;direction:rtl;margin-top:16px'>💡 أسئلة مقترحة:</p>",unsafe_allow_html=True)
        sugs=["ما أفضل آيات للقراءة قبل النوم؟","اشرح لي سورة الفاتحة كاملاً","ما معنى حروف المقطعة في القرآن؟","أنواع المد في التجويد","كيف أحفظ القرآن بسرعة؟","ما أكثر سورة مكررة في القرآن؟"]
        cols=st.columns(2)
        for i,s in enumerate(sugs):
            with cols[i%2]:
                if st.button(s,key=f"sug_{i}",use_container_width=True):
                    st.session_state.chat.append({"role":"user","content":s})
                    with st.spinner("🤖 جارٍ التفكير…"):
                        rep=claude_ask(s,history=st.session_state.chat[:-1])
                    st.session_state.chat.append({"role":"assistant","content":rep})
                    st.rerun()

    c1,c2=st.columns([5,1])
    with c1:
        inp=st.text_input("اكتب سؤالك…",placeholder="أي سؤال قرآني أو ديني…",key="ai_inp",label_visibility="collapsed")
    with c2:
        send=st.button("إرسال ✉️",key="ai_send",use_container_width=True,type="primary")

    if send and inp.strip():
        st.session_state.chat.append({"role":"user","content":inp.strip()})
        with st.spinner("🤖 جارٍ التفكير…"):
            rep=claude_ask(inp.strip(),
                           system="أنت مساعد قرآني إسلامي عالم ذو علم واسع. أجب بالعربية الفصيحة المفهومة. كن دقيقاً ودافئاً ومشجعاً.",
                           history=st.session_state.chat[:-1])
        st.session_state.chat.append({"role":"assistant","content":rep})
        st.rerun()

    if st.session_state.chat:
        if st.button("🗑️ مسح المحادثة",key="ai_clear"):
            st.session_state.chat=[];st.rerun()

# ══════════════════════════════════════════════════════════════
#  ⑩ مكتبة القلب
# ══════════════════════════════════════════════════════════════
def pg_heart():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>❤️ مكتبة القلب</h2>", unsafe_allow_html=True)

    if not st.session_state.heart:
        st.markdown("""
        <div style='text-align:center;padding:60px 20px'>
          <div style='font-size:4rem'>❤️</div>
          <div style='color:#4a7060;font-family:Cairo,sans-serif;margin-top:14px;direction:rtl'>
            مكتبة القلب فارغة<br>
            <small>أضف الآيات التي تؤثر فيك من المصحف أو مشغل الصوت</small>
          </div>
        </div>""",unsafe_allow_html=True)
        return

    st.markdown(f"<p style='color:#7fb899;font-family:Cairo,sans-serif;direction:rtl'>{len(st.session_state.heart)} آية في مكتبة قلبك</p>",unsafe_allow_html=True)

    for i,item in enumerate(reversed(st.session_state.heart)):
        ri = len(st.session_state.heart)-1-i
        c1,c2=st.columns([5,1])
        with c1:
            mood_span = f"<span style='background:rgba(201,168,76,.12);border:1px solid rgba(201,168,76,.3);border-radius:20px;padding:2px 10px;color:#C9A84C;font-family:Cairo,sans-serif;font-size:.75rem;margin-top:6px;display:inline-block'>{item.get('mood','')}</span>" if item.get('mood') else ""
            st.markdown(f"""
            <div class='ayah-card'>
              <div style='color:#C9A84C;font-family:Cairo,sans-serif;font-size:.78rem;margin-bottom:6px'>📖 سورة {item.get("surah_name","")} — الآية {item.get("ayah","")}</div>
              <div style='font-family:Amiri,serif;font-size:1.5rem;color:#f0ebe0;direction:rtl;line-height:2.4'>{item.get("text","")}</div>
              {mood_span}
              <div style='color:#2a4a35;font-family:Cairo,sans-serif;font-size:.7rem;margin-top:6px'>{item.get("time","")}</div>
            </div>""",unsafe_allow_html=True)
        with c2:
            au=audio_url(item.get("surah",1),item.get("ayah",1),st.session_state.sheikh)
            st.markdown(f"<audio controls style='width:100%;height:30px;margin-top:14px'><source src='{au}' type='audio/mpeg'></audio>",unsafe_allow_html=True)
            if st.button("🗑️",key=f"dh_{ri}",help="حذف"):
                st.session_state.heart.pop(ri);st.rerun()

# ══════════════════════════════════════════════════════════════
#  ⑪ الإشارات المرجعية
# ══════════════════════════════════════════════════════════════
def pg_bookmarks():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>🔖 الإشارات المرجعية</h2>",unsafe_allow_html=True)

    if not st.session_state.bookmarks:
        st.markdown("<div style='text-align:center;padding:60px;color:#4a7060;font-family:Cairo,sans-serif;direction:rtl'><div style='font-size:3rem'>🔖</div><br>لا توجد إشارات بعد — أضفها أثناء القراءة</div>",unsafe_allow_html=True)
        return

    for i,bm in enumerate(reversed(st.session_state.bookmarks)):
        ri=len(st.session_state.bookmarks)-1-i
        c1,c2,c3=st.columns([4,1,1])
        with c1:
            st.markdown(f"""
            <div class='sl-item'>
              <div>
                <div class='sl-name'>سورة {bm.get("surah_name","")} — الآية {bm.get("ayah","")}</div>
                <div class='sl-meta'>⏰ {bm.get("time","")}</div>
              </div>
              <div class='sl-num'>{bm.get("surah","")}</div>
            </div>""",unsafe_allow_html=True)
        with c2:
            if st.button("📖 اذهب",key=f"bm_go_{ri}",use_container_width=True):
                st.session_state.cur_surah=bm.get("surah",1)
                st.session_state.cur_ayah=bm.get("ayah",1)
                st.session_state.page="mushaf";st.rerun()
        with c3:
            if st.button("🗑️",key=f"bm_del_{ri}",help="حذف"):
                st.session_state.bookmarks.pop(ri);st.rerun()

# ══════════════════════════════════════════════════════════════
#  ⑫ الختمة
# ══════════════════════════════════════════════════════════════
def pg_khatma():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>📿 تتبع الختمة القرآنية</h2>",unsafe_allow_html=True)

    done=sum(st.session_state.khatma)
    pct=(done/114)*100
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#0d2018,#162a1f);border:1px solid #C9A84C;border-radius:16px;padding:22px;text-align:center;margin-bottom:18px'>
      <div style='color:#C9A84C;font-family:Amiri,serif;font-size:2.8rem;font-weight:700'>{done}/114</div>
      <div style='color:#7fb899;font-family:Cairo,sans-serif;font-size:.85rem;margin:6px 0'>سورة أتممت قراءتها</div>
      <div class='pbar' style='margin:12px auto;max-width:400px'><div class='pfill' style='width:{pct:.1f}%'></div></div>
      <div style='color:#C9A84C;font-family:Cairo,sans-serif'>{pct:.1f}% مكتملة</div>
    </div>""",unsafe_allow_html=True)

    c1,c2=st.columns(2)
    with c1:
        if st.button("✅ علّم الكل",use_container_width=True):
            st.session_state.khatma=[True]*114;st.rerun()
    with c2:
        if st.button("🔄 إعادة ضبط",use_container_width=True):
            st.session_state.khatma=[False]*114;st.rerun()

    st.markdown("<p style='color:#7fb899;font-family:Cairo,sans-serif;direction:rtl;margin-top:12px'>اضغط على السورة لتغيير حالتها:</p>",unsafe_allow_html=True)

    cols=st.columns(8)
    for idx in range(114):
        with cols[idx%8]:
            done_flag=st.session_state.khatma[idx]
            label=f"✅{SURAH_NAMES[idx][:4]}" if done_flag else SURAH_NAMES[idx][:4]
            if st.button(label,key=f"k_{idx}",use_container_width=True,
                          help=f"سورة {SURAH_NAMES[idx]} - {SURAH_VERSES[idx]} آية",
                          type="primary" if done_flag else "secondary"):
                st.session_state.khatma[idx]=not done_flag;st.rerun()

# ══════════════════════════════════════════════════════════════
#  ⑬ الأذكار
# ══════════════════════════════════════════════════════════════
def pg_dhikr():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>🌙 الأذكار والأدعية</h2>",unsafe_allow_html=True)

    DHIKR = {
        "🌅 أذكار الصباح":[
            {"t":"أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ","n":1,"b":"ذكر الصباح الجامع"},
            {"t":"اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ","n":1,"b":"تفويض الأمر كله لله"},
            {"t":"سُبْحَانَ اللَّهِ وَبِحَمْدِهِ","n":100,"b":"تُمحى به الخطايا وإن كانت كزبد البحر"},
            {"t":"لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ","n":10,"b":"كمن أعتق 4 من ولد إسماعيل"},
            {"t":"اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَٰهَ إِلَّا أَنْتَ خَلَقْتَنِي وَأَنَا عَبْدُكَ وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ","n":1,"b":"سيد الاستغفار — من قاله موقناً دخل الجنة"},
        ],
        "🌙 أذكار المساء":[
            {"t":"أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ","n":1,"b":"ذكر المساء الجامع"},
            {"t":"اللَّهُمَّ عَافِنِي فِي بَدَنِي اللَّهُمَّ عَافِنِي فِي سَمْعِي اللَّهُمَّ عَافِنِي فِي بَصَرِي لَا إِلَٰهَ إِلَّا أَنْتَ","n":3,"b":"دعاء العافية في الجسد"},
            {"t":"اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْكُفْرِ وَالْفَقْرِ وَأَعُوذُ بِكَ مِنْ عَذَابِ الْقَبْرِ","n":3,"b":"الاستعاذة من المهالك"},
            {"t":"سُبْحَانَ اللَّهِ وَبِحَمْدِهِ عَدَدَ خَلْقِهِ وَرِضَا نَفْسِهِ وَزِنَةَ عَرْشِهِ وَمِدَادَ كَلِمَاتِهِ","n":3,"b":"أفضل التسبيح"},
        ],
        "💤 أذكار النوم":[
            {"t":"بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا","n":1,"b":"ذكر النوم النبوي"},
            {"t":"اللَّهُمَّ قِنِي عَذَابَكَ يَوْمَ تَبْعَثُ عِبَادَكَ","n":3,"b":"الحفظ من عذاب يوم القيامة"},
            {"t":"سُبْحَانَ اللَّهِ — الحَمْدُ لِلَّهِ — اللَّهُ أَكْبَرُ","n":33,"b":"وصية النبي ﷺ لفاطمة — خير من خادم"},
            {"t":"آيَةُ الْكُرْسِيِّ","n":1,"b":"حفظ الله لليل — لا يقربه شيطان حتى يصبح"},
            {"t":"قُلْ هُوَ اللَّهُ أَحَدٌ — قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ — قُلْ أَعُوذُ بِرَبِّ النَّاسِ","n":3,"b":"كفاية من كل شيء"},
        ],
    }

    t1,t2,t3 = st.tabs(list(DHIKR.keys()))
    for tab, (tab_name, items) in zip([t1,t2,t3], DHIKR.items()):
        with tab:
            for j,d in enumerate(items):
                key=f"dc_{tab_name}_{j}"
                cnt=st.session_state.dhikr_cnt.get(key,0)
                pct=min(cnt/d["n"],1.0)*100
                c1,c2=st.columns([5,1])
                with c1:
                    st.markdown(f"""
                    <div class='dhikr-card'>
                      <div class='dhikr-text'>{d["t"]}</div>
                      <div class='dhikr-badge'>× {d["n"]}</div>
                      <div class='dhikr-benefit'>{d["b"]}</div>
                      <div class='dhikr-counter'>{cnt}/{d["n"]}</div>
                      <div class='pbar'><div class='pfill' style='width:{pct:.0f}%'></div></div>
                    </div>""",unsafe_allow_html=True)
                with c2:
                    st.write("")
                    st.write("")
                    if st.button("سبّح\n✋",key=f"dhb_{tab_name}_{j}",use_container_width=True,type="primary"):
                        nc=cnt+1 if cnt<d["n"] else 0
                        st.session_state.dhikr_cnt[key]=nc
                        if nc==d["n"]: st.toast("🎉 أتممت هذا الذكر!")
                        st.rerun()

# ══════════════════════════════════════════════════════════════
#  ⑭ أوقات الصلاة
# ══════════════════════════════════════════════════════════════
def pg_prayer():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>🕌 أوقات الصلاة</h2>",unsafe_allow_html=True)

    c1,c2,c3=st.columns(3)
    with c1: lat=st.number_input("خط العرض (Latitude)",value=30.0626,format="%.4f",key="pr_lat")
    with c2: lon=st.number_input("خط الطول (Longitude)",value=31.2497,format="%.4f",key="pr_lon")
    with c3:
        methods={4:"أم القرى (مكة)",2:"رابطة العالم الإسلامي",5:"أمريكا الشمالية",1:"هيئة مصرية",3:"MWL",8:"خليج عُمان"}
        msel=st.selectbox("طريقة الحساب",list(methods.values()),key="pr_m")
        mkey=[k for k,v in methods.items() if v==msel][0]

    st.markdown("<div class='warn-box'>📍 الموقع الافتراضي القاهرة — عدّله حسب مدينتك</div>",unsafe_allow_html=True)

    if st.button("🔄 احسب أوقات الصلاة",use_container_width=True,type="primary",key="pr_go"):
        with st.spinner("جارٍ الجلب…"):
            t=fetch_prayer(lat,lon,mkey)
        if t:
            prayers=[("الفجر","Fajr","🌙"),("الشروق","Sunrise","🌅"),("الظهر","Dhuhr","☀️"),
                     ("العصر","Asr","🌤"),("المغرب","Maghrib","🌇"),("العشاء","Isha","🌙")]
            now=datetime.now().strftime("%H:%M")
            for name,key,icon in prayers:
                val=t.get(key,"--:--")
                is_now="now" if val[:5]==now[:5] else ""
                st.markdown(f"""
                <div class='pt-card {is_now}'>
                  <div style='display:flex;align-items:center;gap:10px'>
                    <span style='font-size:1.2rem'>{icon}</span>
                    <span class='pt-name {is_now}'>{name}</span>
                    {"<span style='background:#C9A84C;color:#050e08;border-radius:20px;padding:2px 8px;font-family:Cairo,sans-serif;font-size:.7rem;font-weight:700'>الآن</span>" if is_now else ""}
                  </div>
                  <span class='pt-time'>{val}</span>
                </div>""",unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center;margin-top:12px;color:#4a7060;font-family:Cairo,sans-serif;font-size:.78rem'>📅 {datetime.now().strftime('%Y-%m-%d')} | ⏰ {now}</div>",unsafe_allow_html=True)
        else:
            st.error("⚠️ تعذّر جلب أوقات الصلاة. تحقق من الاتصال.")

# ══════════════════════════════════════════════════════════════
#  ⑮ القبلة
# ══════════════════════════════════════════════════════════════
def pg_qibla():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>🧭 اتجاه القبلة</h2>",unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1: lat=st.number_input("خط العرض",value=30.0626,format="%.4f",key="qb_lat")
    with c2: lon=st.number_input("خط الطول",value=31.2497,format="%.4f",key="qb_lon")

    if st.button("🧭 احسب اتجاه القبلة",use_container_width=True,type="primary",key="qb_go"):
        with st.spinner("جارٍ الحساب…"):
            d=fetch_qibla(lat,lon)
        if d is not None:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#0d2018,#162a1f);border:2px solid #C9A84C;border-radius:20px;padding:40px;text-align:center;margin:16px 0'>
              <div style='font-size:5rem;display:inline-block;transform:rotate({d}deg);transition:transform 1s ease'>🧭</div>
              <div style='color:#C9A84C;font-family:Amiri,serif;font-size:2rem;margin-top:14px'>اتجاه القبلة</div>
              <div style='color:#f5f0e8;font-family:Cairo,sans-serif;font-size:1.4rem;margin:8px 0'>{d:.2f}°</div>
              <div style='color:#7fb899;font-family:Cairo,sans-serif;font-size:.82rem'>من الشمال باتجاه عقارب الساعة</div>
            </div>""",unsafe_allow_html=True)
        else:
            st.error("⚠️ تعذّر الحساب. تحقق من الاتصال.")

# ══════════════════════════════════════════════════════════════
#  ⑯ الأحاديث
# ══════════════════════════════════════════════════════════════
def pg_hadith():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>📜 الأحاديث النبوية الصحيحة</h2>",unsafe_allow_html=True)

    t1,t2=st.tabs(["🔍 ابحث عن حديث","📚 أحاديث مختارة"])

    with t1:
        q=st.text_input("موضوع الحديث",placeholder="مثال: الصدق، رحمة القلب، طلب العلم…",key="hd_q")
        if st.button("🔍 ابحث",use_container_width=True,type="primary",key="hd_go"):
            if q:
                with st.spinner("جارٍ البحث…"):
                    res=claude_ask(f"""ابحث عن الأحاديث النبوية الصحيحة الثابتة المتعلقة بـ: "{q}"
أعطِ 4-5 أحاديث مع:
- نص الحديث الكامل
- الصحابي الراوي
- المصدر والرقم (مثل: رواه البخاري برقم 52)
- درجة صحته
- الفائدة المستخلصة
لا تذكر أحاديث ضعيفة أو موضوعة.""")
                st.markdown(f"<div class='hadith-card'><div class='hadith-text' style='font-size:.92rem'>{res}</div></div>",unsafe_allow_html=True)

    with t2:
        HADITHS=[
            {"t":"إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى","s":"صحيح البخاري (1) | عن عمر بن الخطاب رضي الله عنه"},
            {"t":"الدِّينُ النَّصِيحَةُ","s":"صحيح مسلم (55) | عن تميم الداري رضي الله عنه"},
            {"t":"لَا يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لِأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ","s":"صحيح البخاري (13) | عن أنس بن مالك رضي الله عنه"},
            {"t":"مَنْ كَانَ يُؤْمِنُ بِاللَّهِ وَالْيَوْمِ الْآخِرِ فَلْيَقُلْ خَيْرًا أَوْ لِيَصْمُتْ","s":"صحيح البخاري (6136) | عن أبي هريرة رضي الله عنه"},
            {"t":"مَنْ سَلَكَ طَرِيقًا يَطْلُبُ فِيهِ عِلْمًا سَلَكَ اللَّهُ بِهِ طَرِيقًا مِنْ طُرُقِ الْجَنَّةِ","s":"صحيح مسلم (2699) | عن أبي هريرة رضي الله عنه"},
            {"t":"اتَّقِ اللَّهَ حَيْثُمَا كُنْتَ وَأَتْبِعِ السَّيِّئَةَ الْحَسَنَةَ تَمْحُهَا وَخَالِقِ النَّاسَ بِخُلُقٍ حَسَنٍ","s":"سنن الترمذي (1987) | عن أبي ذر رضي الله عنه"},
            {"t":"خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ","s":"صحيح البخاري (5027) | عن عثمان رضي الله عنه"},
            {"t":"إِنَّ اللَّهَ لَا يَنْظُرُ إِلَى صُوَرِكُمْ وَأَمْوَالِكُمْ وَلَكِنْ يَنْظُرُ إِلَى قُلُوبِكُمْ وَأَعْمَالِكُمْ","s":"صحيح مسلم (2564) | عن أبي هريرة رضي الله عنه"},
        ]
        for h in HADITHS:
            st.markdown(f"<div class='hadith-card'><div class='hadith-text'>{h['t']}</div><div class='hadith-src'>📚 {h['s']}</div></div>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  ⑰ الإعدادات
# ══════════════════════════════════════════════════════════════
def pg_settings():
    st.markdown("<h2 style='color:#C9A84C;font-family:Amiri,serif;direction:rtl'>⚙️ الإعدادات</h2>",unsafe_allow_html=True)

    c1,c2=st.columns(2)
    with c1:
        st.markdown("<h3 style='color:#7fb899;font-family:Cairo,sans-serif;direction:rtl'>📖 إعدادات المصحف</h3>",unsafe_allow_html=True)
        fs=st.slider("حجم خط الآيات",1.2,3.4,st.session_state.font_size,0.05,key="cfg_fs")
        st.session_state.font_size=fs
        st.session_state.show_trans=st.checkbox("إظهار الترجمة الإنجليزية",st.session_state.show_trans,key="cfg_tr")
        st.session_state.show_tafseer=st.checkbox("إظهار زر التفسير لكل آية",st.session_state.show_tafseer,key="cfg_tf")

        st.markdown("<h3 style='color:#7fb899;font-family:Cairo,sans-serif;direction:rtl;margin-top:20px'>🎙️ إعدادات الصوت</h3>",unsafe_allow_html=True)
        sk_n=list(SHEIKHS.values()); sk_k=list(SHEIKHS.keys())
        ci=sk_k.index(st.session_state.sheikh) if st.session_state.sheikh in sk_k else 0
        sn=st.selectbox("الشيخ الافتراضي",sk_n,index=ci,key="cfg_sk")
        st.session_state.sheikh=sk_k[sk_n.index(sn)]

    with c2:
        st.markdown("<h3 style='color:#7fb899;font-family:Cairo,sans-serif;direction:rtl'>📊 الإحصائيات</h3>",unsafe_allow_html=True)
        stats=[
            ("سور أتممتها",f"{sum(st.session_state.khatma)}/114"),
            ("آيات في مكتبة القلب",str(len(st.session_state.heart))),
            ("الإشارات المرجعية",str(len(st.session_state.bookmarks))),
            ("رسائل المساعد الذكي",str(len(st.session_state.chat))),
        ]
        for lbl,val in stats:
            st.markdown(f"""
            <div class='g-card' style='padding:12px 16px;margin:6px 0'>
              <div style='display:flex;justify-content:space-between;direction:rtl'>
                <span style='font-family:Cairo,sans-serif;color:#7fb899;font-size:.85rem'>{lbl}</span>
                <span style='font-family:Amiri,serif;color:#C9A84C;font-size:1.1rem'>{val}</span>
              </div>
            </div>""",unsafe_allow_html=True)

        st.markdown("<h3 style='color:#7fb899;font-family:Cairo,sans-serif;direction:rtl;margin-top:16px'>🔄 إعادة ضبط</h3>",unsafe_allow_html=True)
        if st.button("🗑️ مسح مكتبة القلب",use_container_width=True,key="cfg_dh"):
            st.session_state.heart=[];st.toast("✅ تم المسح")
        if st.button("🗑️ مسح الإشارات المرجعية",use_container_width=True,key="cfg_db"):
            st.session_state.bookmarks=[];st.toast("✅ تم المسح")
        if st.button("🗑️ مسح محادثة المساعد",use_container_width=True,key="cfg_dc"):
            st.session_state.chat=[];st.toast("✅ تم المسح")
        if st.button("⚠️ إعادة ضبط كل شيء",use_container_width=True,key="cfg_all"):
            for k in ["heart","bookmarks","chat","khatma","dhikr_cnt"]:
                st.session_state[k]=[] if k!="khatma" and k!="dhikr_cnt" else ([False]*114 if k=="khatma" else {})
            st.toast("✅ تم إعادة الضبط")
            st.rerun()

    st.markdown("""
    <div class='g-card' style='margin-top:20px;text-align:center'>
      <div style='color:#C9A84C;font-family:Amiri,serif;font-size:1.4rem;margin-bottom:10px'>مصحف هاشم الذكي</div>
      <div style='color:#7fb899;font-family:Cairo,sans-serif;font-size:.78rem;line-height:2;direction:rtl'>
        ✅ المصحف الكامل (114 سورة) بخط عثماني<br>
        ✅ الاستماع لـ 8 مشايخ<br>
        ✅ تصحيح التلاوة بالذكاء الاصطناعي<br>
        ✅ خريطة القصص القرآنية التفاعلية<br>
        ✅ القرآن بحسب الحالة الوجدانية<br>
        ✅ التفسير وسبب النزول والمتشابهات<br>
        ✅ البحث بالمقاصد<br>
        ✅ المساعد القرآني الذكي<br>
        ✅ مكتبة القلب والإشارات المرجعية<br>
        ✅ الختمة التفاعلية والأذكار<br>
        ✅ أوقات الصلاة واتجاه القبلة<br>
        ✅ الأحاديث الصحيحة مع البحث
      </div>
    </div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  Router
# ══════════════════════════════════════════════════════════════
PAGE_FN = {
    "home": pg_home,
    "mushaf": pg_mushaf,
    "audio": pg_audio,
    "tajweed": pg_tajweed,
    "mindmap": pg_mindmap,
    "mood": pg_mood,
    "tafseer": pg_tafseer,
    "search": pg_search,
    "ai": pg_ai,
    "heart": pg_heart,
    "bookmarks": pg_bookmarks,
    "khatma": pg_khatma,
    "dhikr": pg_dhikr,
    "prayer": pg_prayer,
    "qibla": pg_qibla,
    "hadith": pg_hadith,
    "settings": pg_settings,
}

fn = PAGE_FN.get(st.session_state.page, pg_home)
fn()
