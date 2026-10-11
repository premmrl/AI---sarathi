import streamlit as st
from google import genai

# १. पेज कॉन्फिगरेशन
st.set_page_config(
    page_title="ॐ AI सारथी | Gita AI Guide",
    page_icon="🕉️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# २. पर्सपेक्टिव्ह A: 'दिव्य रथ व कुरुक्षेत्र' (Celestial Chariot & Divine Gold Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Mukta:wght@300;400;600;700;800&display=swap');

    /* दिव्य आकाशीय व सात्विक पार्श्वभूमी (Celestial Midnight Cosmic Aura) */
    .stApp {
        background: radial-gradient(circle at 50% -10%, #2e1065 0%, #1e1b4b 35%, #0f172a 70%, #030712 100%) !important;
        font-family: 'Mukta', sans-serif !important;
        color: #f8fafc !important;
    }

    /* मुख्य हेडर कार्ड (Hero Card - Celestial Chariot Aura) */
    .hero-card {
        position: relative;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.07) 0%, rgba(217, 119, 6, 0.1) 100%);
        border: 1.5px solid rgba(251, 191, 36, 0.55);
        border-radius: 24px;
        padding: 26px 20px 22px 20px;
        text-align: center;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.65), 0 0 28px rgba(245, 158, 11, 0.25);
        backdrop-filter: blur(16px);
        margin-bottom: 18px;
    }

    .om-icon {
        font-size: 48px;
        line-height: 1.1;
        filter: drop-shadow(0 0 18px rgba(251, 191, 36, 0.9));
        margin-bottom: 4px;
        animation: pulseGlow 3s infinite alternate;
    }

    @keyframes pulseGlow {
        0% { transform: scale(1); filter: drop-shadow(0 0 12px rgba(251, 191, 36, 0.7)); }
        100% { transform: scale(1.05); filter: drop-shadow(0 0 22px rgba(251, 191, 36, 1)); }
    }

    .title-glow {
        font-size: 40px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFDF0 0%, #FEF08A 25%, #F59E0B 65%, #B45309 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
        margin: 4px 0 8px 0;
        filter: drop-shadow(0 2px 10px rgba(245, 158, 11, 0.4));
    }

    .sub-tagline {
        color: #e2e8f0;
        font-size: 15px;
        font-weight: 400;
        line-height: 1.6;
        opacity: 0.95;
    }

    /* भाषा निवड लेबल */
    .stSelectbox label p {
        color: #FDE68A !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 4px !important;
    }

    /* भाषा निवड ड्रॉपडाऊन बॉक्स */
    div[data-baseweb="select"] {
        border-radius: 14px !important;
        border: 1.2px solid rgba(251, 191, 36, 0.55) !important;
        background-color: rgba(30, 41, 59, 0.8) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35) !important;
    }

    div[data-baseweb="select"] * {
        color: #FEF08A !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    ul[data-baseweb="menu"] {
        background-color: #0f172a !important;
        border: 1px solid rgba(251, 191, 36, 0.45) !important;
    }

    ul[data-baseweb="menu"] li {
        color: #f8fafc !important;
        font-size: 14.5px !important;
    }

    /* रेडिओ बटन्स - सुवर्ण प्रभाव असणारे पिल्स */
    div[role="radiogroup"] {
        display: flex !important;
        justify-content: center !important;
        background: rgba(30, 41, 59, 0.65) !important;
        padding: 6px !important;
        border-radius: 30px !important;
        border: 1px solid rgba(251, 191, 36, 0.4) !important;
        gap: 8px !important;
        margin: 12px 0 18px 0 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
    }

    div[role="radiogroup"] label {
        padding: 8px 18px !important;
        border-radius: 20px !important;
        background: transparent !important;
        color: #f8fafc !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    /* इनपुट बॉक्स स्टाईल */
    div[data-baseweb="textarea"] {
        background-color: rgba(30, 41, 59, 0.85) !important;
        border: 1px solid rgba(251, 191, 36, 0.35) !important;
        border-radius: 16px !important;
    }

    /* तळटीप व संस्था ब्रँडिंग */
    .footer-container {
        text-align: center;
        margin-top: 42px;
        padding-top: 22px;
        border-top: 1px solid rgba(251, 191, 36, 0.25);
    }

    .brand-title {
        color: #FCD34D;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .footer-text {
        color: #cbd5e1;
        font-size: 13px;
        line-height: 1.6;
    }

    /* भेट देणारे साधक बॅज */
    .visitor-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(251, 191, 36, 0.6);
        color: #FEF08A;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin-top: 14px;
        box-shadow: 0 0 14px rgba(245, 158, 11, 0.25);
    }
    </style>
""", unsafe_allow_html=True)

# ३. स्थानिक भाषांतर डेटा (१० भाषा)
LOCALIZED_CONTENT = {
    "मराठी": {
        "title": "AI सारथी",
        "tagline": "जीवनातील आणि व्यवसायातील गुंतागुंतीच्या निर्णयांना भगवद्गीतेच्या दिव्य प्रकाशात अचूक दिशा",
        "modes": [
            "🌱 वैयक्तिक जीवन (Personal Guidance)",
            "💼 व्यवसाय आणि करिअर (Business & Career)"
        ],
        "placeholder": "आपला प्रश्न, चिंता किंवा द्विधा मनःस्थिती येथे मांडा...",
        "foundation_text": "प्रकल्प संकल्पना व संचलन: <b>विघ्नहर्ता गोल्ड फाउंडेशन</b><br>भगवद्गीतेच्या कालातीत तत्त्वांवर आधारित समाजहितैषी डिजिटल उपक्रम",
        "visitor_label": "एकूण भेट देणारे साधक:"
    },
    "हिंदी": {
        "title": "AI सारथी",
        "tagline": "जीवन और व्यापार के कठिन निर्णयों को भगवद्गीता के दिव्य प्रकाश में सही दिशा",
        "modes": [
            "🌱 व्यक्तिगत जीवन (Personal Guidance)",
            "💼 व्यवसाय और करियर (Business & Career)"
        ],
        "placeholder": "अपना प्रश्न, दुविधा या चिंता यहाँ लिखें...",
        "foundation_text": "परिकल्पना एवं संचालन: <b>विघ्नहर्ता गोल्ड फाउंडेशन</b><br>भगवद्गीता के शाश्वत सिद्धांतों पर आधारित सामाजिक डिजिटल पहल",
        "visitor_label": "कुल आगंतुक साधक:"
    },
    "English": {
        "title": "AI Sarathi",
        "tagline": "Guiding life and business decisions in the divine light of the Bhagavad Gita",
        "modes": [
            "🌱 Personal Life & Inner Peace",
            "💼 Business, Leadership & Career"
        ],
        "placeholder": "Ask your question, dilemma, or life situation here...",
        "foundation_text": "Initiative by <b>Vighnaharta Gold Foundation</b><br>A digital guide rooted in the timeless wisdom of the Bhagavad Gita",
        "visitor_label": "Total Seekers Visited:"
    },
    "ગુજરાતી": {
        "title": "AI સારથી",
        "tagline": "જીવન અને વેપારના નિર્ણયોને ભગવદ્ગીતાના દિવ્ય પ્રકાશમાં સચોટ માર્ગદર્શન",
        "modes": [
            "🌱 વ્યક્તિગત જીવન (Personal Guidance)",
            "💼 વ્યવસાય અને કારકિર્દી (Business & Career)"
        ],
        "placeholder": "તમારો પ્રશ્ન કે મૂંઝવણ અહીં લખો...",
        "foundation_text": "સંચાલન: <b>વિઘ્નહર્તા ગોલ્ડ ફાઉન્ડેશન</b><br>ભગવદ્ગીતાના શાશ્વત સિદ્ધાંતો પર આધારિત ડિજિટલ પહેલ",
        "visitor_label": "કુલ મુલાકાતી સાધકો:"
    },
    "ಕನ್ನಡ": {
        "title": "AI ಸಾರಥಿ",
        "tagline": "ಭಗವದ್ಗೀತೆಯ ದಿವ್ಯ ಬೆಳಕಿನಲ್ಲಿ ಜೀವನ ಮತ್ತು ವ್ಯವಹಾರದ ನಿರ್ಧಾರಗಳಿಗೆ ಸೂಕ್ತ ಮಾರ್ಗದರ್ಶನ",
        "modes": [
            "🌱 ವೈಯಕ್ತಿಕ ಜೀವನ (Personal Life)",
            "💼 ಉದ್ಯೋಗ ಮತ್ತು ವ್ಯಾಪಾರ (Business & Career)"
        ],
        "placeholder": "ನಿಮ್ಮ ಪ್ರಶ್ನೆ ಅಥವಾ ಸಂದೇಹವನ್ನು ಇಲ್ಲಿ ಹಂಚಿಕೊಳ್ಳಿ...",
        "foundation_text": "ಉಪಕ್ರಮ: <b>ವಿಘ್ನಹರ್ತಾ ಗೋಲ್ಡ್ ಫೌಂಡೇಶನ್</b><br>ಭಗವದ್ಗೀತೆಯ ತತ್ವಗಳ ಆಧಾರಿತ ಮಾರ್ಗದರ್ಶಿ",
        "visitor_label": "ಒಟ್ಟು ಭೇಟಿ ನೀಡಿದ ಸಾಧಕರು:"
    },
    "తెలుగు": {
        "title": "AI సారథి",
        "tagline": "భగవద్గీత దివ్య వెలుగులో జీవిత మరియు వ్యాపార నిర్ణయాలకు సరైన దిశా నిర్దేశం",
        "modes": [
            "🌱 వ్యక్తిగత జీవితం (Personal Life)",
            "💼 వ్యాపారం & వృత్తి (Business & Career)"
        ],
        "placeholder": "మీ ప్రశ్న లేదా సందేహాన్ని ఇక్కడ అడగండి...",
        "foundation_text": "సంకల్పం: <b>విఘ్నహర్త గోల్డ్ ఫౌండేషన్</b><br>భగవద్గీత శాశ్వత సూత్రాలపై ఆధారపడిన డిజిటల్ చొరవ",
        "visitor_label": "మొత్తం సందర్శించిన సాధకులు:"
    },
    "தமிழ்": {
        "title": "AI சாரதி",
        "tagline": "பகவத் கீதையின் தெய்வீக ஒளியில் வாழ்க்கை மற்றும் வணிக முடிவுகளுக்கு தெளிவான வழிகாட்டுதல்",
        "modes": [
            "🌱 தனிப்பட்ட வாழ்க்கை (Personal Life)",
            "💼 வணிகம் & தொழில் (Business & Career)"
        ],
        "placeholder": "உங்கள் கேள்வி அல்லது கவலையை இங்கே பகிருங்கள்...",
        "foundation_text": "முயற்சி: <b>விக்னஹர்த்தா கோல்ட் ஃபவுண்டேஷன்</b><br>பகவத் கீதையின் வழிகாட்டுதல் திட்டம்",
        "visitor_label": "பார்வையிட்ட பக்தர்கள்:"
    },
    "বাংলা": {
        "title": "AI সারথি",
        "tagline": "ভগবদ্গীতার দিব্য আলোকে জীবন ও ব্যবসার সিদ্ধান্তের সঠিক পথনির্দেশ",
        "modes": [
            "🌱 व्यक्तिगत जीवन (Personal Guidance)",
            "💼 व्यवसाय ও कर्मजीवन (Business & Career)"
        ],
        "placeholder": "আপনার প্রশ্ন বা সংশয় এখানে লিখুন...",
        "foundation_text": "উদ্যোগ: <b>বিঘ্নহর্তা গোল্ড ফাউন্ডেশন</b><br>শ্রীমদ্ভগবদ্গীতার কালজয়ী নির্দেশিকা",
        "visitor_label": "মোট দর্শনার্থী সাধক:"
    },
    "മലയാളം": {
        "title": "AI സാരഥി",
        "tagline": "ഭഗവദ്ഗീതയുടെ ദിവ്യവെളിച്ചത്തിൽ ജീവിതത്തിലെയും ബിസിനസ്സിലെയും തീരുമാനങ്ങൾക്ക് കൃത്യമായ വഴികാട്ടി",
        "modes": [
            "🌱 വ്യക്തിജീവിതം (Personal Guidance)",
            "💼 ബിസിനസ്സും കരിയറും (Business & Career)"
        ],
        "placeholder": "നിങ്ങളുടെ ചോദ്യം ഇവിടെ കുറിക്കുക...",
        "foundation_text": "സംരംഭം: <b>വിഘ്നഹർത്ത ഗോൾഡ് ഫൗണ്ടേഷൻ</b><br>ഭഗവദ്ഗീതാ തത്വങ്ങളുടെ ഡിജിറ്റൽ മാർഗ്ഗരേഖ",
        "visitor_label": "ആകെ സന്ദർശിച്ചവർ:"
    },
    "ਪੰਜਾਬੀ": {
        "title": "AI ਸਾਰਥੀ",
        "tagline": "ਭਗਵਦ ਗੀਤਾ ਦੇ ਦਿਵਯ ਚਾਨਣ ਵਿੱਚ ਜ਼ਿੰਦਗੀ ਅਤੇ ਕਾਰੋਬਾਰ ਦੇ ਫੈਸਲਿਆਂ ਲਈ ਸਹੀ ਦਿਸ਼ਾ",
        "modes": [
            "🌱 ਨਿੱਜੀ ਜੀਵਨ (Personal Guidance)",
            "💼 ਕਾਰੋਬਾਰ ਅਤੇ ਕਰੀਅਰ (Business & Career)"
        ],
        "placeholder": "ਆਪਣਾ ਸਵਾਲ ਜਾਂ ਦੁਵਿਧਾ ਇੱਥੇ ਪੁੱਛੋ...",
        "foundation_text": "ਉਪਰਾਲਾ: <b>ਵਿਘਨਹਰਤਾ ਗੋਲਡ ਫਾਊਂਡੇਸ਼ਨ</b><br>ਭਗਵਦ ਗੀਤਾ ਦੇ ਸਿਧਾਂਤਾਂ 'ਤੇ ਆਧਾਰਿਤ ਡਿਜੀਟਲ ਪਹਿਲ",
        "visitor_label": "ਕੁੱਲ ਸਾਧਕ:"
    }
}

if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = "मराठी"

curr = LOCALIZED_CONTENT[st.session_state.selected_lang]

# ४. मुख्य हेडर कार्ड (पर्सपेक्टिव्ह A)
st.markdown(f"""
    <div class="hero-card">
        <div class="om-icon">🕉️</div>
        <div class="title-glow">{curr["title"]}</div>
        <div class="sub-tagline">{curr["tagline"]}</div>
    </div>
""", unsafe_allow_html=True)

# ५. हेडर कार्डच्या खाली ज्या ठिकाणी आहे तिथेच भाषा निवड
LANGUAGES = list(LOCALIZED_CONTENT.keys())
chosen_lang = st.selectbox(
    "🌐 भाषा निवडा / Choose Language:",
    LANGUAGES,
    index=LANGUAGES.index(st.session_state.selected_lang)
)

if chosen_lang != st.session_state.selected_lang:
    st.session_state.selected_lang = chosen_lang
    st.rerun()

# ६. मार्गदर्शन विभाग (वैयक्तिक / व्यवसाय)
selected_mode = st.radio(
    "मार्गदर्शन क्षेत्र:",
    curr["modes"],
    horizontal=True,
    label_visibility="collapsed"
)

# ७. सिस्टीम प्रॉम्ट
system_prompt = (
    "तू 'AI सारथी' आहेस - भगवद्गीतेच्या तत्त्वज्ञानावर आधारित एक ज्ञानी, शांत, संवेदनशील आणि मार्गदर्शक डिजिटल मित्र. "
    "हा उपक्रम 'विघ्नहर्ता गोल्ड फाउंडेशन' यांच्या संकल्पनेतून चालवला जात आहे. "
    f"वापरकर्त्याने निवडलेली भाषा: {st.session_state.selected_lang}. निवडलेला विभाग: {selected_mode}. "
    "महत्त्वाचे नियम: "
    f"१. संपूर्ण उत्तर १००% शुद्ध, आदरार्थी आणि सहज समजणाऱ्या {st.session_state.selected_lang} भाषेतच दे. "
    "२. उत्तरात थेट भगवद्गीतेतील समर्पक श्लोक किंवा श्रीकृष्ण-अर्जुन संवादाचा सारांश देऊन व्यावहारिक समुपदेशन कर. "
    "३. कर्म, धर्म, अनासक्ती, मनःशांती आणि निर्णयक्षमतेवर भर दे."
)

# ८. Google GenAI क्लायंट
api_token = st.secrets.get("GEMINI_API_KEY", "").strip()

if not api_token:
    st.info("कृपया Streamlit Secrets मध्ये GEMINI_API_KEY जोडा.", icon="ℹ️")
    st.stop()

@st.cache_resource(show_spinner=False)
def init_genai_client(key):
    return genai.Client(api_key=key)

client = init_genai_client(api_token)

# ९. वेगवान स्ट्रीमिंग रिस्पॉन्स
def stream_sarathi_response(query):
    prompt_with_context = f"{system_prompt}\n\n[विभाग: {selected_mode}]\nप्रश्न: {query}"
    response_stream = client.models.generate_content_stream(
        model="gemini-3.8-flash",
        contents=prompt_with_context
    )
    for chunk in response_stream:
        if chunk.text:
            yield chunk.text

# १०. चॅट हिस्ट्री
if "sarathi_messages" not in st.session_state:
    st.session_state.sarathi_messages = []

for message in st.session_state.sarathi_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ११. प्रश्न इनपुट बॉक्स
if user_prompt := st.chat_input(curr["placeholder"]):
    st.session_state.sarathi_messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        try:
            full_response = st.write_stream(stream_sarathi_response(user_prompt))
            st.session_state.sarathi_messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"तांत्रिक अडचण: {str(e)}")

# १२. तळटीप ब्रँडिंग आणि २७९ वरून आपोआप पुढे वाढणारा रिअल-टाईम व्हिजिटर काउंटर
st.markdown(f"""
    <div class="footer-container">
        <div class="brand-title">AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION</div>
        <div class="footer-text">{curr["foundation_text"]}</div>
        <div class="visitor-badge">
            👁️ {curr["visitor_label"]} 
            <img src="https://komarev.com/ghpvc/?username=vighnaharta-ai-sarathi-live&base=279&color=f59e0b&style=flat-square&label=Views" alt="Views" style="vertical-align: middle; margin-left: 6px; border-radius: 4px;">
        </div>
    </div>
""", unsafe_allow_html=True)
