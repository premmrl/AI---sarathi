import streamlit as st
import time
from google import genai

# १. पेज कॉन्फिगरेशन
st.set_page_config(
    page_title="ॐ AI सारथी | Gita AI Guide",
    page_icon="🕉️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# २. प्रीमियम आणि दिव्य CSS डिझाइन (Gold Glow, Glassmorphism, Spiritual Vibes)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Yatra+One&family=Mukta:wght@300;400;600;700;800&display=swap');

    /* संपूर्ण पार्श्वभूमी व मूलभूत फॉन्ट */
    .stApp {
        background: radial-gradient(circle at 50% 8%, #1f1830 0%, #0d0a14 100%) !important;
        font-family: 'Mukta', sans-serif !important;
        color: #f5f2eb !important;
    }

    /* मुख्य हेडर कार्ड (Hero Card) */
    .hero-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(212, 175, 55, 0.04));
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 22px;
        padding: 24px 20px 18px 20px;
        text-align: center;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.55), 0 0 18px rgba(212, 175, 55, 0.12);
        backdrop-filter: blur(12px);
        margin-bottom: 22px;
    }

    .om-icon {
        font-size: 42px;
        line-height: 1.1;
        filter: drop-shadow(0 0 12px rgba(255, 179, 0, 0.65));
        margin-bottom: 4px;
    }

    .title-glow {
        font-family: 'Mukta', sans-serif;
        font-size: 34px;
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

    /* मोड सिलेक्टर (रेडिओ बटन्स) चे सुंदर टॅब डिझाइन */
    div[role="radiogroup"] {
        display: flex !important;
        justify-content: center !important;
        background: rgba(255, 255, 255, 0.04) !important;
        padding: 6px !important;
        border-radius: 30px !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        gap: 8px !important;
        margin: 10px 0 16px 0 !important;
    }

    div[role="radiogroup"] label {
        padding: 8px 16px !important;
        border-radius: 20px !important;
        background: transparent !important;
        color: #e0d8ee !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
    }

    div[role="radiogroup"] label:hover {
        background: rgba(212, 175, 55, 0.15) !important;
    }

    /* क्विक प्रश्न चिप्स (Prompt Chips) */
    .quick-chips-title {
        text-align: center;
        font-size: 12px;
        color: #bfa8e6;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
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

    /* भेट देणारे साधक काउंटर बॅज */
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

# ३. भाषा निवड
LANGUAGES = [
    "मराठी", "हिंदी", "English", "ગુજરાતી", "ಕನ್ನಡ", 
    "తెలుగు", "தமிழ்", "বাংলা", "മലയാളം", "ਪੰਜਾਬੀ"
]

language = st.selectbox(
    "🌐 Choose Language / भाषा निवडा / अपनी भाषा चुनें:",
    LANGUAGES,
    index=0
)

# ४. आकर्षक मुख्य हेडर कार्ड (Hero Card)
st.markdown("""
    <div class="hero-card">
        <div class="om-icon">🕉️</div>
        <div class="title-glow">AI सारथी</div>
        <div class="sub-tagline">
            जीवनातील आणि व्यवसायातील गुंतागुंतीच्या निर्णयांना भगवद्गीतेच्या दिव्य प्रकाशात अचूक दिशा
        </div>
    </div>
""", unsafe_allow_html=True)

# ५. मार्गदर्शन विभाग निवड
modes = [
    "🌱 वैयक्तिक जीवन (Personal Guidance)",
    "💼 व्यवसाय आणि करिअर (Business & Career)"
]

selected_mode = st.radio(
    "मार्गदर्शन प्रकार निवडा:",
    modes,
    horizontal=True,
    label_visibility="collapsed"
)

# ६. सिस्टीम सूचना (System Prompt)
system_prompt = (
    "तू 'AI सारथी' आहेस - भगवद्गीतेच्या तत्त्वज्ञानावर आधारित एक ज्ञानी, शांत, संवेदनशील आणि मार्गदर्शक डिजिटल मित्र. "
    "हा उपक्रम 'विघ्नहर्ता गोल्ड फाउंडेशन' यांच्या संकल्पनेतून समाजाला योग्य दिशा देण्यासाठी चालवला जात आहे. "
    f"वापरकर्त्याने निवडलेली भाषा: {language}. निवडलेला विभाग: {selected_mode}. "
    "महत्त्वाचे नियम: "
    f"१. संपूर्ण उत्तर १००% शुद्ध, आदरार्थी आणि सहज समजणाऱ्या {language} भाषेतच दे. "
    "२. उत्तरात थेट भगवद्गीतेतील समर्पक श्लोक किंवा श्रीकृष्ण-अर्जुन संवादाचा सारांश देऊन व्यावहारिक समुपदेशन कर. "
    "३. कर्म, धर्म, अनासक्ती, मनःशांती आणि निर्णयक्षमतेवर भर दे."
)

# ७. Google GenAI क्लायंट सेटअप
api_token = st.secrets.get("GEMINI_API_KEY", "").strip()

if not api_token:
    st.info("कृपया Streamlit Secrets मध्ये GEMINI_API_KEY जोडा.", icon="ℹ️")
    st.stop()

@st.cache_resource(show_spinner=False)
def init_genai_client(key):
    return genai.Client(api_key=key)

client = init_genai_client(api_token)

# ८. वेगाने व न अडखळता उत्तर देणारे Streaming फंक्शन
def stream_sarathi_response(query):
    prompt_with_context = f"{system_prompt}\n\n[विभाग: {selected_mode}]\nप्रश्न: {query}"
    
    # चालू व स्थिर मॉडेल
    response_stream = client.models.generate_content_stream(
        model="gemini-3.8-flash",
        contents=prompt_with_context
    )
    for chunk in response_stream:
        if chunk.text:
            yield chunk.text

# ९. चॅट हिस्ट्री व्यवस्थापन
if "sarathi_messages" not in st.session_state:
    st.session_state.sarathi_messages = []

for message in st.session_state.sarathi_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# १०. साधकाचा प्रश्न व जलद टाईपिंग रिस्पॉन्स
input_placeholder = "आपला प्रश्न, चिंता किंवा द्विधा मनःस्थिती येथे मांडा..."
if user_prompt := st.chat_input(input_placeholder):
    st.session_state.sarathi_messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        try:
            full_response = st.write_stream(stream_sarathi_response(user_prompt))
            st.session_state.sarathi_messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"तांत्रिक अडचण: {str(e)}")

# ११. दिव्य तळटीप, संस्था ब्रँडिंग आणि साधक व्हिजिटर काउंटर
st.markdown("""
    <div class="footer-container">
        <div class="brand-title">AN INITIATIVE BY VIGHNAHARTA GOLD FOUNDATION</div>
        <div class="footer-text">
            प्रकल्प संकल्पना व संचलन: <b>विघ्नहर्ता गोल्ड फाउंडेशन</b><br>
            भगवद्गीतेच्या कालातीत तत्त्वांवर आधारित समाजहितैषी डिजिटल उपक्रम
        </div>
        <div class="visitor-badge">
            👁️ एकूण भेट देणारे साधक: 
            <img src="https://komarev.com/ghpvc/?username=aisarathi-vighnaharta&color=ffb300&style=flat-square&label=Views" alt="Views" style="vertical-align: middle; margin-left: 4px; border-radius: 4px;">
        </div>
    </div>
""", unsafe_allow_html=True)
