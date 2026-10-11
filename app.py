import streamlit as st
from google import genai

# १. पेज कॉन्फिगरेशन
st.set_page_config(
    page_title="ॐ AI सारथी | Gita AI Guide",
    page_icon="🕉️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# २. दिव्य, आधुनिक आणि फॉन्ट विझिबिलिटी सुधारित CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Mukta:wght@300;400;600;700;800&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 8%, #1f1830 0%, #0d0a14 100%) !important;
        font-family: 'Mukta', sans-serif !important;
        color: #f5f2eb !important;
    }

    /* मुख्य हेडर कार्ड */
    .hero-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(212, 175, 55, 0.04));
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 22px;
        padding: 24px 20px 20px 20px;
        text-align: center;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.55), 0 0 18px rgba(212, 175, 55, 0.12);
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
    }

    .om-icon {
        font-size: 44px;
        line-height: 1.1;
        filter: drop-shadow(0 0 12px rgba(255, 179, 0, 0.7));
        margin-bottom: 4px;
    }

    .title-glow {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFF176 0%, #FFD54F 40%, #FFA000 80%, #FF8F00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.8px;
        margin: 4px 0 8px 0;
        text-shadow: 0 0 25px rgba(255, 193, 7, 0.25);
    }

    .sub-tagline {
        color: #e4ddf2;
        font-size: 14.5px;
        font-weight: 400;
        line-height: 1.6;
        opacity: 0.95;
    }

    /* भाषा निवड ड्रॉपडाऊन अक्षरे स्पष्ट दिसण्यासाठी (Font Visibility Fix) */
    div[data-baseweb="select"] {
        border-radius: 12px !important;
        border: 1px solid rgba(212, 175, 55, 0.45) !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
    }

    div[data-baseweb="select"] * {
        color: #FFF59D !important; /* सोनेरी-पांढरी स्पष्ट अक्षरे */
        font-weight: 600 !important;
        font-size: 14.5px !important;
    }

    /* ड्रॉपडाऊन यादी (Dropdown Menu Items) */
    ul[data-baseweb="menu"] {
        background-color: #1a1528 !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
    }

    ul[data-baseweb="menu"] li {
        color: #ffffff !important;
    }

    ul[data-baseweb="menu"] li:hover {
        background-color: rgba(212, 175, 55, 0.2) !important;
        color: #FFD54F !important;
    }

    /* रेडिओ बटन्स */
    div[role="radiogroup"] {
        display: flex !important;
        justify-content: center !important;
        background: rgba(255, 255, 255, 0.04) !important;
        padding: 6px !important;
        border-radius: 30px !important;
        border: 1px solid rgba(212, 175, 55, 0.25) !important;
        gap: 8px !important;
        margin: 10px 0 16px 0 !important;
    }

    div[role="radiogroup"] label {
        padding: 8px 16px !important;
        border-radius: 20px !important;
        background: transparent !important;
        color: #ffffff !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
    }

    /* फुटर व संस्था ब्रँडिंग */
    .footer-container {
        text-align: center;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid rgba(212, 175, 55, 0.2);
    }

    .brand-title {
        color: #FFD54F;
        font-size: 12.5px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .footer-text {
        color: #c7bece;
        font-size: 12.5px;
        line-height: 1.6;
    }

    .visitor-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(212, 175, 55, 0.1);
        border: 1px solid rgba(212, 175, 55, 0.45);
        color: #FFE082;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12.5px;
        font-weight: 600;
        margin-top: 12px;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# ३. स्थानिक भाषांतर डेटा
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
            "🌱 ব্যক্তিগত জীবন (Personal Guidance)",
            "💼 ব্যবসা ও কর্মজীবন (Business & Career)"
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

# ४. मुख्य हेडर कार्ड
st.markdown(f"""
    <div class="hero-card">
        <div class="om-icon">🕉️</div>
        <div class="title-glow">{curr["title"]}</div>
        <div class="sub-tagline">{curr["tagline"]}</div>
    </div>
""", unsafe_allow_html=True)

# ५. कार्डच्या खाली भाषा निवड आणि विभाग पर्याय
LANGUAGES = list(LOCALIZED_CONTENT.keys())
chosen_lang = st.selectbox(
    "🌐 Choose Language / भाषा निवडा:",
    LANGUAGES,
    index=LANGUAGES.index(st.session_state.selected_lang),
    label_visibility="collapsed"
)

if chosen_lang != st.session_state.selected_lang:
    st.session_state.selected_lang = chosen_lang
    st.rerun()

selected_mode = st.radio(
    "मार्गदर्शन क्षेत्र:",
    curr["modes"],
    horizontal=True,
    label_visibility="collapsed"
)

# ६. सिस्टीम प्रॉम्ट
system_prompt = (
    "तू 'AI सारथी' आहेस - भगवद्गीतेच्या तत्त्वज्ञानावर आधारित एक ज्ञानी, शांत, संवेदनशील आणि मार्गदर्शक डिजिटल मित्र. "
    "हा उपक्रम 'विघ्नहर्ता गोल्ड फाउंडेशन' यांच्या संकल्पनेतून चालवला जात आहे. "
    f"वापरकर्त्याने निवडलेली भाषा: {st.session_state.selected_lang}. निवडलेला विभाग: {selected_mode}. "
    "महत्त्वाचे नियम: "
    f"१. संपूर्ण उत्तर १००% शुद्ध, आदरार्थी आणि सहज समजणाऱ्या {st.session_state.selected_lang} भाषेतच दे. "
    "२. उत्तरात थेट भगवद्गीतेतील समर्पक श्लोक किंवा श्रीकृष्ण-अर्जुन संवादाचा सारांश देऊन व्यावहारिक समुपदेशन कर. "
    "३. कर्म, धर्म, अनासक्ती, मनःशांती आणि निर्णयक्षमतेवर भर दे."
)

# ७. Google GenAI क्लायंट
api_token = st.secrets.get("GEMINI_API_KEY", "").strip()

if not api_token:
    st.info("कृपया Streamlit Secrets मध्ये GEMINI_API_KEY जोडा.", icon="ℹ️")
    st.stop()

@st.cache_resource(show_spinner=False)
def init_genai_client(key):
    return genai.Client(api_key=key)

client = init_genai_client(api_token)

# ८. वेगवान स्ट्रीमिंग रिस्पॉन्स
def stream_sarathi_response(query):
    prompt_with_context = f"{system_prompt}\n\n[विभाग: {selected_mode}]\nप्रश्न: {query}"
    response_stream = client.models.generate_content_stream(
        model="gemini-3.8-flash",
        contents=prompt_with_context
    )
    for chunk in response_stream:
        if chunk.text:
            yield chunk.text

# ९. चॅट हिस्ट्री
if "sarathi_messages" not in st.session_state:
    st.session_state.sarathi_messages = []

for message in st.session_state.sarathi_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# १०. प्रश्न इनपुट बॉक्स
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

# ११. तळटीप ब्रँडिंग आणि साधक काउंटर
st.markdown(f"""
    <div class="footer-container">
        <div class="brand-title">AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION</div>
        <div class="footer-text">{curr["foundation_text"]}</div>
        <div class="visitor-badge">
            👁️ {curr["visitor_label"]} 
            <img src="https://komarev.com/ghpvc/?username=aisarathi-vighnaharta&color=ffb300&style=flat-square&label=Views" alt="Views" style="vertical-align: middle; margin-left: 4px; border-radius: 4px;">
        </div>
    </div>
""", unsafe_allow_html=True)
