import streamlit as st
import google.generativeai as genai

# १. पेज सेटिंग्ज
st.set_page_config(
    page_title="AI सारथी | Gita AI Guide",
    page_icon="🕉️️",
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

# ३. सिस्टीम मार्गदर्शक सूचना
SYSTEM_INSTRUCTION = """
तू 'AI सारथी' आहेस - एक मार्गदर्शक, मित्र आणि तत्त्वज्ञ.
वापरकर्ता दैनंदिन जीवनातील चिंता, नाती, करिअर, अपयश, राग किंवा इतर कोणताही प्रश्न कोणत्याही भाषेत विचारेल.

महत्त्वाचा नियम: वापरकर्त्याने निवडलेल्या भाषेत (किंवा ज्या भाषेत प्रश्न विचारला आहे), त्याला संपूर्ण उत्तर त्याच भाषेत दे (उदा. गुजरातीमध्ये विचारल्यास गुजरातीत, तमिळमध्ये विचारल्यास तमिळमध्ये, मराठीत विचारल्यास मराठीत).

तुझे काम खालील रचनेनुसार उत्तर देणे आहे:
१. मानसिक दिलासा आणि समस्येचे मूळ कारण सोप्या शब्दांत स्पष्ट करणे.
२. भगवद्गीतेतील अचूक अध्याय आणि श्लोकाचा संदर्भ देणे (मूळ संस्कृत श्लोक आणि त्याचा निवडलेल्या भाषेत सोपा अर्थ).
३. हा विचार दैनंदिन जीवनात कसा आचरायचा, याची २ ते ३ व्यावहारिक पावले (Actionable Advice) देणे.

तुझा सूर नेहमी प्रेमळ, सकारात्मक, संयमी आणि मार्गदर्शकासारखा असावा.
"""

# ४. भाषा निवड (१० प्रमुख भारतीय भाषा)
language = st.selectbox(
    "🌐 Choose Language / भाषा निवडा / अपनी भाषा चुनें:",
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

# ५. निवडलेल्या भाषेनुसार शीर्षके
titles = {
    "मराठी": ("🕉️ AI सारथी", "तुमच्या मनातील प्रश्न आणि समस्यांवर भगवद्गीतेच्या प्रकाशात अचूक मार्गदर्शन", "तुमचा प्रश्न किंवा समस्या येथे लिहा...", "सारथी विचार करत आहेत..."),
    "हिंदी": ("🕉️ AI सारथी", "आपके जीवन के प्रश्नों और समस्याओं का भगवद्गीता के प्रकाश में सटीक मार्गदर्शन", "अपनी समस्या या प्रश्न यहाँ लिखें...", "सारथी विचार कर रहे हैं..."),
    "English": ("🕉️ AI Sarathi", "Timeless guidance from the Bhagavad Gita for modern life's challenges", "Type your question or dilemma here...", "Sarathi is reflecting..."),
    "ગુજરાતી (Gujarati)": ("🕉️ AI સારથી", "તમારા જીવનના પ્રશ્નો અને સમસ્યાઓનું ભગવદ્ગીતાના પ્રકાશમાં માર્ગદર્શન", "તમારો પ્રશ્ન અહીં લખો...", "સારથી વિચારી રહ્યા છે..."),
    "ಕನ್ನಡ (Kannada)": ("🕉️ AI ಸಾರಥಿ", "ನಿಮ್ಮ ಜೀವನದ ಸಮಸ್ಯೆಗಳಿಗೆ ಭಗವದ್ಗೀತೆಯ ಬೆಳಕಿನಲ್ಲಿ ಮಾರ್ಗದರ್ಶನ", "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಬರೆಯಿರಿ...", "ಸಾರಥಿ ಯೋಚಿಸುತ್ತಿದ್ದಾರೆ..."),
    "తెలుగు (Telugu)": ("🕉 AI సారథి", "భగవద్గీత వెలుగులో మీ సమస్యలకు సరైన మార్గదర్శనం", "మీ ప్రశ్నను ఇక్కడ రాయండి...", "సారథి ఆలోచిస్తున్నారు..."),
    "தமிழ் (Tamil)": ("🕉 AI சாரதி", "பகவத் கீதையின் வழிகாட்டுதலில் உங்கள் கேள்விகளுக்கான தீர்வு", "உங்கள் கேள்வியை இங்கே எழுதுங்கள்...", "சாரதி சிந்திக்கிறார்..."),
    "বাংলা (Bengali)": ("🕉️ AI সারথি", "ভগবদ্গীতার আলোকে আপনার জীবনের সমস্যা ও প্রশ্নের সমাধান", "আপনার प्रश्न येथे लिहा...", "সারথি চিন্তা করছেন..."),
    "മലയാളം (Malayalam)": ("🕉️ AI സാരഥി", "ഭഗവദ്ഗീതയുടെ വെളിച്ചത്തിൽ നിങ്ങളുടെ പ്രശ്നങ്ങൾക്കുള്ള പരിഹാരം", "നിങ്ങളുടെ ചോദ്യം ഇവിടെ എഴുതുക...", "സാരഥി ചിന്തിക്കുന്നു..."),
    "ਪੰਜਾਬੀ (Punjabi)": ("🕉 AI ਸਾਰਥੀ", "ਭਗਵਦ ਗੀਤਾ ਦੀ ਰੌਸ਼ਨੀ ਵਿੱਚ ਤੁਹਾਡੀਆਂ ਸਮੱਸਿਆਵਾਂ ਦਾ ਸਹੀ ਮਾਰਗਦਰਸ਼ਨ", "ਆਪਣਾ ਸਵਾਲ ਇੱਥੇ ਲਿਖੋ...", "ਸਾਰਥੀ ਸੋਚ ਰਹੇ ਹਨ...")
}
current_title, current_caption, input_placeholder, thinking_text = titles.get(language, titles["मराठी"])

st.title(current_title)
st.caption(current_caption)

# ६. API Key कॉन्फिगरेशन
api_key = st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    st.info("कृपया पुढे जाण्यासाठी API Key आवश्यक आहे.", icon="ℹ️")
    st.stop()

genai.configure(api_key=api_key)

# ७. चॅट हिस्ट्री
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ८. प्रश्न आणि उत्तर
if user_prompt := st.chat_input(input_placeholder):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner(thinking_text):
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=f"{SYSTEM_INSTRUCTION}\nसध्या निवडलेली भाषा: {language}"
                )
                
                history = []
                for msg in st.session_state.messages[:-1]:
                    role = "user" if msg["role"] == "user" else "model"
                    history.append({"role": role, "parts": [msg["content"]]})
                
                chat = model.start_chat(history=history)
                response = chat.send_message(user_prompt)
                
                reply_text = response.text
                st.markdown(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})
            except Exception as e:
                st.error(f"त्रुटी आली आहे: {str(e)}")

# ९. तळाशी ब्रँडिंग फूटर
st.markdown("""
    <div class='footer-container'>
        <div class='brand-title'>An Initiative by Vighnaharta Gold Foundation</div>
        <div class='footer-text'>
            प्रकल्प संकल्पना व संचलन: <b>Vighnaharta Gold Foundation</b><br>
            भगवद्गीतेच्या तत्त्वांवर आधारित समाजहितैषी डिजिटल उपक्रम
        </div>
    </div>
""", unsafe_allow_html=True)
