import streamlit as st
import time
from google import genai

# १. पेज सेटिंग्ज
st.set_page_config(
    page_title="AI सारथी | Gita AI Guide",
    page_icon="🕉️",
    layout="centered"
)

# २. स्टाईल (CSS)
st.markdown("""
    <style>
    .footer-container {
        text-align: center;
        margin-top: 55px;
        padding-top: 18px;
        border-top: 1px solid #333333;
    }
    .brand-title {
        font-size: 13px;
        color: #d4af37;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .footer-text {
        color: #888888;
        font-size: 12px;
        margin-top: 4px;
        line-height: 1.5;
    }
    .stRadio > div {
        display: flex;
        justify-content: center;
        gap: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ३. भाषा निवड (भारतातील प्रमुख १० भाषा)
LANGUAGES = [
    "मराठी", 
    "हिंदी", 
    "English", 
    "ગુજરાતી (Gujarati)", 
    "ಕನ್ನಡ (Kannada)", 
    "తెలుగు (Telugu)", 
    "தமிழ் (Tamil)", 
    "বাংলা (Bengali)", 
    "മലയാളം (Malayalam)", 
    "ਪੰਜਾਬੀ (Punjabi)"
]

language = st.selectbox(
    "🌐 Choose Language / भाषा निवडा / अपनी भाषा चुनें:",
    LANGUAGES
)

# ४. भाषेनुसार स्थानिक डेटा (शीर्षक, ब्रँडिंग व मोड्स)
LOCALIZATION = {
    "मराठी": {
        "title": "🕉️ AI सारथी",
        "caption": "तुमच्या जीवनातील व व्यवसायातील प्रश्नांवर भगवद्गीतेच्या प्रकाशात अचूक मार्गदर्शन",
        "modes": ["🌱 वैयक्तिक जीवन (Personal Guidance)", "💼 व्यवसाय आणि करिअर (Business & Career)"],
        "input_placeholder": "तुमचा प्रश्न किंवा अडचण येथे मांडा...",
        "thinking": "सारथी विचारमंथन करत आहेत...",
        "brand_title": "AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION",
        "brand_desc": "प्रकल्प संकल्पना व संचलन: <b>विघ्नहर्ता गोल्ड फाउंडेशन</b><br>भगवद्गीतेच्या कालातीत तत्त्वांवर आधारित समाजहितैषी डिजिटल उपक्रम"
    },
    "हिंदी": {
        "title": "🕉️ AI सारथी",
        "caption": "जीवन और व्यापार के कठिन प्रश्नों का भगवद्गीता के प्रकाश में सटीक समाधान",
        "modes": ["🌱 व्यक्तिगत जीवन (Personal Life)", "💼 व्यापार और करियर (Business & Career)"],
        "input_placeholder": "अपनी समस्या या प्रश्न यहाँ लिखें...",
        "thinking": "सारथी विचार कर रहे हैं...",
        "brand_title": "AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION",
        "brand_desc": "प्रकल्प संकल्पना एवं संचालन: <b>विघ्नहर्ता गोल्ड फाउंडेशन</b><br>भगवद्गीता के सिद्धांतों पर आधारित समाजोपयोगी डिजिटल पहल"
    },
    "English": {
        "title": "🕉️ AI Sarathi",
        "caption": "Timeless Wisdom from the Bhagavad Gita for Personal & Professional Life",
        "modes": ["🌱 Personal Life", "💼 Business & Career"],
        "input_placeholder": "Type your situation or question here...",
        "thinking": "Sarathi is contemplating...",
        "brand_title": "AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION",
        "brand_desc": "Project Conception & Governance: <b>Vighnaharta Gold Foundation</b><br>A Digital Initiative Grounded in Bhagavad Gita Wisdom"
    },
    "ગુજરાતી (Gujarati)": {
        "title": "🕉️ AI સારથી",
        "caption": "જીવન અને વ્યવસાયના પ્રશ્નોનું ભગવદ્ગીતાના પ્રકાશમાં સચોટ માર્ગદર્શન",
        "modes": ["🌱 વ્યક્તિગત જીવન (Personal)", "💼 વ્યાપાર અને કારકિર્દી (Business)"],
        "input_placeholder": "તમારો પ્રશ્ન કે સમસ્યા અહીં લખો...",
        "thinking": "સારથી ચિંતન કરી રહ્યા છે...",
        "brand_title": "AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION",
        "brand_desc": "આયોજન અને સંચાલન: <b>વિઘ્નહર્તા ગોલ્ડ ફાઉન્ડેશન</b><br>ભગવદ્ગીતાના મૂલ્યો પર આધારિત ડિજિટલ સેવાયજ્ઞ"
    },
    "ಕನ್ನಡ (Kannada)": {
        "title": "🕉️️ AI ಸಾರಥಿ",
        "caption": "ವೈಯಕ್ತಿಕ ಜೀವನ ಮತ್ತು ವ್ಯಾಪಾರದ ಸಮಸ್ಯೆಗಳಿಗೆ ಭಗವದ್ಗೀತೆಯ ಬೆಳಕಿನಲ್ಲಿ ಮಾರ್ಗದರ್ಶನ",
        "modes": ["🌱 ವೈಯಕ್ತಿಕ ಜೀವನ (Personal)", "💼 ವ್ಯಾಪಾರ ಮತ್ತು ವೃತ್ತಿ (Business)"],
        "input_placeholder": "ನಿಮ್ಮ ಪ್ರಶ್ನೆ ಅಥವಾ ಸವಾಲನ್ನು ಇಲ್ಲಿ ಬರೆಯಿರಿ...",
        "thinking": "ಸಾರಥಿ ಆಲೋಚಿಸುತ್ತಿದ್ದಾರೆ...",
        "brand_title": "AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION",
        "brand_desc": "ಪರಿಕಲ್ಪನೆ ಮತ್ತು ನಿರ್ವಹಣೆ: <b>ವಿಘ್ನಹರ್ತಾ ಗೋಲ್ಡ್ ಫೌಂಡೇಶನ್</b><br>ಭಗವದ್ಗೀತೆಯ ತತ್ವಗಳ ಆಧಾರಿತ ಸಾಮಾಜಿಕ ಡಿಜಿಟಲ್ ಉಪಕ್ರಮ"
    },
    "తెలుగు (Telugu)": {
        "title": "🕉️ AI సారథి",
        "caption": "జీవితం మరియు వ్యాపార నిర్ణయాలకు భగవద్గీత వెలుగులో సరైన మార్గదర్శనం",
        "modes": ["🌱 వ్యక్తిగత జీవితం (Personal)", "💼 వ్యాపారం & వృత్తి (Business)"],
        "input_placeholder": "మీ ప్రశ్నను ఇక్కడ నమోదు చేయండి...",
        "thinking": "సారథి ఆలోచిస్తున్నారు...",
        "brand_title": "AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION",
        "brand_desc": "రూపకల్పన & నిర్వహణ: <b>విఘ్నహర్త గోల్డ్ ఫౌండేషన్</b><br>భగవద్గీత సందేశంతో ప్రజోపయోగ డిజిటల్ వ్యవస్థ"
    },
    "தமிழ் (Tamil)": {
        "title": "🕉️ AI சாரதி",
        "caption": "தனிப்பட்ட வாழ்க்கை மற்றும் வணிக சவால்களுக்கு பகவத் கீதையின் வழிகாட்டுதல்",
        "modes": ["🌱 தனிப்பட்ட வாழ்க்கை (Personal)", "💼 வணிகம் & தொழில் (Business)"],
        "input_placeholder": "உங்கள் கேள்வி அல்லது சிக்கலை இங்கே எழுதுங்கள்...",
        "thinking": "சாரதி சிந்திக்கிறார்...",
        "brand_title": "AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION",
        "brand_desc": "உருவாக்கம் & வழிகாட்டல்: <b>விக்னஹர்தா கோல்ட் ஃபவுண்டேஷன்</b><br>பகவத் கீதையின் நல்வழியில் உருவான சேவை"
    },
    "বাংলা (Bengali)": {
        "title": "🕉️ AI সারথি",
        "caption": "ব্যক্তিগত জীবন ও ব্যবসার জটিল সমস্যার ভগবদ্গীতার আলোকে সমাধান",
        "modes": ["🌱 ব্যক্তিগত জীবন (Personal)", "💼 ব্যবসা ও ক্যারিয়ার (Business)"],
        "input_placeholder": "আপনার প্রশ্ন বা समस्या এখানে লিখুন...",
        "thinking": "সারথি চিন্তা করছেন...",
        "brand_title": "AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION",
        "brand_desc": "পরিকল্পনা ও রূপায়ণ: <b>বিঘ্নহর্তা গোল্ড ফাউন্ডেশন</b><br>ভগবদ্গীতার শিক্ষায় সমৃদ্ধ কল্যাণমুখী ডিজিটাল প্রয়াস"
    },
    "മലയാളം (Malayalam)": {
        "title": "🕉️ AI സാരഥി",
        "caption": "വ്യക്തിജീവിതത്തിലും ബിസിനസ്സിലും ഭഗവദ്ഗീതയുടെ വെളിച്ചത്തിൽ മാർഗ്ഗദർശനം",
        "modes": ["🌱 വ്യക്തിജീവിതം (Personal)", "💼 ബിസിനസ്സും കരിയറും (Business)"],
        "input_placeholder": "നിങ്ങളുടെ ചോദ്യം ഇവിടെ രേഖപ്പെടുത്തുക...",
        "thinking": "സാരഥി ചിന്തിക്കുന്നു...",
        "brand_title": "AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION",
        "brand_desc": "നേതൃത്വം: <b>വിഘ്നഹർത്താ ഗോൾഡ് ഫൗണ്ടേഷൻ</b><br>ഭഗവദ്ഗീതാ തത്വങ്ങളിൽ അധിഷ്ഠിതമായ ജനക്ഷേമ സംരംഭം"
    },
    "ਪੰਜਾਬੀ (Punjabi)": {
        "title": "🕉️ AI ਸਾਰਥੀ",
        "caption": "ਨਿੱਜੀ ਜੀਵਨ ਅਤੇ ਕਾਰੋਬਾਰ ਦੀਆਂ ਸਮੱਸਿਆਵਾਂ ਦਾ ਭਗਵਦ ਗੀਤਾ ਦੀ ਰੌਸ਼ਨੀ ਵਿੱਚ ਸਹੀ ਹੱਲ",
        "modes": ["🌱 ਨਿੱਜੀ ਜੀਵਨ (Personal)", "💼 ਕਾਰੋਬਾਰ ਅਤੇ ਕਰੀਅਰ (Business)"],
        "input_placeholder": "ਆਪਣਾ ਸਵਾਲ ਜਾਂ ਦੁਵਿਧਾ ਇੱਥੇ ਲਿਖੋ...",
        "thinking": "ਸਾਰਥੀ ਸੋਚ ਰਹੇ ਹਨ...",
        "brand_title": "AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION",
        "brand_desc": "ਸੰਕਲਪ ਅਤੇ ਪ੍ਰਬੰਧਨ: <b>ਵਿਘਨਹਰਤਾ ਗੋਲਡ ਫਾਊਂਡੇਸ਼ਨ</b><br>ਭਗਵਦ ਗੀਤਾ ਦੇ ਮਾਰਗ 'ਤੇ ਆਧਾਰਿਤ ਡਿਜੀਟਲ ਸੇਵਾ"
    }
}

content = LOCALIZATION.get(language, LOCALIZATION["मराठी"])

# ५. शीर्षके व मोड निवड
st.title(content["title"])
st.caption(content["caption"])

guidance_mode = st.radio(
    "मार्गदर्शन प्रकार निवडा:",
    content["modes"],
    horizontal=True,
    label_visibility="collapsed"
)

# ६. सिस्टीम मार्गदर्शक सूचना
SYSTEM_INSTRUCTION = f"""
तू 'AI सारथी' आहेस - एक निष्पक्ष मार्गदर्शक, मित्र आणि तत्त्वज्ञ.
सध्या निवडलेली भाषा: {language}
सध्या निवडलेला मोड: {guidance_mode}

महत्त्वाचे नियम:
१. वापरकर्त्याने निवडलेल्या भाषेतच ({language}) संपूर्ण उत्तर दे.
२. जर मोड 'व्यवसाय आणि करिअर' असेल, तर व्यावसायिक नीतिमत्ता, नेतृत्व, निर्णयक्षमता, रणनीती आणि कर्मयोगावर भर दे.
३. जर मोड 'वैयक्तिक जीवन' असेल, तर मानसिक शांतता, नातेसंबंध, ताणतणाव आणि आत्मसंयमावर मार्गदर्शन कर.
४. उत्तराची रचना:
   - समस्येचे मूळ कारण आणि तात्त्विक दिलासा.
   - भगवद्गीतेतील अचूक अध्याय आणि श्लोक संदर्भ (मूळ संस्कृत श्लोक + निवडलेल्या भाषेत सोपा अर्थ).
   - २ ते ३ व्यावहारिक, अमलात आणण्याजोगी पावले (Actionable Steps).
"""

# ७. API Key आणि Client व्यवस्थापन
api_key = st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    st.info("कृपया पुढे जाण्यासाठी API Key आवश्यक आहे.", icon="ℹ️")
    st.stop()

client = genai.Client(api_key=api_key)

# ८. उपलब्ध मॉडेल्स स्वयंचलित शोधणे (Dynamic Model Discovery)
@st.cache_resource(show_spinner=False)
def get_supported_model_list():
    try:
        available = []
        for m in client.models.list():
            # generateContent ला सपोर्ट करणारी आणि flash/pro असणारी मॉडेल्स शोधणे
            methods = getattr(m, "supported_generation_methods", []) or getattr(m, "supported_actions", [])
            m_name = m.name.replace("models/", "")
            if "flash" in m_name or "pro" in m_name:
                available.append(m_name)
        # प्राधान्यक्रम: आधी 3.8-flash, मग इतर
        if "gemini-3.8-flash" in available:
            available.remove("gemini-3.8-flash")
            available.insert(0, "gemini-3.8-flash")
        return available if available else ["gemini-3.8-flash"]
    except Exception:
        return ["gemini-3.8-flash"]

# ९. चॅट हिस्ट्री
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# १०. प्रश्न व उत्तर हाताळणी
if user_prompt := st.chat_input(content["input_placeholder"]):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner(content["thinking"]):
            full_prompt = f"{SYSTEM_INSTRUCTION}\n\n[क्षेत्र: {guidance_mode}]\nप्रश्न: {user_prompt}"
            
            models_to_try = get_supported_model_list()
            reply_text = None
            last_err = ""
            
            for m in models_to_try:
                for attempt in range(2):
                    try:
                        response = client.models.generate_content(
                            model=m,
                            contents=full_prompt
                        )
                        if response and response.text:
                            reply_text = response.text
                            break
                    except Exception as e:
                        last_err = str(e)
                        time.sleep(1)
                if reply_text:
                    break
            
            if reply_text:
                st.markdown(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})
            else:
                st.error(f"तांत्रिक माहिती: {last_err}")

# ११. तळाशी भाषेनुसार बदलणारे ब्रँडिंग
st.markdown(f"""
    <div class='footer-container'>
        <div class='brand-title'>{content["brand_title"]}</div>
        <div class='footer-text'>{content["brand_desc"]}</div>
    </div>
""", unsafe_allow_html=True)
