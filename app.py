import streamlit as st
import requests
import random
import json
from datetime import datetime

# ========== 页面配置 ==========
st.set_page_config(
    page_title="القرآن الكريم - موقع إبداعي",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== 样式 ==========
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
        padding: 2rem;
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
    </style>
""", unsafe_allow_html=True)

# ========== API 函数 ==========
QURAN_API_BASE = "https://api.alquran.cloud/v1"

def get_all_surahs():
    """获取所有古兰经章节列表"""
    try:
        response = requests.get(f"{QURAN_API_BASE}/surah")
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
    except:
        pass
    return []

def get_ayahs(surah_number, start=1, end=10):
    """获取指定章节的经文"""
    try:
        response = requests.get(f"{QURAN_API_BASE}/surah/{surah_number}")
        if response.status_code == 200:
            data = response.json()
            ayahs = data.get('data', {}).get('ayahs', [])
            # 过滤指定范围的经文
            filtered = [a for a in ayahs if start <= a.get('numberInSurah', 0) <= end]
            return filtered
    except:
        pass
    return []

def get_random_ayah():
    """获取随机经文"""
    try:
        # 随机选择一个章节
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
    """搜索经文（通过API）"""
    # 注意：alquran.cloud API 不支持直接搜索
    # 这里使用简单模拟：获取所有章节并搜索
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

# ========== 侧边栏 ==========
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3047/3047924.png", width=80)
    st.markdown("### 🕋 القائمة")
    
    # 导航
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

# ========== 页面：首页 ==========
if page == "🏠 الرئيسية":
    st.markdown("""
    <div class="main-header">
        <h1>🕌 القرآن الكريم</h1>
        <p>موقع إبداعي لقراءة وتدبر آيات الله</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 特色功能卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📖</h3>
            <h3>قراءة</h3>
            <p style="color:#666; font-size:0.9rem;">تصفح سور القرآن<br>باللغتين العربية والإنجليزية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯</h3>
            <h3>آية عشوائية</h3>
            <p style="color:#666; font-size:0.9rem;">آيات عشوائية للتدبر<br>والتأمل اليومي</p>
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
            <h3>💡</h3>
            <h3>تدبر</h3>
            <p style="color:#666; font-size:0.9rem;">تأمل في معاني الآيات<br>وتدبر كلمات الله</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 随机推荐经文
    st.markdown("---")
    st.markdown("### 🌟 آية اليوم")
    
    ayah, surah_name, surah_num = get_random_ayah()
    if ayah:
        st.markdown(f"""
        <div class="ayah-card">
            <div class="ayah-arabic">{ayah.get('text', '')}</div>
            <div class="surah-name">— {surah_name} ({surah_num}) : {ayah.get('numberInSurah', 0)}</div>
            <div class="ayah-translation">"{ayah.get('translation', {}).get('en', 'Translation not available')}"</div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🔄 تحديث الآية"):
        st.rerun()

# ========== 页面：阅读 ==========
elif page == "📖 القراءة":
    st.markdown("### 📖 تصفح القرآن")
    
    # 获取所有章节
    surahs = get_all_surahs()
    
    if surahs:
        # 创建章节选择
        surah_names = [f"{s.get('number', 0)}. {s.get('name', '')} ({s.get('englishName', '')})" for s in surahs]
        selected = st.selectbox("اختر سورة", surah_names, index=0)
        
        if selected:
            # 获取章节编号
            surah_number = int(selected.split('.')[0])
            
            # 获取章节详情
            surah_data = next((s for s in surahs if s.get('number') == surah_number), None)
            if surah_data:
                total_ayahs = surah_data.get('numberOfAyahs', 10)
                
                col1, col2 = st.columns(2)
                with col1:
                    start = st.number_input("من الآية", min_value=1, max_value=total_ayahs, value=1)
                with col2:
                    end = st.number_input("إلى الآية", min_value=start, max_value=total_ayahs, value=min(start+9, total_ayahs))
                
                if st.button("📖 اقرأ", use_container_width=True):
                    ayahs = get_ayahs(surah_number, start, end)
                    
                    if ayahs:
                        st.markdown(f"""
                        <div style="text-align:center; margin: 1rem 0;">
                            <span class="verse-counter">📖 {surah_data.get('name', '')} — {len(ayahs)} آيات</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        for ayah in ayahs:
                            st.markdown(f"""
                            <div class="ayah-card">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <span class="verse-counter">🕌 {ayah.get('numberInSurah', 0)}</span>
                                </div>
                                <div class="ayah-arabic">{ayah.get('text', '')}</div>
                                <div class="ayah-translation">"{ayah.get('translation', {}).get('en', 'Translation not available')}"</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ لم يتم العثور على آيات")
    else:
        st.error("❌ تعذر تحميل قائمة السور. يرجى التحقق من اتصال الإنترنت.")

# ========== 页面：随机经文 ==========
elif page == "🎯 آية عشوائية":
    st.markdown("### 🎯 آية عشوائية للتدبر")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎲 احصل على آية", use_container_width=True):
            ayah, surah_name, surah_num = get_random_ayah()
            
            if ayah:
                st.balloons()
                st.markdown(f"""
                <div class="ayah-card" style="border-right-color: #c9a84c;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="verse-counter">🎯 عشوائية</span>
                    </div>
                    <div class="ayah-arabic" style="font-size:2.2rem;">{ayah.get('text', '')}</div>
                    <div class="surah-name">— {surah_name} ({surah_num}) : {ayah.get('numberInSurah', 0)}</div>
                    <div class="ayah-translation">"{ayah.get('translation', {}).get('en', 'Translation not available')}"</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ تعذر جلب آية. يرجى المحاولة مرة أخرى.")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#888; padding:1rem;">
        <p>💡 اضغط على الزر للحصول على آية عشوائية للتدبر والتأمل</p>
    </div>
    """, unsafe_allow_html=True)

# ========== 页面：搜索 ==========
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

# ========== 页面：关于 ==========
elif page == "📊 عن الموقع":
    st.markdown("### 📊 عن الموقع")
    
    st.markdown("""
    <div style="background: #f8f4ec; padding: 2rem; border-radius: 15px;">
        <h3 style="color: #1a472a;">🕌 موقع القرآن الإبداعي</h3>
        <p style="color: #444; line-height: 1.8;">
            هذا موقع تفاعلي لقراءة وتدبر آيات القرآن الكريم، تم بناؤه باستخدام 
            <strong>Streamlit</strong> و <strong>Quran Cloud API</strong>.
        </p>
        <hr>
        <h4 style="color: #1a472a;">✨ المميزات</h4>
        <ul style="color: #444; line-height: 2;">
            <li>📖 <strong>قراءة القرآن</strong> - تصفح جميع سور القرآن مع الترجمة</li>
            <li>🎯 <strong>آية عشوائية</strong> - احصل على آية عشوائية للتدبر اليومي</li>
            <li>🔍 <strong>بحث</strong> - ابحث عن كلمات في آيات القرآن</li>
            <li>🌙 <strong>واجهة عربية</strong> - تصميم أنيق باللغة العربية</li>
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

# ========== 页脚 ==========
st.markdown("""
<div class="footer">
    🕌 القرآن الكريم • موقع إبداعي للقراءة والتدبر • 
    <span style="direction: ltr;">"وَلَقَدْ يَسَّرْنَا الْقُرْآنَ لِلذِّكْرِ"</span>
</div>
""", unsafe_allow_html=True)
