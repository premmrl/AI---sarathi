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

# ३. सर्व १० भाषांनुसार डेटा
translations = {
    "मराठी": {
        "domain_label": "🎯 मार्गदर्शन क्षेत्र:",
        "opt_personal": "जीवन व वैयक्तिक समस्या",
        "opt_business": "व्यवसाय व आर्थिक गुंतवणूक",
        "personal_placeholder": "तुमचा प्रश्न किंवा समस्या येथे लिहा...",
        "business_placeholder": "तुमचा व्यावसायिक संभ्रम किंवा प्रश्न येथे लिहा...",
        "title_p": "🕉️ AI सारथी",
        "desc_p": "तुमच्या मनातील प्रश्न आणि समस्यांवर भगवद्गीतेच्या प्रकाशात अचूक मार्गदर्शन",
        "title_b": "💼 🕉️️ AI सारथी — Business & Wealth",
        "desc_b": "व्यापार, नेतृत्व आणि आर्थिक गुंतवणुकीसाठी भगवद्गीतेवर आधारित व्यवस्थापकीय मार्गदर्शन",
        "thinking": "सारथी विचार करत आहेत...",
        "footer_desc": "प्रकल्प संकल्पना व संचलन: <b>Vighnaharta Gold Foundation</b><br>भगवद्गीतेच्या तत्त्वांवर आधारित समाजहितैषी डिजिटल उपक्रम"
    },
    "हिंदी": {
        "domain_label": "🎯 मार्गदर्शन क्षेत्र:",
        "opt_personal": "जीवन एवं व्यक्तिगत चुनौतियाँ",
        "opt_business": "व्यापार एवं वित्तीय निवेश",
        "personal_placeholder": "अपनी समस्या या प्रश्न यहाँ लिखें...",
        "business_placeholder": "अपनी व्यावसायिक दुविधा या निवेश संबंधी प्रश्न यहाँ लिखें...",
        "title_p": "🕉️ AI सारथी",
        "desc_p": "आपके जीवन के प्रश्नों और समस्याओं का भगवद्गीता के प्रकाश में सटीक मार्गदर्शन",
        "title_b": "💼 🕉️ AI सारथी — Business & Wealth",
        "desc_b": "व्यापार, नेतृत्व और वित्तीय निवेश के लिए भगवद्गीता पर आधारित प्रबंधकीय मार्गदर्शन",
        "thinking": "सारथी विचार कर रहे हैं...",
        "footer_desc": "परियोजना संकल्पना एवं संचालन: <b>Vighnaharta Gold Foundation</b><br>भगवद्गीता के सिद्धांतों पर आधारित लोक-कल्याणकारी डिजिटल पहल"
    },
    "English": {
        "domain_label": "🎯 Guidance Domain:",
        "opt_personal": "Life & Personal Challenges",
        "opt_business": "Business & Wealth / Investments",
        "personal_placeholder": "Type your life question or dilemma here...",
        "business_placeholder": "Enter your business challenge or investment query here...",
        "title_p": "🕉️ AI Sarathi",
        "desc_p": "Timeless guidance from the Bhagavad Gita for modern life's challenges",
        "title_b": "💼 🕉️ AI Sarathi — Business & Wealth",
        "desc_b": "Managerial and strategic wisdom from the Bhagavad Gita for business and wealth",
        "thinking": "Sarathi is reflecting...",
        "footer_desc": "Project Concept & Initiative: <b>Vighnaharta Gold Foundation</b><br>A community-focused digital initiative based on the teachings of Bhagavad Gita"
    },
    "ગુજરાતી (Gujarati)": {
        "domain_label": "🎯 માર્ગદર્શન ક્ષેત્ર:",
        "opt_personal": "જીવન અને વ્યક્તિગત પ્રશ્નો",
        "opt_business": "વેપાર અને આર્થિક રોકાણ",
        "personal_placeholder": "તમારો પ્રશ્ન અથવા મૂંઝવણ અહીં લખો...",
        "business_placeholder": "તમારો વ્યવસાયિક પ્રશ્ન અહીં લખો...",
        "title_p": "🕉️ AI સારથી",
        "desc_p": "જીવનની સમસ્યાઓનું ભગવદ્ગીતાના પ્રકાશમાં માર્ગદર્શન",
        "title_b": "💼 🕉️ AI સારથી — Business & Wealth",
        "desc_b": "વેપાર અને રોકાણ માટે ભગવદ્ગીતા આધારિત માર્ગદર્શન",
        "thinking": "સારથી વિચારી રહ્યા છે...",
        "footer_desc": "પ્રોજેક્ટ સંકલ્પના અને સંચાલન: <b>Vighnaharta Gold Foundation</b><br>ભગવદ્ગીતાના સિદ્ધાંતો પર આધારિત લોકકલ્યાણકારી ડિજિટલ પહેલ"
    },
    "ಕನ್ನಡ (Kannada)": {
        "domain_label": "🎯 ಮಾರ್ಗದರ್ಶನ ಕ್ಷೇತ್ರ:",
        "opt_personal": "ಜೀವನ ಮತ್ತು ವೈಯಕ್ತಿಕ ಸವಾಲುಗಳು",
        "opt_business": "ವ್ಯವಹಾರ ಮತ್ತು ಆರ್ಥಿಕ ಹೂಡಿಕೆ",
        "personal_placeholder": "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಬರೆಯಿರಿ...",
        "business_placeholder": "ನಿಮ್ಮ ವ್ಯಾಪಾರ ಅಥವಾ ಹೂಡಿಕೆ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಬರೆಯಿರಿ...",
        "title_p": "🕉️ AI ಸಾರಥಿ",
        "desc_p": "ಭಗವದ್ಗೀತೆಯ ಬೆಳಕಿನಲ್ಲಿ ಜೀವನದ ಮಾರ್ಗದರ್ಶನ",
        "title_b": "💼 🕉️ AI ಸಾರಥಿ — Business & Wealth",
        "desc_b": "ವ್ಯವಹಾರ ಮತ್ತು ಹೂಡಿಕೆಗಾಗಿ ಭಗವದ್ಗೀತೆ ಆಧಾರಿತ ಮಾರ್ಗದರ್ಶನ",
        "thinking": "ಸಾರಥಿ ಯೋಚಿಸುತ್ತಿದ್ದಾರೆ...",
        "footer_desc": "ಯೋಜನೆಯ ಪರಿಕಲ್ಪನೆ ಮತ್ತು ನಿರ್ವಹಣೆ: <b>Vighnaharta Gold Foundation</b><br>ಭಗವದ್ಗೀತೆಯ ತತ್ವಗಳ ಆಧಾರದ ಮೇಲೆ ಡಿಜಿಟಲ್ ಉಪಕ್ರಮ"
    },
    "తెలుగు (Telugu)": {
        "domain_label": "🎯 మార్గదర్శక రంగం:",
        "opt_personal": "జీవితం మరియు వ్యక్తిగత సమస్యలు",
        "opt_business": "వ్యాపారం మరియు పెట్టుబడులు",
        "personal_placeholder": "మీ ప్రశ్నను ఇక్కడ రాయండి...",
        "business_placeholder": "మీ వ్యాపార లేదా పెట్టుబడి ప్రశ్నను ఇక్కడ రాయండి...",
        "title_p": "🕉️ AI సారథి",
        "desc_p": "భగవద్గీత వెలుగులో జీవిత సమస్యలకు మార్గదర్శనం",
        "title_b": "💼 🕉️ AI సారథి — Business & Wealth",
        "desc_b": "వ్యాపారం మరియు పెట్టుబడులకు భగవద్గీత ఆధారిత మార్గదర్శనం",
        "thinking": "సారథి ఆలోచిస్తున్నారు...",
        "footer_desc": "ప్రాజెక్ట్ కాన్సెప్ట్ మరియు నిర్వహణ: <b>Vighnaharta Gold Foundation</b><br>భగవద్గీత సూత్రాల ఆధారంగా ఒక డిజిటల్ కార్యక్రమం"
    },
    "தமிழ் (Tamil)": {
        "domain_label": "🎯 வழிகாட்டுதல் துறை:",
        "opt_personal": "வாழ்க்கை மற்றும் தனிப்பட்ட சவால்கள்",
        "opt_business": "வணிகம் மற்றும் முதலீடுகள்",
        "personal_placeholder": "உங்கள் கேள்வியை இங்கே எழுதுங்கள்...",
        "business_placeholder": "உங்கள் வணிகம் அல்லது முதலீட்டு கேள்வியை இங்கே எழுதுங்கள்...",
        "title_p": "🕉️ AI சாரதி",
        "desc_p": "பகவத் கீதையின் வழிகாட்டுதலில் தீர்வுகள்",
        "title_b": "💼 🕉️ AI சாரதி — Business & Wealth",
        "desc_b": "வணிகம் மற்றும் முதலீட்டிற்கான பகவத் கீதை வழிகாட்டுதல்",
        "thinking": "சாரதி சிந்திக்கிறார்...",
        "footer_desc": "திட்ட கருத்து மற்றும் வழிகாட்டுதல்: <b>Vighnaharta Gold Foundation</b><br>பகவத் கீதையின் கொள்கைகளை அடிப்படையாகக் கொண்ட டிஜிட்டல் முயற்சி"
    },
    "বাংলা (Bengali)": {
        "domain_label": "🎯 দিকনির্দেশনার ক্ষেত্র:",
        "opt_personal": "জীবন ও व्यक्तिगत समस्या",
        "opt_business": "ব্যবসা ও আর্থিক বিনিয়োগ",
        "personal_placeholder": "আপনার প্রশ্ন এখানে লিখুন...",
        "business_placeholder": "আপনার ব্যবসায়িক বা বিনিয়োগ प्रश्न এখানে লিখুন...",
        "title_p": "🕉️ AI সারথি",
        "desc_p": "ভগবদ্গীতার আলোকে জীবনের সঠিক পথনির্দেশ",
        "title_b": "💼 🕉️ AI সারথি — Business & Wealth",
        "desc_b": "ব্যবসা ও বিনিয়োগের জন্য ভগবদ্গীতা ভিত্তিক পরামর্শ",
        "thinking": "সারথি চিন্তা করছেন...",
        "footer_desc": "প্রকল্প পরিকল্পনা ও পরিচালনা: <b>Vighnaharta Gold Foundation</b><br>ভগবদ্গীতার নীতির ওপর ভিত্তি করে জনকল্যাণমূলক ডিজিটাল উদ্যোগ"
    },
    "മലയാളം (Malayalam)": {
        "domain_label": "🎯 മാർഗ്ഗദർശന മേഖല:",
        "opt_personal": "ജീവിതവും വ്യക്തിഗത വെല്ലുവിളികളും",
        "opt_business": "ബിസിനസ്സും സാമ്പത്തിക നിക്ഷേപവും",
        "personal_placeholder": "നിങ്ങളുടെ ചോദ്യം ഇവിടെ എഴുതുക...",
        "business_placeholder": "നിങ്ങളുടെ ബിസിനസ്സ് ചോദ്യം ഇവിടെ എഴുതുക...",
        "title_p": "🕉️ AI സാരഥി",
        "desc_p": "ഭഗവദ്ഗീതയുടെ വെളിച്ചത്തിൽ ജീവിത മാർഗ്ഗദർശനം",
        "title_b": "💼 🕉️ AI സാരഥി — Business & Wealth",
        "desc_b": "ബിസിനസ്സിനും നിക്ഷേപത്തിനുമുള്ള ഭഗവദ്ഗീത മാർഗ്ഗദർശനം",
        "thinking": "സാരഥി ചിന്തിക്കുന്നു...",
        "footer_desc": "പദ്ധതി ആശയം: <b>Vighnaharta Gold Foundation</b><br>ഭഗവദ്ഗീതയുടെ തത്വങ്ങളെ അടിസ്ഥാനമാക്കിയുള്ള ഡിജിറ്റൽ സംരംഭം"
    },
    "ਪੰਜਾਬੀ (Punjabi)": {
        "domain_label": "🎯 ਮਾਰਗਦਰਸ਼ਨ ਖੇਤਰ:",
        "opt_personal": "ਜੀਵਨ ਅਤੇ ਨਿੱਜੀ ਚੁਣੌਤੀਆਂ",
        "opt_business": "ਕਾਰੋਬਾਰ ਅਤੇ ਵਿੱਤੀ ਨਿਵੇਸ਼",
        "personal_placeholder": "ਆਪਣਾ ਸਵਾਲ ਇੱਥੇ ਲਿਖੋ...",
        "business_placeholder": "ਆਪਣਾ ਕਾਰੋਬਾਰੀ ਜਾਂ ਨਿਵੇਸ਼ ਸਵਾਲ ਇੱਥੇ ਲਿਖੋ...",
        "title_p": "🕉️ AI ਸਾਰਥੀ",
        "desc_p": "ਭਗਵਦ ਗੀਤਾ ਦੀ ਰੌਸ਼ਨੀ ਵਿੱਚ ਜੀਵਨ ਦਾ ਮਾਰਗਦਰਸ਼ਨ",
        "title_b": "💼 🕉️ AI ਸਾਰਥੀ — Business & Wealth",
        "desc_b": "ਕਾਰੋਬਾਰ ਅਤੇ ਨਿਵੇਸ਼ ਲਈ ਗੀਤਾ ਅਧਾਰਤ ਮਾਰਗਦਰਸ਼ਨ",
        "thinking": "ਸਾਰਥੀ ਸੋਚ ਰਹੇ ਹਨ...",
        "footer_desc": "ਪ੍ਰੋਜੈਕਟ ਸੰਕਲਪ ਅਤੇ ਪ੍ਰਬੰਧਨ: <b>Vighnaharta Gold Foundation</b><br>ਭਗਵਦ ਗੀਤਾ ਦੇ ਸਿਧਾਂਤਾਂ 'ਤੇ ਆਧਾਰਿਤ ਡਿਜੀਟਲ ਪਹਿਲਕਦਮੀ"
    }
}

# ४. भाषा व डोमेन निवड
col1, col2 = st.columns([1, 1.2])

with col1:
    language = st.selectbox(
        "🌐 Language / भाषा:",
        list(translations.keys())
    )

lang_data = translations.get(language, translations["मराठी"])

with col2:
    mode_options = [lang_data["opt_personal"], lang_data["opt_business"]]
    selected_mode = st.selectbox(
        lang_data["domain_label"],
        mode_options
    )

is_business = (selected_mode == lang_data["opt_business"])

# ५. शीर्षके व प्लेसहोल्डर
if is_business:
    st.title(lang_data["title_b"])
    st.caption(lang_data["desc_b"])
    current_input_placeholder = lang_data["business_placeholder"]
else:
    st.title(lang_data["title_p"])
    st.caption(lang_data["desc_p"])
    current_input_placeholder = lang_data["personal_placeholder"]

# ६. थेट आणि संक्षिप्त सिस्टीम प्रॉम्प्ट (कमी टोकन्स = प्रचंड वेग)
if is_business:
    DOMAIN_PROMPT = """
तू 'AI सारथी - Business & Wealth Edition' आहेस. 
व्यावसायिक किंवा गुंतवणूकदाराच्या प्रश्नावर थेट, वेगाने व अचूक उत्तर दे:
१. समस्येचे संक्षिप्त विश्लेषण (२ ओळींत).
२. भगवद्गीतेतील अचूक श्लोक आणि आधुनिक व्यापार/गुंतवणुकीतील अर्थ.
३. लगेच करता येण्यासारखी २ ते ३ ठोस रणनीतिक पावले (Actionable Steps).
"""
else:
    DOMAIN_PROMPT = """
तू 'AI सारथी' आहेस - एक मार्गदर्शक आणि तत्त्वज्ञ.
वापरकर्त्याच्या प्रश्नावर थेट आणि सुटसुटीत उत्तर दे:
१. मानसिक दिलासा आणि समस्येचे मूळ कारण.
२. भगवद्गीतेतील अचूक श्लोक व सोपा अर्थ.
३. दैनंदिन जीवनातील २ ते ३ व्यावहारिक पावले.
"""

SYSTEM_INSTRUCTION = f"""
{DOMAIN_PROMPT}
नियम: संपूर्ण उत्तर केवळ {language} या भाषेतच दे.
"""

# ७. API Key व्यवस्थापन
api_key = st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    api_key = st.sidebar.text_input("Gemini API Key:", type="password")

if not api_key:
    st.info("कृपया पुढे जाण्यासाठी API Key आवश्यक आहे.", icon="ℹ️")
    st.stop()

# ८. Client
client = genai.Client(api_key=api_key)

# ९. चॅट हिस्ट्री
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# १०. प्रश्न घेणे आणि थेट फास्ट मॉडेलद्वारे उत्तर देणे
if user_prompt := st.chat_input(current_input_placeholder):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner(lang_data["thinking"]):
            # कोटा वाचवण्यासाठी फक्त सध्याचा प्रश्न पाठवणे
            history_contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=user_prompt)]
                )
            ]

            reply_text = None
            error_details = ""
            
            # कमाल कोटा आणि अतिजलद प्रतिसाद देणारे मॉडेल
            models = ["gemini-2.5-flash-lite", "gemini-2.5-flash"]

            for m in models:
                try:
                    response = client.models.generate_content(
                        model=m,
                        contents=history_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                            temperature=0.7
                        )
                    )
                    if response and response.text:
                        reply_text = response.text
                        break
                except Exception as err:
                    error_details = str(err)
                    continue

            if reply_text:
                st.markdown(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})
            else:
                if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                    st.session_state.messages.pop()
                st.error("सर्व्हरशी संपर्क होऊ शकला नाही. कृपया १ मिनिटाने पुन्हा प्रयत्न करा.")
                if error_details:
                    with st.expander("तांत्रिक तपशील (Technical Details)"):
                        st.caption(error_details)

# ११. तळाशी ब्रँडिंग फूटर
st.markdown(f"""
    <div class='footer-container'>
        <div class='brand-title'>An Initiative by Vighnaharta Gold Foundation</div>
        <div class='footer-text'>
            {lang_data["footer_desc"]}
        </div>
    </div>
""", unsafe_allow_html=True)
