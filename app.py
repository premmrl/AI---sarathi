import streamlit as st
from google import genai
from google.genai import types

# १. पेज कॉन्फिगरेशन
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
        margin-top: 50px;
        padding-top: 15px;
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
    </style>
""", unsafe_allow_html=True)

# ३. भाषा आणि श्रेणी निवड
col1, col2 = st.columns([1, 1.2])

with col1:
    language = st.selectbox(
        "🌐 Language / भाषा:",
        [
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
    )

with col2:
    mode = st.selectbox(
        "🎯 Guidance Domain / मार्गदर्शन क्षेत्र:",
        [
            "जीवन व वैयक्तिक (Life & Personal)",
            "व्यवसाय व गुंतवणूक (Business & Wealth)"
        ]
    )

# ४. निवडलेल्या क्षेत्रानुसार सिस्टीम मार्गदर्शक सूचना
if "Business" in mode:
    DOMAIN_PROMPT = """
तू 'AI सारथी - Business & Wealth Edition' आहेस. 
वापरकर्ता व्यावसायिक, उद्योजक, लीडर किंवा गुंतवणूकदार आहे. त्याचे प्रश्न व्यापार, नेतृत्व, भागीदारी, नुकसान, बाजारातील मंदी, जोखीम व्यवस्थापन (Risk Management) किंवा आर्थिक गुंतवणुकीतील निर्णय याविषयी असतील.

तुझे काम:
१. व्यावसायिक संभ्रम आणि भावनिक दबाव (उदा. लोभ, भीती, अस्थिरता) याचे विश्लेषण करणे.
२. भगवद्गीतेतील अचूक अध्याय व श्लोकाचा संदर्भ देणे (उदा. 'कर्मण्येवाधिकारस्ते', 'स्थितप्रज्ञ', 'समत्वं योग उच्यते', 'योगः कर्मसु कौशलम्' इत्यादी) आणि त्याचा आधुनिक व्यवस्थापन व गुंतवणुकीच्या संदर्भात अर्थ सांगणे.
३. उद्योजक/गुंतवणूकदारासाठी २ ते ३ स्पष्ट, व्यावहारिक आणि रणनीतिक पावले (Strategic Steps) देणे.
तुझा सूर व्यावसायिक, प्रेरणादायी, धोरणी आणि तत्त्वज्ञासारखा असावा.
"""
else:
    DOMAIN_PROMPT = """
तू 'AI सारथी' आहेस - एक मार्गदर्शक, मित्र आणि तत्त्वज्ञ.
वापरकर्ता दैनंदिन जीवनातील चिंता, नाती, करिअर, अपयश, राग किंवा इतर कोणताही प्रश्न कोणत्याही भाषेत विचारेल.

तुझे काम:
१. मानसिक दिलासा आणि समस्येचे मूळ कारण सोप्या शब्दांत स्पष्ट करणे.
२. भगवद्गीतेतील अचूक अध्याय आणि श्लोकाचा संदर्भ देणे (मूळ संस्कृत श्लोक आणि निवडलेल्या भाषेत सोपा अर्थ).
३. हा विचार दैनंदिन जीवनात कसा आचरायचा, याची २ ते ३ व्यावहारिक पावले (Actionable Advice) देणे.
तुझा सूर नेहमी प्रेमळ, सकारात्मक, संयमी आणि मार्गदर्शकासारखा असावा.
"""

SYSTEM_INSTRUCTION = f"""
{DOMAIN_PROMPT}

महत्त्वाचा नियम: वापरकर्त्याने निवडलेल्या भाषेत (किंवा ज्या भाषेत प्रश्न विचारला आहे), त्याला संपूर्ण उत्तर त्याच भाषेत दे.
सध्या निवडलेली भाषा: {language}
"""

# ५. शीर्षके व प्लेसहोल्डर
if "Business" in mode:
    st.title("💼 🕉️ AI सारथी — Business & Wealth")
    st.caption("व्यापार, नेतृत्व आणि आर्थिक गुंतवणुकीसाठी भगवद्गीतेवर आधारित व्यवस्थापकीय मार्गदर्शन")
    input_placeholder = "तुमचा व्यावसायिक संभ्रम, गुंतवणुकीचा प्रश्न किंवा आव्हान येथे लिहा..."
else:
    st.title("🕉️ AI सारथी")
    st.caption("तुमच्या मनातील प्रश्न आणि समस्यांवर भगवद्गीतेच्या प्रकाशात अचूक मार्गदर्शन")
    input_placeholder = "तुमचा प्रश्न किंवा समस्या येथे लिहा..."

# ६. API Key व्यवस्थापन
api_key = st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    api_key = st.sidebar.text_input("Gemini API Key:", type="password")

if not api_key:
    st.info("कृपया पुढे जाण्यासाठी API Key आवश्यक आहे.", icon="ℹ️")
    st.stop()

# ७. Client सुरू करणे
client = genai.Client(api_key=api_key)

# ८. चॅट हिस्ट्री व्यवस्थापन
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ९. प्रश्न घेणे आणि उत्तर देणे
if user_prompt := st.chat_input(input_placeholder):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("सारथी विचार करत आहेत..."):
            history_contents = []
            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "model"
                history_contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )

            reply_text = None
            for model_name in ["gemini-2.5-flash", "gemini-3.8-flash", "gemini-3-flash-preview"]:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=history_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                            temperature=0.7
                        )
                    )
                    reply_text = response.text
                    break
                except Exception:
                    continue

            if reply_text:
                st.markdown(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})
            else:
                st.warning("सर्व्हर सध्या व्यस्त आहे. कृपया थोड्या वेळाने प्रयत्न करा.")

# १०. तळाशी ब्रँडिंग फूटर
st.markdown("""
    <div class='footer-container'>
        <div class='brand-title'>An Initiative by Vighnaharta Gold Foundation</div>
        <div class='footer-text'>
            प्रकल्प संकल्पना व संचलन: <b>Vighnaharta Gold Foundation</b><br>
            भगवद्गीतेच्या तत्त्वांवर आधारित समाजहितैषी डिजिटल उपक्रम
        </div>
    </div>
""", unsafe_allow_html=True)
