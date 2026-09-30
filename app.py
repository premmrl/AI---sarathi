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

# ४. भाषेनुसार आणि डोमेननुसार डायनॅमिक मजकूर (सर्व मजकूर व फूटरसह)
is_business = "Business" in mode

translations = {
    "मराठी": {
        "personal": "तुमचा प्रश्न किंवा समस्या येथे लिहा...",
        "business": "तुमचा व्यावसायिक संभ्रम किंवा प्रश्न येथे लिहा...",
        "title_p": "🕉️ AI सारथी",
        "desc_p": "तुमच्या मनातील प्रश्न आणि समस्यांवर भगवद्गीतेच्या प्रकाशात अचूक मार्गदर्शन",
        "title_b": "💼 🕉️ AI सारथी — Business & Wealth",
        "desc_b": "व्यापार, नेतृत्व आणि आर्थिक गुंतवणुकीसाठी भगवद्गीतेवर आधारित व्यवस्थापकीय मार्गदर्शन",
        "thinking": "सारथी विचार करत आहेत...",
        "footer_desc": "प्रकल्प संकल्पना व संचलन: <b>Vighnaharta Gold Foundation</b><br>भगवद्गीतेच्या तत्त्वांवर आधारित समाजहितैषी डिजिटल उपक्रम"
    },
    "हिंदी": {
        "personal": "अपनी समस्या या प्रश्न यहाँ लिखें...",
        "business": "अपनी व्यावसायिक दुविधा या निवेश संबंधी प्रश्न यहाँ लिखें...",
        "title_p": "🕉️ AI सारथी",
        "desc_p": "आपके जीवन के प्रश्नों और समस्याओं का भगवद्गीता के प्रकाश में सटीक मार्गदर्शन",
        "title_b": "💼 🕉️ AI सारथी — Business & Wealth",
        "desc_b": "व्यापार, नेतृत्व और वित्तीय निवेश के लिए भगवद्गीता पर आधारित प्रबंधकीय मार्गदर्शन",
        "thinking": "सारथी विचार कर रहे हैं...",
        "footer_desc": "परियोजना संकल्पना एवं संचालन: <b>Vighnaharta Gold Foundation</b><br>भगवद्गीता के सिद्धांतों पर आधारित लोक-कल्याणकारी डिजिटल पहल"
    },
    "English": {
        "personal": "Type your life question or dilemma here...",
        "business": "Enter your business challenge or investment query here...",
        "title_p": "🕉️ AI Sarathi",
        "desc_p": "Timeless guidance from the Bhagavad Gita for modern life's challenges",
        "title_b": "💼 🕉️ AI Sarathi — Business & Wealth",
        "desc_b": "Managerial and strategic wisdom from the Bhagavad Gita for business and wealth",
        "thinking": "Sarathi is reflecting...",
        "footer_desc": "Project Concept & Initiative: <b>Vighnaharta Gold Foundation</b><br>A community-focused digital initiative based on the teachings of Bhagavad Gita"
    },
    "ગુજરાતી (Gujarati)": {
        "personal": "તમારો પ્રશ્ન અથવા મૂંઝવણ અહીં લખો...",
        "business": "તમારો વ્યવસાયિક પ્રશ્ન અહીં લખો...",
        "title_p": "🕉️ AI સારથી",
        "desc_p": "જીવનની સમસ્યાઓનું ભગવદ્ગીતાના પ્રકાશમાં માર્ગદર્શન",
        "title_b": "💼 🕉️ AI સારથી — Business & Wealth",
        "desc_b": "વેપાર અને રોકાણ માટે ભગવદ્ગીતા આધારિત માર્ગદર્શન",
        "thinking": "સારથી વિચારી રહ્યા છે...",
        "footer_desc": "પ્રોજેક્ટ સંકલ્પના અને સંચાલન: <b>Vighnaharta Gold Foundation</b><br>ભગવદ્ગીતાના સિદ્ધાંતો પર આધારિત લોકકલ્યાણકારી ડિજિટલ પહેલ"
    },
    "ಕನ್ನಡ (Kannada)": {
        "personal": "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಬರೆಯಿರಿ...",
        "business": "ನಿಮ್ಮ ವ್ಯಾಪಾರ ಅಥವಾ ಹೂಡಿಕೆ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಬರೆಯಿರಿ...",
        "title_p": "🕉️ AI ಸಾರಥಿ",
        "desc_p": "ಭಗವದ್ಗೀತೆಯ ಬೆಳಕಿನಲ್ಲಿ ಜೀವನದ ಮಾರ್ಗದರ್ಶನ",
        "title_b": "💼 🕉️ AI ಸಾರಥಿ — Business & Wealth",
        "desc_b": "ವ್ಯವಹಾರ ಮತ್ತು ಹೂಡಿಕೆಗಾಗಿ ಭಗವದ್ಗೀತೆ ಆಧಾರಿತ ಮಾರ್ಗದರ್ಶನ",
        "thinking": "ಸಾರಥಿ ಯೋಚಿಸುತ್ತಿದ್ದಾರೆ...",
        "footer_desc": "ಯೋಜನೆಯ ಪರಿಕಲ್ಪನೆ ಮತ್ತು ನಿರ್ವಹಣೆ: <b>Vighnaharta Gold Foundation</b><br>ಭಗವದ್ಗೀತೆಯ ತತ್ವಗಳ ಆಧಾರದ ಮೇಲೆ ಡಿಜಿಟಲ್ ಉಪಕ್ರಮ"
    },
    "తెలుగు (Telugu)": {
        "personal": "మీ ప్రశ్నను ఇక్కడ రాయండి...",
        "business": "మీ వ్యాపార లేదా పెట్టుబడి ప్రశ్నను ఇక్కడ రాయండి...",
        "title_p": "🕉️ AI సారథి",
        "desc_p": "భగవద్గీత వెలుగులో జీవిత సమస్యలకు మార్గదర్శనం",
        "title_b": "💼 🕉️ AI సారథి — Business & Wealth",
        "desc_b": "వ్యాపారం మరియు పెట్టుబడులకు భగవద్గీత ఆధారిత మార్గదర్శనం",
        "thinking": "సారథి ఆలోచిస్తున్నారు...",
        "footer_desc": "ప్రాజెక్ట్ కాన్సెప్ట్ మరియు నిర్వహణ: <b>Vighnaharta Gold Foundation</b><br>భగవద్గీత సూత్రాల ఆధారంగా ఒక డిజిటల్ కార్యక్రమం"
    },
    "தமிழ் (Tamil)": {
        "personal": "உங்கள் கேள்வியை இங்கே எழுதுங்கள்...",
        "business": "உங்கள் வணிகம் அல்லது முதலீட்டு கேள்வியை இங்கே எழுதுங்கள்...",
        "title_p": "🕉️ AI சாரதி",
        "desc_p": "பகவத் கீதையின் வழிகாட்டுதலில் தீர்வுகள்",
        "title_b": "💼 🕉️ AI சாரதி — Business & Wealth",
        "desc_b": "வணிகம் மற்றும் முதலீட்டிற்கான பகவத் கீதை வழிகாட்டுதல்",
        "thinking": "சாரதி சிந்திக்கிறார்...",
        "footer_desc": "திட்ட கருத்து மற்றும் வழிகாட்டுதல்: <b>Vighnaharta Gold Foundation</b><br>பகவத் கீதையின் கொள்கைகளை அடிப்படையாகக் கொண்ட டிஜிட்டல் முயற்சி"
    },
    "বাংলা (Bengali)": {
        "personal": "আপনার প্রশ্ন এখানে লিখুন...",
        "business": "আপনার ব্যবসায়িক বা বিনিয়োগ প্রশ্ন এখানে লিখুন...",
        "title_p": "🕉️ AI সারথি",
        "desc_p": "ভগবদ্গীতার আলোকে জীবনের সঠিক পথনির্দেশ",
        "title_b": "💼 🕉️ AI সারথি — Business & Wealth",
        "desc_b": "ব্যবসা ও বিনিয়োগের জন্য ভগবদ্গীতা ভিত্তিক পরামর্শ",
        "thinking": "সারথি চিন্তা করছেন...",
        "footer_desc": "প্রকল্প পরিকল্পনা ও পরিচালনা: <b>Vighnaharta Gold Foundation</b><br>ভগবদ্গীতার নীতির ওপর ভিত্তি করে জনকল্যাণমূলক ডিজিটাল উদ্যোগ"
    },
    "മലയാളം (Malayalam)": {
        "personal": "നിങ്ങളുടെ ചോദ്യം ഇവിടെ എഴുതുക...",
        "business": "നിങ്ങളുടെ ബിസിനസ്സ് ചോദ്യം ഇവിടെ എഴുതുക...",
        "title_p": "🕉️ AI സാരഥി",
        "desc_p": "ഭഗവദ്ഗീതയുടെ വെളിച്ചത്തിൽ ജീവിത മാർഗ്ഗദർശനം",
        "title_b": "💼 🕉️ AI സാരഥി — Business & Wealth",
        "desc_b": "ബിസിനസ്സിനും നിക്ഷേപത്തിനുമുള്ള ഭഗവദ്ഗീത മാർഗ്ഗദർശനം",
        "thinking": "സാരഥി ചിന്തിക്കുന്നു...",
        "footer_desc": "പദ്ധതി ആശയം: <b>Vighnaharta Gold Foundation</b><br>ഭഗവദ്ഗീതയുടെ തത്വങ്ങളെ അടിസ്ഥാനമാക്കിയുള്ള ഡിജിറ്റൽ സംരംഭം"
    },
    "ਪੰਜਾਬੀ (Punjabi)": {
        "personal": "ਆਪਣਾ ਸਵਾਲ ਇੱਥੇ ਲਿਖੋ...",
        "business": "ਆਪਣਾ ਕਾਰੋਬਾਰੀ ਜਾਂ ਨਿਵੇਸ਼ ਸਵਾਲ ਇੱਥੇ ਲਿਖੋ...",
        "title_p": "🕉️ AI ਸਾਰਥੀ",
        "desc_p": "ਭਗਵਦ ਗੀਤਾ ਦੀ ਰੌਸ਼ਨੀ ਵਿੱਚ ਜੀਵਨ ਦਾ ਮਾਰਗਦਰਸ਼ਨ",
        "title_b": "💼 🕉️ AI ਸਾਰਥੀ — Business & Wealth",
        "desc_b": "ਕਾਰੋਬਾਰ ਅਤੇ ਨਿਵੇਸ਼ ਲਈ ਗੀਤਾ ਅਧਾਰਤ ਮਾਰਗਦਰਸ਼ਨ",
        "thinking": "ਸਾਰਥੀ ਸੋਚ ਰਹੇ ਹਨ...",
        "footer_desc": "ਪ੍ਰੋਜੈਕਟ ਸੰਕਲਪ ਅਤੇ ਪ੍ਰਬੰਧਨ: <b>Vighnaharta Gold Foundation</b><br>ਭਗਵਦ ਗੀਤਾ ਦੇ ਸਿਧਾਂਤਾਂ 'ਤੇ ਆਧਾਰਿਤ ਡਿਜੀਟਲ ਪਹਿਲਕਦਮੀ"
    }
}

lang_data = translations.get(language, translations["मराठी"])

# शीर्षके आणि इनपुट बॉक्स
if is_business:
    st.title(lang_data["title_b"])
    st.caption(lang_data["desc_b"])
    current_input_placeholder = lang_data["business"]
else:
    st.title(lang_data["title_p"])
    st.caption(lang_data["desc_p"])
    current_input_placeholder = lang_data["personal"]

# ५. सिस्टीम मार्गदर्शक सूचना
if is_business:
    DOMAIN_PROMPT = """
तू 'AI सारथी - Business & Wealth Edition' आहेस. 
वापरकर्ता व्यावसायिक, उद्योजक, लीडर किंवा गुंतवणूकदार आहे. त्याचे प्रश्न व्यापार वाढवणे, नेतृत्व, तोटा, बाजारातील मंदी, जोखीम व्यवस्थापन (Risk Management) किंवा आर्थिक गुंतवणुकीतील निर्णय याविषयी असतील.

तुझे काम:
१. समस्येचे आणि व्यावसायिक उद्दिष्टाचे संक्षिप्त व प्रभावी विश्लेषण.
२. भगवद्गीतेतील अचूक अध्याय व श्लोकाचा संदर्भ आणि त्याचा आधुनिक व्यापार/गुंतवणूक संदर्भातील अर्थ.
३. २ ते ३ व्यावहारिक आणि रणनीतिक पावले (Actionable Strategic Steps).
उत्तर धोरणी, थेट आणि व्यावसायिक असावे.
"""
else:
    DOMAIN_PROMPT = """
तू 'AI सारथी' आहेस - एक मार्गदर्शक, मित्र आणि तत्त्वज्ञ.
वापरकर्ता दैनंदिन जीवनातील चिंता, नाती, करिअर, अपयश, राग किंवा इतर कोणताही प्रश्न विचारेल.

तुझे काम:
१. मानसिक दिलासा आणि समस्येचे मूळ कारण सोप्या शब्दांत सांगणे.
२. भगवद्गीतेतील अचूक अध्याय आणि श्लोकाचा संदर्भ (संस्कृत श्लोक आणि सोपा अर्थ).
३. २ ते ३ व्यावहारिक पावले (Actionable Advice).
उत्तर प्रेमळ, सकारात्मक आणि सुटसुटीत असावे.
"""

SYSTEM_INSTRUCTION = f"""
{DOMAIN_PROMPT}

नियम: वापरकर्त्याने निवडलेल्या भाषेतच संपूर्ण उत्तर दे.
सध्या निवडलेली भाषा: {language}
"""

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

# ९. प्रश्न घेणे आणि थेट निवडलेल्या भाषेत उत्तर देणे
if user_prompt := st.chat_input(current_input_placeholder):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner(lang_data["thinking"]):
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
                st.error("सर्व्हर प्रतिसाद मिळण्यात अडचण येत आहे. कृपया थोड्या वेळाने प्रयत्न करा.")

# १०. तळाशी भाषेनुसार बदलणारा ब्रँडिंग फूटर
st.markdown(f"""
    <div class='footer-container'>
        <div class='brand-title'>An Initiative by Vighnaharta Gold Foundation</div>
        <div class='footer-text'>
            {lang_data["footer_desc"]}
        </div>
    </div>
""", unsafe_allow_html=True)
