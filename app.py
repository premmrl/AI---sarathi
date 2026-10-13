import streamlit as st
from google import genai

# १. पेज कॉन्फिगरेशन
st.set_page_config(
    page_title="ॐ AI सारथी | Gita AI Guide",
    page_icon="🕉️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# २. परफेक्ट मोबाइल लेआउट CSS (वर योग्य मोकळी जागा दिलेली)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Mukta:wght@300;400;600;700;800&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% -10%, #2e1065 0%, #1e1b4b 35%, #0f172a 70%, #030712 100%) !important;
        font-family: 'Mukta', sans-serif !important;
        color: #ffffff !important;
    }

    /* वरून कार्ड खाली घेण्यासाठी मुख्य कंटेनरचे स्पेसिंग */
    .block-container {
        padding-top: 2.8rem !important;
        padding-bottom: 4.5rem !important;
        max-width: 520px !important;
    }

    /* मुख्य हेडर कार्ड */
    .hero-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.07) 0%, rgba(217, 119, 6, 0.1) 100%);
        border: 1.2px solid rgba(251, 191, 36, 0.55);
        border-radius: 16px;
        padding: 12px 14px 10px 14px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5), 0 0 14px rgba(245, 158, 11, 0.18);
        backdrop-filter: blur(10px);
        margin-top: 14px !important;
        margin-bottom: 8px;
    }

    .om-icon {
        font-size: 32px;
        line-height: 1.1;
        filter: drop-shadow(0 0 10px rgba(251, 191, 36, 0.85));
        margin-bottom: 2px;
    }

    .title-glow {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFDF0 0%, #FEF08A 25%, #F59E0B 65%, #B45309 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.6px;
        margin: 1px 0 3px 0;
        filter: drop-shadow(0 2px 6px rgba(245, 158, 11, 0.35));
    }

    .sub-tagline {
        color: #e2e8f0;
        font-size: 11.5px;
        font-weight: 400;
        line-height: 1.35;
        opacity: 0.95;
    }

    /* भाषा निवड लेबल */
    .stSelectbox label p {
        color: #FDE68A !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
        margin-bottom: 2px !important;
    }

    /* भाषा निवड बॉक्स */
    div[data-baseweb="select"] {
        border-radius: 10px !important;
        border: 1.2px solid rgba(251, 191, 36, 0.55) !important;
        background-color: rgba(30, 41, 59, 0.85) !important;
        min-height: 36px !important;
    }

    div[data-baseweb="select"] * {
        color: #FEF08A !important;
        font-weight: 700 !important;
        font-size: 13.5px !important;
    }

    /* रेडिओ बटन्स */
    div[role="radiogroup"] {
        display: flex !important;
        justify-content: center !important;
        background: rgba(30, 41, 59, 0.65) !important;
        padding: 3px 6px !important;
        border-radius: 22px !important;
        border: 1px solid rgba(251, 191, 36, 0.4) !important;
        gap: 6px !important;
        margin: 4px 0 6px 0 !important;
    }

    div[role="radiogroup"] label {
        padding: 4px 10px !important;
        border-radius: 16px !important;
        background: transparent !important;
        color: #f8fafc !important;
        font-size: 12px !important;
        font-weight: 600 !important;
    }

    /* चॅट मेसेज कार्ड्स */
    div[data-testid="stChatMessage"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95)) !important;
        border: 1.2px solid rgba(251, 191, 36, 0.4) !important;
        border-radius: 14px !important;
        padding: 10px 12px !important;
        margin-bottom: 8px !important;
    }

    div[data-testid="stChatMessage"] * {
        color: #f8fafc !important;
    }

    div[data-testid="stChatMessage"] h1, 
    div[data-testid="stChatMessage"] h2, 
    div[data-testid="stChatMessage"] h3, 
    div[data-testid="stChatMessage"] h4 {
        color: #FDE68A !important;
        font-weight: 700 !important;
    }

    div[data-testid="stChatMessage"] p, 
    div[data-testid="stChatMessage"] li {
        color: #f1f5f9 !important;
        font-size: 14px !important;
        line-height: 1.55 !important;
    }

    /* इनपुट बॉक्स */
    div[data-testid="stChatInput"],
    div[data-testid="stChatInput"] > div,
    .stChatInputContainer {
        background-color: #0f172a !important;
        border: 1.4px solid rgba(251, 191, 36, 0.65) !important;
        border-radius: 14px !important;
    }

    div[data-testid="stChatInput"] textarea,
    .stChatInputContainer textarea {
        color: #ffffff !important;
        background-color: #0f172a !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        caret-color: #fbbf24 !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder,
    .stChatInputContainer textarea::placeholder {
        color: #94a3b8 !important;
        font-weight: 400 !important;
    }

    /* कॉम्पॅक्ट फुटर */
    .footer-container {
        text-align: center;
        margin-top: 6px;
        padding-top: 4px;
        border-top: 1px solid rgba(251, 191, 36, 0.2);
    }

    .brand-title {
        color: #FCD34D;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 1px;
    }

    .footer-text {
        color: #cbd5e1;
        font-size: 10px;
        line-height: 1.35;
    }

    /* भेट देणारे साधक बॅज */
    .visitor-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(245, 158, 11, 0.15);
        border: 1.2px solid rgba(251, 191, 36, 0.6);
        color: #FEF08A;
        padding: 3px 12px;
        border-radius: 14px;
        font-size: 11.5px;
        font-weight: 600;
        margin-top: 4px;
    }

    .views-counter-tag {
        background: #D97706;
        color: #FFFBEB;
        padding: 1px 7px;
        border-radius: 4px;
        font-weight: 800;
        font-size: 11px;
    }
    </style>
""", unsafe_allow_html=True)

# ३. सर्व्हर-आधारित रिअल-टाईम व्हिजिटर काऊंटर (चालू आकडा २५ वरून पुढे)
@st.cache_resource
def get_global_counter():
    return {"count": 25}

counter_store = get_global_counter()

if "counted_this_device" not in st.session_state:
    counter_store["count"] += 1
    st.session_state.counted_this_device = True

current_views = counter_store["count"]

# ४. स्थानिक भाषांतर डेटा (१० भाषा)
LOCALIZED_CONTENT = {
    "मराठी": {
        "title": "AI सारथी",
        "tagline": "जीवनातील आणि व्यवसायातील गुंतागुंतीच्या निर्णयांना भगवद्गीतेच्या दिव्य प्रकाशात अचूक दिशा",
        "modes": [
            "🌱 वैयक्तिक जीवन (Personal Guidance)",
            "💼 व्यवसाय आणि करिअर (Business & Career)"
        ],
        "placeholder": "आपला प्रश्न, चिंता किंवा द्विधा मनःस्थिती येथे मांडा...",
        "thinking": "ॐ AI सारथी भगवद्गीतेच्या प्रकाशात मार्गदर्शन शोधत आहे...",
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
        "thinking": "ॐ AI सारथी भगवद्गीता के प्रकाश में मार्गदर्शन प्राप्त कर रहे हैं...",
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
        "thinking": "ॐ AI Sarathi is seeking divine guidance from the Bhagavad Gita...",
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
        "thinking": "ॐ AI સારથી ભગવદ્ગીતાના પ્રકાશમાં માર્ગદર્શન મેળવી રહ્યા છે...",
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
        "thinking": "ॐ AI ಸಾರಥಿ ಭಗವದ್ಗೀತೆಯ ಮಾರ್ಗದರ್ಶನವನ್ನು ಪಡೆಯುತ್ತಿದ್ದಾರೆ...",
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
        "thinking": "ॐ AI సారథి భగవద్గీత వెలుగులో సమాధానాన్ని అన్వేషిస్తున్నారు...",
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
        "thinking": "ॐ AI சாரதி பகவத் கீதையிலிருந்து வழிகாட்டுதலைப் பெறுகிறார்...",
        "foundation_text": "முயற்சி: <b>விக்னஹர்த்தா கோல்ட் ஃபவுண்டேஷன்</b><br>பகவத் கீதையின் வழிகாட்டுதல் திட்டம்",
        "visitor_label": "பார்வையிட்ட பக்தர்கள்:"
    },
    "বাংলা": {
        "title": "AI সারথি",
        "tagline": "ভগবদ্গীতার দিব্য আলোকে জীবন ও ব্যবসার সিদ্ধান্তের সঠিক পথনির্দেশ",
        "modes": [
            "🌱 व्यक्तिगत जीवन (Personal Guidance)",
            "💼 व्यवसाय ও कर्मজীবন (Business & Career)"
        ],
        "placeholder": "আপনার प्रश्न বা সংশয় येथे লিখুন...",
        "thinking": "ॐ AI সারথি শ্রীমদ্ভগবদ্গীতার আলোকে निर्देशिका খুঁজছেন...",
        "foundation_text": "উদ্যোগ: <b>বিঘ্নহর্তা গোল্ড ফাউন্ডেশন</b><br>শ্রীমদ্ভগবদ্গীতার কালজয়ী निर्देशিকা",
        "visitor_label": "মোট দর্শনার্থী সাধक:"
    },
    "മലയാളം": {
        "title": "AI സಾರഥി",
        "tagline": "ഭഗവദ്ഗീതയുടെ ദിവ്യവെളിച്ചത്തിൽ ജീവിതത്തിലെയും ബിസിനസ്സിലെയും തീരുമാനങ്ങൾക്ക് കൃത്യമായ വഴികാട്ടി",
        "modes": [
            "🌱 വ്യക്തിജീവിതം (Personal Guidance)",
            "💼 ബിസിനസ്സും കരിയറും (Business & Career)"
        ],
        "placeholder": "നിങ്ങളുടെ ചോദ്യം ഇവിടെ കുറിക്കുക...",
        "thinking": "ॐ AI സാരഥി ഭഗവദ്ഗീതയിൽ നിന്ന് മാർഗ്ഗദർശനം തേടുന്നു...",
        "foundation_text": "സംരംഭം: <b>വിഘ്നഹർത്ത ഗോൾഡ് ഫൗണ്ടേഷൻ</b><br>ഭഗવദ്गीതാ तத்துவங்களின் டிஜிറ്റൽ മാർഗ്ഗരേഖ",
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
        "thinking": "ॐ AI ਸਾਰਥੀ ਭਗਵਦ ਗੀਤਾ ਤੋਂ ਮਾਰਗਦਰਸ਼ਨ ਲੈ ਰਹੇ ਹਨ...",
        "foundation_text": "ਉਪਰਾਲਾ: <b>ਵਿਘਨਹਰਤਾ ਗੋਲਡ ਫਾਊਂਡੇਸ਼ਨ</b><br>ਭਗਵਦ ਗੀਤਾ ਦੇ ਸਿਧਾਂਤਾਂ 'ਤੇ ਆਧਾਰਿਤ ਡਿਜੀਟਲ ਪਹਿਲ",
        "visitor_label": "ਕੁੱਲ ਸਾਧਕ:"
    }
}

if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = "मराठी"

curr = LOCALIZED_CONTENT[st.session_state.selected_lang]

# ५. मुख्य हेडर कार्ड
st.markdown(f"""
    <div class="hero-card">
        <div class="om-icon">🕉️</div>
        <div class="title-glow">{curr["title"]}</div>
        <div class="sub-tagline">{curr["tagline"]}</div>
    </div>
""", unsafe_allow_html=True)

# ६. भाषा निवड
LANGUAGES = list(LOCALIZED_CONTENT.keys())
chosen_lang = st.selectbox(
    "🌐 भाषा निवडा / Choose Language:",
    LANGUAGES,
    index=LANGUAGES.index(st.session_state.selected_lang)
)

if chosen_lang != st.session_state.selected_lang:
    st.session_state.selected_lang = chosen_lang
    st.rerun()

# ७. मार्गदर्शन विभाग
selected_mode = st.radio(
    "मार्गदर्शन क्षेत्र:",
    curr["modes"],
    horizontal=True,
    label_visibility="collapsed"
)

# ८. Google GenAI क्लायंट व सिस्टीम प्रॉम्ट
system_prompt = (
    "तू 'AI सारथी' आहेस - भगवद्गीतेच्या तत्त्वज्ञानावर आधारित एक ज्ञानी, शांत, संवेदनशील आणि मार्गदर्शक डिजिटल मित्र. "
    "हा उपक्रम 'विघ्नहर्ता गोल्ड फाउंडेशन' यांच्या संकल्पनेतून चालवला जात आहे. "
    f"वापरकर्त्याने निवडलेली भाषा: {st.session_state.selected_lang}. निवडलेला विभाग: {selected_mode}. "
    "महत्त्वाचे नियम: "
    f"१. संपूर्ण उत्तर १००% शुद्ध, आदरार्थी आणि सहज समजणाऱ्या {st.session_state.selected_lang} भाषेतच दे. "
    "२. उत्तरात थेट भगवद्गीतेतील समर्पक श्लोक किंवा श्रीकृष्ण-अर्जुन संवादाचा सारांश देऊन व्यावहारिक समुपदेशन कर. "
    "३. कर्म, धर्म, अनासक्ती, मनःशांती आणि निर्णयक्षमतेवर भर दे."
)

api_token = st.secrets.get("GEMINI_API_KEY", "").strip()

if not api_token:
    st.info("कृपया Streamlit Secrets मध्ये GEMINI_API_KEY जोडा.", icon="ℹ️")
    st.stop()

@st.cache_resource(show_spinner=False)
def init_genai_client(key):
    return genai.Client(api_key=key)

client = init_genai_client(api_token)

# ९. अधिक कोटा असलेले मोफत मॉडेल (gemini-1.5-flash)
def get_sarathi_response(query):
    prompt_with_context = f"{system_prompt}\n\n[विभाग: {selected_mode}]\nप्रश्न: {query}"
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt_with_context
    )
    return response.text

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
        with st.spinner(curr["thinking"]):
            try:
                full_response = get_sarathi_response(user_prompt)
                st.markdown(full_response)
                st.session_state.sarathi_messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"तांत्रिक अडचण: {str(e)}")

# १२. कॉम्पॅक्ट तळटीप ब्रँडिंग आणि काऊंटर
st.markdown(f"""
    <div class="footer-container">
        <div class="brand-title">AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION</div>
        <div class="footer-text">{curr["foundation_text"]}</div>
        <div class="visitor-badge">
            👁️ {curr["visitor_label"]} 
            <span class="views-counter-tag">Views {current_views}</span>
        </div>
    </div>
""", unsafe_allow_html=True)
