import streamlit as st
import os
from google import genai
from google.genai import types

# १. पेज सेटिंग्ज
st.set_page_config(
    page_title="AI सारथी | Vighnaharta Gold Foundation",
    page_icon="🕉️",
    layout="centered"
)

# २. ब्रँडिंग व डिझाइन स्टाईल (Custom CSS)
st.markdown("""
    <style>
    .brand-header {
        text-align: center;
        margin-top: 5px;
        margin-bottom: 12px;
    }
    .brand-title {
        font-size: 14px;
        color: #d4af37;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .footer-text {
        text-align: center;
        color: #888888;
        font-size: 13px;
        margin-top: 45px;
        padding-top: 15px;
        border-top: 1px solid #333333;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# ३. सिस्टीम मार्गदर्शक सूचना (मराठी, हिंदी व इंग्रजी तिन्हींसाठी)
SYSTEM_INSTRUCTION = """
तू 'AI सारथी' आहेस - एक मार्गदर्शक, मित्र आणि तत्त्वज्ञ.
वापरकर्ता दैनंदिन जीवनातील चिंता, नाती, करिअर, अपयश, राग किंवा इतर कोणताही प्रश्न त्यांच्या भाषेत (मराठी, हिंदी किंवा इंग्रजी) विचारेल.

महत्त्वाचा नियम: वापरकर्त्याने ज्या भाषेत प्रश्न विचारला आहे, त्याला संपूर्ण उत्तर त्याच भाषेत दे (उदा. हिंदीमध्ये विचारल्यास शुद्ध, प्रेमळ व सोप्या हिंदीत; मराठीत विचारल्यास मराठीत; इंग्रजीत विचारल्यास इंग्रजीत).

तुझे काम खालील रचनेनुसार उत्तर देणे आहे:
१. मानसिक दिलासा आणि समस्येचे मूळ कारण सोप्या शब्दांत स्पष्ट करणे.
२. भगवद्गीतेतील अचूक अध्याय आणि श्लोकाचा संदर्भ देणे (मूळ संस्कृत श्लोक आणि त्याचा निवडलेल्या भाषेत सोपा अर्थ).
३. हा विचार दैनंदिन जीवनात कसा आचरायचा, याची २ ते ३ व्यावहारिक पावले (Actionable Advice) देणे.

तुझा सूर नेहमी प्रेमळ, सकारात्मक, संयमी आणि मार्गदर्शकासारखा असावा.
"""

# ४. भाषा निवड (स्क्रीनच्या सर्वात वर)
language = st.selectbox(
    "🌐 Choose Language / भाषा निवडा / अपनी भाषा चुनें:",
    ["मराठी", "हिंदी", "English"]
)

# ५. लोगो दाखवणे (logo1.jpg किंवा logo.jpg)
col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
with col2:
    for img_name in ["logo1.jpg", "logo.jpg", "logo.png", "logo.jpeg"]:
        if os.path.exists(img_name):
            st.image(img_name, use_container_width=True)
            break

# ६. ब्रँडिंग हेडर
st.markdown("""
    <div class='brand-header'>
        <div class='brand-title'>An Initiative by Vighnaharta Gold Foundation</div>
    </div>
""", unsafe_allow_html=True)

# ७. निवडलेल्या भाषेनुसार शीर्षके आणि मजकूर
if language == "हिंदी":
    st.title("🕉️ AI सारथी")
    st.caption("आपके जीवन के प्रश्नों और समस्याओं का भगवद्गीता के प्रकाश में सटीक मार्गदर्शन")
    input_placeholder = "अपनी समस्या या प्रश्न यहाँ लिखें..."
    thinking_text = "सारथी विचार कर रहे हैं..."
elif language == "English":
    st.title("🕉️ AI Sarathi")
    st.caption("Timeless guidance from the Bhagavad Gita for modern life's challenges")
    input_placeholder = "Type your question or dilemma here..."
    thinking_text = "Sarathi is reflecting..."
else:
    st.title("🕉️ AI सारथी")
    st.caption("तुमच्या मनातील प्रश्न आणि समस्यांवर भगवद्गीतेच्या प्रकाशात अचूक मार्गदर्शन")
    input_placeholder = "तुमचा प्रश्न किंवा समस्या येथे लिहा..."
    thinking_text = "सारथी विचार करत आहेत..."

# ८. API Key व्यवस्थापन
api_key = st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    api_key = st.sidebar.text_input("Gemini API Key:", type="password")

if not api_key:
    st.info("कृपया पुढे जाण्यासाठी API Key आवश्यक आहे.", icon="ℹ️")
    st.stop()

# ९. Client सुरू करणे
client = genai.Client(api_key=api_key)

# १०. चॅट हिस्ट्री व्यवस्थापन
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ११. युझरचा प्रश्न घेणे आणि उत्तर देणे
if user_prompt := st.chat_input(input_placeholder):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner(thinking_text):
            history_contents = []
            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "model"
                history_contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )

            # सर्व्हर लोड टाळण्यासाठी पर्यायी मॉडेल्स
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
                st.warning("सर्व्हर सध्या व्यस्त आहे. कृपया थोड्या वेळाने पुन्हा प्रयत्न करा.")

# १२. अधिकृत फूटर (Footer)
st.markdown("""
    <div class='footer-text'>
        प्रकल्प संकल्पना व संचलन: <b>Vighnaharta Gold Foundation</b><br>
        भगवद्गीतेच्या तत्त्वांवर आधारित समाजहितैषी डिजिटल उपक्रम
    </div>
""", unsafe_allow_html=True)
