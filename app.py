import streamlit as st
import google.generativeai as genai
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Dhairya AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== SESSION STATE ====================
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
if 'api_saved' not in st.session_state:
    st.session_state.api_saved = False

# ==================== CSS & ANIMATIONS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
    }
    
    .heading-container {
        text-align: center;
        padding: 3rem 0 2rem 0;
        perspective: 1000px;
    }
    
    .main-heading {
        font-family: 'Orbitron', monospace;
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00f5ff 0%, #7b2ff7 25%, #f107a3 50%, #00f5ff 75%, #7b2ff7 100%);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-shift 3s ease infinite, float-3d 6s ease-in-out infinite;
        text-shadow: 0 0 80px rgba(123, 47, 247, 0.5);
        letter-spacing: 8px;
        transform-style: preserve-3d;
        position: relative;
        display: inline-block;
    }
    
    .main-heading::before {
        content: 'DHAIRYA AI';
        position: absolute;
        left: 0;
        top: 0;
        background: linear-gradient(135deg, #00f5ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        transform: translateZ(-50px) translateY(5px);
        opacity: 0.3;
        filter: blur(3px);
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float-3d {
        0%, 100% { transform: translateY(0px) rotateX(0deg) rotateY(0deg); }
        25% { transform: translateY(-10px) rotateX(2deg) rotateY(-2deg); }
        50% { transform: translateY(0px) rotateX(0deg) rotateY(2deg); }
        75% { transform: translateY(-5px) rotateX(-2deg) rotateY(0deg); }
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.6);
        margin-top: 1rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        animation: fade-in 2s ease-out;
    }
    
    .gemini-badge {
        display: inline-block;
        background: linear-gradient(135deg, #4285f4, #ea4335, #fbbc04, #34a853);
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-top: 0.5rem;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    @keyframes fade-in {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .orb {
        position: fixed;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.4;
        z-index: -1;
        animation: orb-float 10s ease-in-out infinite;
    }
    
    .orb-1 {
        width: 400px;
        height: 400px;
        background: #7b2ff7;
        top: -100px;
        left: -100px;
        animation-delay: 0s;
    }
    
    .orb-2 {
        width: 300px;
        height: 300px;
        background: #00f5ff;
        bottom: -50px;
        right: -50px;
        animation-delay: 2s;
    }
    
    .orb-3 {
        width: 250px;
        height: 250px;
        background: #f107a3;
        top: 50%;
        right: 10%;
        animation-delay: 4s;
    }
    
    @keyframes orb-float {
        0%, 100% { transform: translate(0, 0) scale(1); }
        33% { transform: translate(30px, -30px) scale(1.1); }
        66% { transform: translate(-20px, 20px) scale(0.9); }
    }
    
    .api-container {
        max-width: 600px;
        margin: 2rem auto;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: slide-up 0.8s ease-out;
    }
    
    @keyframes slide-up {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .api-label {
        font-family: 'Inter', sans-serif;
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
    }
    
    .search-container {
        max-width: 800px;
        margin: 2rem auto;
        position: relative;
    }
    
    .search-wrapper {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 50px;
        padding: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .search-wrapper:hover {
        border-color: rgba(123, 47, 247, 0.5);
        box-shadow: 0 10px 60px rgba(123, 47, 247, 0.2);
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    .message-user {
        background: linear-gradient(135deg, #7b2ff7 0%, #f107a3 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0 1rem 20%;
        font-family: 'Inter', sans-serif;
        animation: message-in 0.4s ease-out;
        box-shadow: 0 5px 20px rgba(123, 47, 247, 0.3);
    }
    
    .message-ai {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        color: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 20% 1rem 0;
        font-family: 'Inter', sans-serif;
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: message-in 0.4s ease-out;
        line-height: 1.6;
    }
    
    @keyframes message-in {
        from { opacity: 0; transform: translateY(20px) scale(0.95); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    .ai-avatar {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.6);
    }
    
    .ai-avatar-icon {
        width: 28px;
        height: 28px;
        background: linear-gradient(135deg, #4285f4, #ea4335);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }
    
    .stTextInput > div > div > input {
        background: transparent !important;
        border: none !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        padding: 1rem 1.5rem !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #7b2ff7 0%, #f107a3 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.8rem 2rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 20px rgba(123, 47, 247, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(123, 47, 247, 0.6) !important;
    }
    
    .datetime {
        position: fixed;
        top: 20px;
        right: 30px;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.4);
        text-align: right;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        max-width: 800px;
        margin: 2rem auto;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(123, 47, 247, 0.5);
        box-shadow: 0 10px 30px rgba(123, 47, 247, 0.2);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .feature-desc {
        color: rgba(255, 255, 255, 0.5);
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        margin-top: 0.3rem;
    }
</style>

<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
<div class="orb orb-3"></div>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
now = datetime.now()

st.markdown(f"""
<div class="datetime">
    {now.strftime("%A, %d %B %Y")}<br>
    {now.strftime("%I:%M %p")}
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="heading-container">
    <h1 class="main-heading">DHAIRYA AI</h1>
    <p class="subtitle">Your Intelligent Assistant</p>
    <span class="gemini-badge">⚡ Powered by Google Gemini</span>
</div>
""", unsafe_allow_html=True)

# ==================== API KEY INPUT ====================
if not st.session_state.api_saved:
    st.markdown("""
    <div class="api-container">
        <p class="api-label">🔑 Enter your FREE Google Gemini API Key</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        api_input = st.text_input(
            "API Key",
            type="password",
            placeholder="AIza...",
            label_visibility="collapsed"
        )
        
        col_a, col_b, col_c = st.columns([1, 2, 1])
        
        with col_b:
            if st.button("🚀 Start Chatting", use_container_width=True):
                if api_input and api_input.startswith("AIza"):
                    st.session_state.api_key = api_input
                    st.session_state.api_saved = True
                    st.rerun()
                else:
                    st.error("⚠️ Please enter a valid Gemini API key (starts with AIza)")
        
        st.markdown("""
        <div style="text-align: center; margin-top: 1.5rem;">
            <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-bottom: 0.5rem;">
                ✨ 100% FREE - No Credit Card Required
            </p>
            <a href="https://makersuite.google.com/app/apikey" target="_blank" 
               style="color: #00f5ff; font-size: 0.9rem; text-decoration: none; font-weight: 600;">
                🎁 Get FREE API Key (1 Click) →
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    # Features Grid
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">Smart Conversations</div>
            <div class="feature-desc">Natural language AI</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Lightning Fast</div>
            <div class="feature-desc">Powered by Gemini</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🆓</div>
            <div class="feature-title">100% FREE</div>
            <div class="feature-desc">No credit card needed</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN CHAT INTERFACE ====================
else:
    # Configure Gemini
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    # Display Chat Messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if st.session_state.messages:
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                st.markdown(f'<div class="message-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message-ai">
                    <div class="ai-avatar">
                        <span class="ai-avatar-icon">🤖</span>
                        <span>Dhairya AI</span>
                    </div>
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <p style="color: rgba(255,255,255,0.5); font-family: 'Inter', sans-serif; font-size: 1.1rem;">
                👋 Hello! I'm <strong style="color: #00f5ff;">Dhairya AI</strong>
            </p>
            <p style="color: rgba(255,255,255,0.4); font-family: 'Inter', sans-serif; font-size: 0.9rem; margin-top: 0.5rem;">
                Powered by Google Gemini - Ask me anything!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Search Bar Input
    st.markdown('<div class="search-container"><div class="search-wrapper">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask Dhairya AI...",
            placeholder="Type your message here...",
            label_visibility="collapsed",
            key="user_input"
        )
    
    with col2:
        send = st.button("➤", use_container_width=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Process Message
    if (send or user_input) and user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI Response
        try:
            # Create chat history for context
            chat = model.start_chat(history=[])
            
            # Send message
            response = chat.send_message(user_input)
            ai_response = response.text
            
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "❌ Invalid API key. Please get a new one from https://makersuite.google.com/app/apikey"
                })
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Sorry, I encountered an error: {error_msg}"
                })
        
        st.rerun()
    
    # Sidebar Settings
    with st.sidebar:
        st.markdown("""
        <div style="padding: 1rem;">
            <h3 style="color: white; font-family: 'Inter', sans-serif;">⚙️ Settings</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("🔑 Change API Key", use_container_width=True):
            st.session_state.api_saved = False
            st.session_state.api_key = ''
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        st.markdown(f"""
        <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem; padding: 1rem;">
            <p>💬 Messages: {len(st.session_state.messages)}</p>
            <p>🤖 Model: Gemini Pro</p>
            <p>🆓 Cost: FREE</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        <div style="color: rgba(255,255,255,0.4); font-size: 0.7rem; padding: 1rem;">
            <p>⚡ Powered by Google Gemini</p>
            <p>🎁 100% FREE API</p>
            <p>Made with ❤️ by Dhairya</p>
        </div>
        """, unsafe_allow_html=True)
