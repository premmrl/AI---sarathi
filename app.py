import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="भगवद्गीता सारथी",
    page_icon="🕉️",
    layout="centered"
)

# सिस्टीम मार्गदर्शक सूचना
SYSTEM_INSTRUCTION = """
तू 'भगवद्गीता सारथी' आहेस - एक मार्गदर्शक, मित्र आणि तत्त्वज्ञ.
वापरकर्ता दैनंदिन जीवनातील चिंता, नाती, करिअर, अपयश, राग किंवा इतर कोणताही प्रश्न त्यांच्या भाषेत विचारेल.
तुझे काम खालील रचनेनुसार उत्तर देणे आहे:
१. मानसिक दिलासा आणि समस्येचे मूळ कारण सोप्या शब्दांत स्पष्ट करणे.
२. भगवद्गीतेतील अचूक अध्याय आणि श्लोकाचा संदर्भ देणे (संस्कृत श्लोक आणि त्याचा सोपा मराठी अर्थ).
३. हा विचार दैनंदिन जीवनात कसा आचरायचा, याची २ ते ३ व्यावहारिक पावले (Actionable Advice) देणे.
तुझा सूर नेहमी प्रेमळ, सकारात्मक, संयमी आणि मार्गदर्शकासारखा असावा.
"""

st.title("🕉️ भगवद्गीता सारथी")
st.caption("तुमच्या मनातील प्रश्न आणि समस्यांवर भगवद्गीतेच्या प्रकाशात अचूक मार्गदर्शन")

# API Key व्यवस्थापन
api_key = st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    api_key = st.sidebar.text_input("तुमची Gemini API Key टाका:", type="password")

if not api_key:
    st.info("कृपया पुढे जाण्यासाठी तुमची Gemini API Key टाका.", icon="ℹ️")
    st.stop()

# Client सुरू करणे
client = genai.Client(api_key=api_key)

# चॅट हिस्ट्री
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# युझरचा प्रश्न घेणे
if user_prompt := st.chat_input("तुमचा प्रश्न किंवा समस्या येथे लिहा..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("सारथी विचार करत आहेत..."):
            try:
                history_contents = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    history_contents.append(
                        types.Content(
                            role=role,
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=history_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7
                    )
                )
                
                reply_text = response.text
                st.markdown(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})

            except Exception as e:
                st.error(f"काहीतरी त्रुटी आली: {e}")
