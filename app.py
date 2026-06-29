import streamlit as st
import requests
import random
import json
from datetime import datetime

# ========== إعدادات الصفحة ==========
st.set_page_config(
    page_title="القرآن الكريم - موقع إبداعي",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== التنسيقات والأنماط ==========
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1a472a, #2d6a4f);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: #f5e6ca;
        font-family: 'Amiri', serif;
    }
    .main-header h1 {
        font-size: 3.5rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }
    .ayah-card {
        background: #f8f4ec;
        padding: 1.5rem;
        border-radius: 15px;
        border-right: 5px solid #2d6a4f;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        direction: rtl;
        font-family: 'Amiri', 'Traditional Arabic', serif;
    }
    .ayah-arabic {
        font-size: 2rem;
        line-height: 2.8rem;
        color: #1a1a1a;
    }
    .ayah-translation {
        font-size: 1.1rem;
        color: #4a4a4a;
        margin-top: 0.5rem;
        direction: ltr;
        font-family: 'Segoe UI', sans-serif;
    }
    .surah-name {
        font-size: 1.5rem;
        color: #2d6a4f;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
        border-top: 4px solid #2d6a4f;
        height: 100%;
    }
    .feature-card h3 {
        color: #1a472a;
        margin-bottom: 0.5rem;
    }
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #666;
        font-size: 0.9rem;
        border-top: 1px solid #eee;
        margin-top: 3rem;
    }
    .stButton > button {
        background: #2d6a4f !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 0.5rem 2rem !important;
        font-weight: bold !important;
        border: none !important;
        transition: all 0.3s !important;
    }
    .stButton > button:hover {
        background: #1a472a !important;
        transform: scale(1.02) !important;
    }
    .verse-counter {
        background: #e8f0e8;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-size: 0.9rem;
        color: #2d6a4f;
    }
    .audio-container {
        direction: ltr;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ========== دوال API الأساسية ==========
QURAN_API_BASE = "https://api.alquran.cloud/v1"

def get_all_surahs():
    """جلب قائمة جميع سور القرآن"""
    try:
        response = requests.get(f"{QURAN_API_BASE}/surah")
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
    except:
        pass
    return []

def get_ayahs(surah_number, start=1, end=10):
    """جلب آيات محددة من سورة معينة"""
    try:
        response = requests.get(f"{QURAN_API_BASE}/surah/{surah_number}")
        if response.status_code == 200:
            data = response.json()
            ayahs = data.get('data', {}).get('ayahs', [])
            filtered = [a for a in ayahs if start <= a.get('numberInSurah', 0) <= end]
            return filtered
    except:
        pass
    return []

def get_random_ayah():
    """جلب آية عشوائية من القرآن"""
    try:
        surah_num = random.randint(1, 114)
        response = requests.get(f"{QURAN_API_BASE}/surah/{surah_num}")
        if response.status_code == 200:
            data = response.json()
            ayahs = data.get('data', {}).get('ayahs', [])
            if ayahs:
                ayah = random.choice(ayahs)
                surah_name = data.get('data', {}).get('name', '')
                return ayah, surah_name, surah_num
    except:
        pass
    return None, None, None

def search_ayahs(keyword):
    """بحث بسيط في الآيات (محاكاة)"""
    results = []
    try:
        for surah_num in range(1, 115):
            response = requests.get(f"{QURAN_API_BASE}/surah/{surah_num}")
            if response.status_code == 200:
                data = response.json()
                ayahs = data.get('data', {}).get('ayahs', [])
                surah_name = data.get('data', {}).get('name', '')
                for ayah in ayahs:
                    text = ayah.get('text', '')
                    if keyword.lower() in text.lower():
                        results.append({
                            'surah': surah_name,
                            'surah_number': surah_num,
                            'ayah_number': ayah.get('numberInSurah', 0),
                            'text': text,
                            'translation': ayah.get('translation', {}).get('en', '')
                        })
                if len(results) >= 20:
                    break
    except:
        pass
    return results

# ========== دالة التلاوة (رابط الصوت المضمون) ==========
def get_audio_url(surah_number, ayah_number):
    """
    رابط مباشر لصوت الآية من شبكة Islamic Network (يعمل بدون مشاكل CORS)
    بصوت القارئ مشاري العفاسي بجودة 128 كيلوبت في الثانية
    """
    return f"https://cdn.islamic.network/quran/audio/128/ar.alafasy/{surah_number:03d}{ayah_number:03d}.mp3"

# ========== الشريط الجانبي ==========
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3047/3047924.png", width=80)
    st.markdown("### 🕋 القائمة")
    
    page = st.radio(
        "اختر الصفحة",
        ["🏠 الرئيسية", "📖 القراءة", "🎯 آية عشوائية", "🔍 البحث", "📊 عن الموقع"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; font-size: 0.8rem; color: #888;">
        <p>✨ { اليوم }</p>
        <p style="direction: ltr;">📖 "اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ"</p>
    </div>
    """.replace("{ اليوم }", datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)

# ========== الصفحة الرئيسية ==========
if page == "🏠 الرئيسية":
    st.markdown("""
    <div class="main-header">
        <h1>🕌 القرآن الكريم</h1>
        <p>موقع إبداعي لقراءة وتدبر آيات الله مع خاصية الاستماع</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📖</h3>
            <h3>قراءة</h3>
            <p style="color:#666; font-size:0.9rem;">تصفح السور<br>مع الترجمة والصوت</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯</h3>
            <h3>آية عشوائية</h3>
            <p style="color:#666; font-size:0.9rem;">آيات عشوائية للتدبر<br>والاستماع إليها</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍</h3>
            <h3>بحث</h3>
            <p style="color:#666; font-size:0.9rem;">ابحث في آيات القرآن<br>بسهولة وسرعة</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h3>🎧</h3>
            <h3>تلاوة</h3>
            <p style="color:#666; font-size:0.9rem;">استمع للتلاوة بصوت<br>مشاري العفاسي</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🌟 آية اليوم مع التلاوة")
    
    ayah, surah_name, surah_num = get_random_ayah()
    if ayah:
        ayah_number = ayah.get('numberInSurah', 0)
        st.markdown(f"""
        <div class="ayah-card">
            <div class="ayah-arabic">{ayah.get('text', '')}</div>
            <div class="surah-name">— {surah_name} ({surah_num}) : {ayah_number}</div>
            <div class="ayah-translation">"{ayah.get('translation', {}).get('en', 'Translation not available')}"</div>
        </div>
        """, unsafe_allow_html=True)
        
        # مشغل الصوت (يعمل الآن)
        audio_url = get_audio_url(surah_num, ayah_number)
        st.audio(audio_url, format="audio/mp3")
    
    if st.button("🔄 تحديث الآية"):
        st.rerun()

# ========== صفحة القراءة (مع التلاوة لكل آية) ==========
elif page == "📖 القراءة":
    st.markdown("### 📖 تصفح القرآن مع الاستماع")
    
    surahs = get_all_surahs()
    
    if surahs:
        surah_names = [f"{s.get('number', 0)}. {s.get('name', '')} ({s.get('englishName', '')})" for s in surahs]
        selected = st.selectbox("اختر سورة", surah_names, index=0)
        
        if selected:
            surah_number = int(selected.split('.')[0])
            surah_data = next((s for s in surahs if s.get('number') == surah_number), None)
            
            if surah_data:
                total_ayahs = surah_data.get('numberOfAyahs', 10)
                
                col1, col2 = st.columns(2)
                with col1:
                    start = st.number_input("من الآية", min_value=1, max_value=total_ayahs, value=1)
                with col2:
                    end = st.number_input("إلى الآية", min_value=start, max_value=total_ayahs, value=min(start+9, total_ayahs))
                
                if st.button("📖 اقرأ واستمع", use_container_width=True):
                    ayahs = get_ayahs(surah_number, start, end)
                    
                    if ayahs:
                        st.markdown(f"""
                        <div style="text-align:center; margin: 1rem 0;">
                            <span class="verse-counter">📖 {surah_data.get('name', '')} — {len(ayahs)} آيات</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        for ayah in ayahs:
                            ayah_num = ayah.get('numberInSurah', 0)
                            audio_url = get_audio_url(surah_number, ayah_num)
                            
                            col_text, col_audio = st.columns([5, 2])
                            
                            with col_text:
                                st.markdown(f"""
                                <div class="ayah-card" style="margin:0.3rem 0; padding:1rem;">
                                    <div style="display:flex; justify-content:space-between; align-items:center;">
                                        <span class="verse-counter">🕌 {ayah_num}</span>
                                    </div>
                                    <div class="ayah-arabic" style="font-size:1.8rem;">{ayah.get('text', '')}</div>
                                    <div class="ayah-translation">"{ayah.get('translation', {}).get('en', 'Translation not available')}"</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col_audio:
                                st.markdown("<div style='margin-top: 1.5rem;'>🎧 استمع</div>", unsafe_allow_html=True)
                                st.audio(audio_url, format="audio/mp3")
                    else:
                        st.warning("⚠️ لم يتم العثور على آيات")
    else:
        st.error("❌ تعذر تحميل قائمة السور. يرجى التحقق من اتصال الإنترنت.")

# ========== صفحة الآية العشوائية (مع الصوت) ==========
elif page == "🎯 آية عشوائية":
    st.markdown("### 🎯 آية عشوائية للتدبر والاستماع")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎲 احصل على آية", use_container_width=True):
            ayah, surah_name, surah_num = get_random_ayah()
            
            if ayah:
                st.balloons()
                ayah_number = ayah.get('numberInSurah', 0)
                
                st.markdown(f"""
                <div class="ayah-card" style="border-right-color: #c9a84c;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="verse-counter">🎯 عشوائية</span>
                    </div>
                    <div class="ayah-arabic" style="font-size:2.2rem;">{ayah.get('text', '')}</div>
                    <div class="surah-name">— {surah_name} ({surah_num}) : {ayah_number}</div>
                    <div class="ayah-translation">"{ayah.get('translation', {}).get('en', 'Translation not available')}"</div>
                </div>
                """, unsafe_allow_html=True)
                
                audio_url = get_audio_url(surah_num, ayah_number)
                st.markdown("#### 🎧 استمع للتلاوة")
                st.audio(audio_url, format="audio/mp3")
            else:
                st.error("❌ تعذر جلب آية. يرجى المحاولة مرة أخرى.")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#888; padding:1rem;">
        <p>💡 اضغط على الزر للحصول على آية عشوائية مع إمكانية الاستماع إليها</p>
    </div>
    """, unsafe_allow_html=True)

# ========== صفحة البحث ==========
elif page == "🔍 البحث":
    st.markdown("### 🔍 البحث في القرآن")
    
    keyword = st.text_input("🔎 أدخل كلمة للبحث", placeholder="مثال: رحمة")
    
    if keyword:
        with st.spinner("⏳ جاري البحث..."):
            results = search_ayahs(keyword)
        
        if results:
            st.success(f"✅ تم العثور على {len(results)} نتيجة")
            for r in results:
                st.markdown(f"""
                <div class="ayah-card" style="border-right-color: #c9a84c;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="verse-counter">📖 {r.get('surah', '')} : {r.get('ayah_number', 0)}</span>
                    </div>
                    <div class="ayah-arabic" style="font-size:1.8rem;">{r.get('text', '')}</div>
                    <div class="ayah-translation">"{r.get('translation', 'Translation not available')}"</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("❌ لم يتم العثور على نتائج")

# ========== صفحة عن الموقع ==========
elif page == "📊 عن الموقع":
    st.markdown("### 📊 عن الموقع")
    
    st.markdown("""
    <div style="background: #f8f4ec; padding: 2rem; border-radius: 15px;">
        <h3 style="color: #1a472a;">🕌 موقع القرآن الإبداعي مع التلاوة</h3>
        <p style="color: #444; line-height: 1.8;">
            هذا موقع تفاعلي لقراءة وتدبر آيات القرآن الكريم، مع إضافة خاصية <strong>الاستماع إلى التلاوة</strong> 
            بصوت القارئ <strong>مشاري راشد العفاسي</strong>.
        </p>
        <hr>
        <h4 style="color: #1a472a;">✨ المميزات الجديدة</h4>
        <ul style="color: #444; line-height: 2;">
            <li>📖 <strong>قراءة القرآن</strong> - تصفح جميع السور مع الترجمة</li>
            <li>🎧 <strong>خاصية التلاوة</strong> - استمع لكل آية على حدة بصوت العفاسي (رابط يعمل 100%)</li>
            <li>🎯 <strong>آية عشوائية</strong> - احصل على آية مع إمكانية الاستماع الفوري</li>
            <li>🔍 <strong>بحث</strong> - ابحث عن كلمات في آيات القرآن</li>
        </ul>
        <hr>
        <p style="color: #888; font-size: 0.9rem;">
            📌 تم الإنشاء بواسطة Streamlit • البيانات من Quran Cloud API
        </p>
        <p style="color: #888; font-size: 0.9rem;">
            📅 { التاريخ }
        </p>
    </div>
    """.replace("{ التاريخ }", datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)

# ========== التذييل ==========
st.markdown("""
<div class="footer">
    🕌 القرآن الكريم • موقع إبداعي للقراءة والتدبر والاستماع • 
    <span style="direction: ltr;">"وَلَقَدْ يَسَّرْنَا الْقُرْآنَ لِلذِّكْرِ"</span>
</div>
""", unsafe_allow_html=True)
