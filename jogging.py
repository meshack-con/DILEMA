import streamlit as st
from supabase import create_client, Client

# =====================================================
# SUPABASE SETUP
# =====================================================
URL = "https://hhmjznocxlboozfpipcc.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhobWp6bm9jeGxib296ZnBpcGNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg3NzAxNzksImV4cCI6MjA5NDM0NjE3OX0.j51ZFITdtGX2_fuUGw1HhS57vtkEDx0EFkC29a3y8AA"

supabase: Client = create_client(URL, KEY)

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="ACM JOGGING",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# CSS STYLING (UPDATED BUTTON TO GREEN WITH WHITE TEXT)
# =====================================================
st.markdown("""
<style>
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 2rem !important;
        max-width: 1200px;
    }

    /* Base App Style */
    .stApp {
        background: #041204;
        color: #ffffff;
    }

    /* LABELS COLOR: GREEN */
    .stWidgetLabel p {
        color: #22c55e !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        margin-bottom: 8px !important;
    }

    /* INPUT FIELDS: BLACK BACKGROUND */
    .stTextInput input {
        background-color: #000000 !important;
        border: 1px solid #22c55e !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }

    /* BUTTON: GREEN BACKGROUND & WHITE TEXT (UPDATED) */
    div.stButton > button {
        width: 100% !important;
        border-radius: 12px !important;
        height: 3.5rem !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        background-color: #22c55e !important; /* Green background */
        color: #ffffff !important; /* White text */
        border: none !important;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4) !important;
        transition: 0.3s all ease-in-out !important;
        margin-top: 15px !important;
    }

    div.stButton > button:hover {
        background-color: #16a34a !important; /* Darker green on hover */
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.6) !important;
    }

    /* Glass Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        padding: 2rem;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Title Gradient */
    .gradient-text {
        background: linear-gradient(135deg, #fbbf24 0%, #22c55e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: center;
    }

    /* Participant Cards */
    .participant-item {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #fbbf24;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER SECTION
# =====================================================
st.markdown("""
<h1 class="gradient-text" style="font-size:4rem; margin-bottom:0;">ACM JOGGING</h1>
<p style="text-align:center; color:#22c55e; font-weight:700; letter-spacing:3px; margin-bottom:30px;">
    HEALTH • FITNESS • COMMUNITY
</p>
""", unsafe_allow_html=True)

# =====================================================
# EVENT DETAILS (DATE: 16 MAY 2026)
# =====================================================
st.markdown("""
<div class="glass-card" style="text-align:center; border-bottom: 4px solid #22c55e;">
    <h2 style="color:white; margin-bottom:15px;">JUMAMOSI YA KESHO</h2>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <span style="font-size: 20px; color: #fbbf24; font-weight: bold;">📅 16 MAY 2026</span>
        <span style="font-size: 20px; color: #fbbf24; font-weight: bold;">⏰ 06:00 AM</span>
        <span style="font-size: 20px; color: #fbbf24; font-weight: bold;">📍 BLOCK 5</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# MAIN CONTENT
# =====================================================
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#22c55e; text-align:center; margin-bottom:20px;">USAJILI</h2>', unsafe_allow_html=True)
    
    with st.form("jogging_form", clear_on_submit=True):
        name = st.text_input("Jina Kamili (Full Name)")
        phone = st.text_input("Namba ya Simu (Phone)")
        room = st.text_input("Namba ya Chumba (Room No)")
        
        submitted = st.form_submit_button("JISAJILI SASA")
        
        if submitted:
            if name and phone and room:
                try:
                    supabase.table("participants").insert({
                        "name": name, 
                        "phone": phone, 
                        "room": room
                    }).execute()
                    st.success(f"Hongera {name}! Usajili umekamilika. ✅")
                    st.rerun()
                except Exception as e:
                    st.error("Kuna tatizo limetokea.")
            else:
                st.warning("Tafadhali jaza nafasi zote!")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#fbbf24; text-align:center; margin-bottom:20px;">WASHIRIKI</h2>', unsafe_allow_html=True)
    
    try:
        res = supabase.table("participants").select("*").order("id", desc=True).execute()
        data = res.data
        
        if data:
            st.markdown(f"<p style='text-align:center; color:#aaa;'>Jumla ya waliojisajili: <b>{len(data)}</b></p>", unsafe_allow_html=True)
            for person in data:
                st.markdown(f"""
                <div class="participant-item">
                    <div style="font-weight:bold; color:#22c55e; font-size:1.1rem;">👤 {person['name']}</div>
                    <div style="font-size:0.9rem; color:#ccc;">🏠 Room: {person['room']} | 📞 {person['phone']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Bado hakuna washiriki waliojisajili.")
    except:
        st.error("Tatizo la kiufundi katika kuleta orodha.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================
st.markdown("""
<br><br>
<div style="text-align:center; color:#4b5563; font-size:12px; letter-spacing:2px;">
    POWERED BY ACM COMMUNITY © 2026
</div>
""", unsafe_allow_html=True)