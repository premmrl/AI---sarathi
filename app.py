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

# ३. भाषा आणि मार्गदर्शन क्षेत्र निवड
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

# ४. सिस्टीम मार्गदर्शक सूचना
if "Business" in mode:
    DOMAIN_PROMPT = """
तू 'AI सारथी - Business & Wealth Edition' आहेस. 
वापरकर्ता व्यावसायिक, उद्योजक, लीडर किंवा गुंतवणूकदार आहे. त्याचे प्रश्न व्यापार वाढवणे (उदा. व्यवसाय १० पट करणे), नेतृत्व, तोटा, बाजारातील मंदी, जोखीम व्यवस्थापन किंवा आर्थिक निर्णय याविषयी असतील.

तुझे काम खालील रचनेनुसार उत्तर देणे आहे:
१. समस्येचे आणि व्यावसायिक उद्दिष्टाचे संक्षिप्त व प्रभावी विश्लेषण.
२. भगवद्गीतेतील अचूक अध्याय व श्लोकाचा संदर्भ (संस्कृत श्लोक व त्याचा आधुनिक व्यापार/गुंतवणूक संदर्भातील अर्थ).
३. ध्येय गाठण्यासाठी २ ते ३ व्यावहारिक आणि रणनीतिक पावले (Actionable Strategic Steps).
उत्तर प्रेरणादायी, धोरणी आणि थेट असावे.
"""
else:
    DOMAIN_PROMPT = """
तू 'AI सारथी' आहेस - एक मार्गदर्शक, मित्र आणि तत्त्वज्ञ.
वापरकर्ता दैनंदिन जीवनातील चिंता, नाती, करिअर, अपयश, राग किंवा इतर कोणताही प्रश्न विचारेल.

तुझे काम खालील रचनेनुसार उत्तर देणे आहे:
१. मानसिक दिलासा आणि समस्येचे मूळ कारण सोप्या शब्दांत सांगणे.
२. भगवद्गीतेतील अचूक अध्याय आणि श्लोकाचा संदर्भ (संस्कृत श्लोक आणि सोपा अर्थ).
३. दैनंदिन जीवनात आचरणात आणण्यासाठी २ ते ३ व्यावहारिक पावले (Actionable Advice).
उत्तर प्रेमळ, सकारात्मक आणि सुटसुटीत असावे.
"""

SYSTEM_INSTRUCTION = f"""
{DOMAIN_PROMPT}

नियम: वापरकर्त्याला उत्तर निवडलेल्या भाषेतच दे.
सध्या निवडलेली भाषा: {language}
"""

# ५. शीर्षके व इनपुट
if "Business" in mode:
    st.title("💼 🕉️ AI सारथी — Business & Wealth")
    st.caption("व्यापार, नेतृत्व आणि आर्थिक गुंतवणुकीसाठी भगवद्गीतेवर आधारित व्यवस्थापकीय मार्गदर्शन")
    input_placeholder = "तुमचा व्यावसायिक संभ्रम किंवा प्रश्न येथे लिहा..."
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

# ८. चॅट हिस्ट्री
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ९. प्रश्न घेणे आणि खात्रीशीर उत्तर देणे
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
            # थेट सक्रिय मॉडेल्सचा क्रम
            models_to_try = ["gemini-3.8-flash", "gemini-3-flash-preview", "gemini-2.5-flash"]
            
            for m_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=m_name,
                        contents=history_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                            temperature=0.7
                        )
                    )
                    if response and response.text:
                        reply_text = response.text
                        break
                except Exception:
                    continue

            if reply_text:
                st.markdown(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})
            else:
                st.error("सर्व्हर प्रतिसाद मिळण्यात अडचण येत आहे. कृपया Secrets मध्ये Gemini API Key बरोबर असल्याची खात्री करा.")

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
