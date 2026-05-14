import streamlit as st
import time
import random
from supabase import create_client, Client

# --- SETUP SUPABASE ---
URL = "https://hhmjznocxlboozfpipcc.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhobWp6bm9jeGxib296ZnBpcGNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg3NzAxNzksImV4cCI6MjA5NDM0NjE3OX0.j51ZFITdtGX2_fuUGw1HhS57vtkEDx0EFkC29a3y8AA"
supabase: Client = create_client(URL, KEY)

# --- PAGE CONFIG ---
st.set_page_config(page_title="The Kondowe Dilemma", layout="wide", initial_sidebar_state="collapsed")

# --- UI STYLING (PREMIUM DARK GREEN THEME) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container {padding: 0px !important;}
    .stApp { background: #061a06; color: white; }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 2rem;
        padding: 2.5rem;
    }
    
    .reward-box {
        background: rgba(234, 179, 8, 0.1);
        border: 1px dashed #eab308;
        border-radius: 1.2rem;
        padding: 20px;
        margin: 15px 0;
        text-align: center;
    }

    .reward-item {
        display: inline-block;
        margin: 0 15px;
    }

    .reward-value {
        font-size: 1.5rem;
        font-weight: 900;
        color: #eab308;
    }

    .gradient-text {
        background: linear-gradient(135deg, #eab308 0%, #22c55e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: center;
    }
    
    div.stButton > button {
        width: 100%; border-radius: 1.2rem; height: 3.8rem; font-weight: 800;
        text-transform: uppercase; letter-spacing: 1.5px; transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.2); color: white;
    }
    
    /* Play Buttons Color Coding */
    div[data-testid="stHorizontalBlock"] div:nth-child(1) button { border: 2px solid #22c55e !important; color: #22c55e !important; background: rgba(34,197,94,0.1) !important; }
    div[data-testid="stHorizontalBlock"] div:nth-child(2) button { border: 2px solid #ef4444 !important; color: #ef4444 !important; background: rgba(239,68,68,0.1) !important; }
    
    .timer-display { font-size: 3.5rem; font-weight: 900; color: #eab308; text-align: center; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION INITIALIZATION ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"USER_{random.randint(1000, 9999)}"
    st.session_state.room_id = None
    st.session_state.role = None
    st.session_state.search_start = None

# --- MATCHMAKING LOGIC ---
def find_match(stake):
    # 1. Jaribu kujiunga na chumba kilichopo tayari
    res = supabase.table("rooms").select("*").eq("stake", stake).eq("status", "waiting").execute()
    rooms = res.data
    
    if rooms:
        room = rooms[0]
        if room['p1_id'] != st.session_state.user_id:
            supabase.table("rooms").update({
                "status": "playing", 
                "p2_id": st.session_state.user_id
            }).eq("room_id", room['room_id']).execute()
            return room['room_id'], "P2"
    
    # 2. Kama hakuna, tengeneza room mpya (Tumeshughulikia 'room_id' hapa)
    r_id = random.randint(100000, 999999) # Hii inazuia not-null constraint error
    try:
        new_room = supabase.table("rooms").insert({
            "room_id": r_id,
            "stake": stake, 
            "p1_id": st.session_state.user_id, 
            "status": "waiting", 
            "current_level": 1
        }).execute()
        return new_room.data[0]['room_id'], "P1"
    except Exception as e:
        st.error(f"Hitilafu ya Database: {e}")
        return None, None

# --- UI CONTENT ---
st.markdown('<h1 class="gradient-text" style="font-size: 3.5rem; margin-top: 2rem;">KONDOWE DILEMMA</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#6b7280; font-weight:bold; letter-spacing:3px; margin-bottom:2rem;">TRUST NO ONE. COLLECT THE REWARD.</p>', unsafe_allow_html=True)

_, col_main, _ = st.columns([1, 2, 1])

with col_main:
    # --- STAGE 1: LOBBY & REWARDS ---
    if st.session_state.room_id is None:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center; font-weight:900;'>CHAGUA DAU LAKO</h3>", unsafe_allow_html=True)
        
        dau = st.selectbox("KIASI (TSh):", [2000, 5000, 10000, 50000], label_visibility="collapsed")
        
        # Reward Calculations
        coop_win = int(dau * 1.5)
        betray_win = int(dau * 1.8)
        
        st.markdown(f"""
            <div class="reward-box">
                <div class="reward-item">
                    <small style="color:#22c55e; font-weight:bold;">COOPERATE REWARD</small><br>
                    <span class="reward-value">TSh {coop_win:,}</span>
                </div>
                <div class="reward-item">
                    <small style="color:#ef4444; font-weight:bold;">BETRAYAL REWARD</small><br>
                    <span class="reward-value">TSh {betray_win:,}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("TAFUTA MPINZANI SASA"):
            r_id, role = find_match(dau)
            if r_id:
                st.session_state.room_id = r_id
                st.session_state.role = role
                st.session_state.search_start = time.time()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- STAGE 2: WAITING / MATCHMAKING ---
    else:
        try:
            # Pata data ya chumba kwa wakati halisi
            room_res = supabase.table("rooms").select("*").eq("room_id", st.session_state.room_id).single().execute()
            room = room_res.data
            
            if not room:
                st.session_state.room_id = None
                st.rerun()

            if room['status'] == 'waiting':
                elapsed = time.time() - st.session_state.search_start
                remaining = int(30 - elapsed)
                
                if remaining <= 0:
                    # Muda umeisha: Futa chumba na rudisha lobby
                    supabase.table("rooms").delete().eq("room_id", st.session_state.room_id).execute()
                    st.session_state.room_id = None
                    st.error("OPPONENT WAS NOT FOUND! Jaribu tena baadaye.")
                    time.sleep(3)
                    st.rerun()
                else:
                    st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
                    st.markdown(f'<div class="timer-display">{remaining}</div>', unsafe_allow_html=True)
                    st.warning(f"Inatafuta mpinzani mwenye dau la {room['stake']:,}...")
                    st.progress(elapsed / 30)
                    
                    if st.button("SITISHA UTAFUTAJI"):
                        supabase.table("rooms").delete().eq("room_id", st.session_state.room_id).execute()
                        st.session_state.room_id = None
                        st.rerun()
                    
                    time.sleep(1)
                    st.rerun()

            # --- STAGE 3: GAMEPLAY ---
            elif room['status'] == 'playing':
                lvl = room['current_level']
                st.markdown(f"<div style='font-weight:900; color:#eab308;'>LEVEL {lvl}/10</div>", unsafe_allow_html=True)
                st.progress(lvl / 10)
                
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                role = st.session_state.role
                my_choice = room['p1_choice'] if role == "P1" else room['p2_choice']
                opp_choice = room['p2_choice'] if role == "P1" else room['p1_choice']

                if not my_choice:
                    st.markdown("<h3 style='text-align:center; font-weight:900;'>UAMUZI WAKO?</h3>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    if c1.button("🤝 COOPERATE"):
                        f = "p1_choice" if role == "P1" else "p2_choice"
                        supabase.table("rooms").update({f: "cooperate"}).eq("room_id", room['room_id']).execute()
                        st.rerun()
                    if c2.button("🗡️ BETRAY"):
                        f = "p1_choice" if role == "P1" else "p2_choice"
                        supabase.table("rooms").update({f: "betray"}).eq("room_id", room['room_id']).execute()
                        st.rerun()
                else:
                    if not opp_choice:
                        st.info("Uamuzi wako umetumwa. Mpinzani bado anafikiri...")
                        time.sleep(2)
                        st.rerun()
                    else:
                        # Hapa ndipo logic ya ku-compare inakaa
                        c1, c2 = room['p1_choice'], room['p2_choice']
                        if c1 == "cooperate" and c2 == "cooperate":
                            st.success("WOTE MMESHIRIKIANA! Songa Level Inayofuata.")
                            if role == "P1":
                                time.sleep(2)
                                if lvl < 10:
                                    supabase.table("rooms").update({"current_level": lvl+1, "p1_choice": None, "p2_choice": None}).eq("room_id", room['room_id']).execute()
                                else:
                                    supabase.table("rooms").update({"status": "finished"}).eq("room_id", room['room_id']).execute()
                            st.rerun()
                        # Hapa unaweza kuongeza masharti ya ushindi/kupoteza zaidi...
                st.markdown('</div>', unsafe_allow_html=True)

            elif room['status'] == 'finished':
                st.balloons()
                st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
                st.header("GAME OVER")
                if st.button("RUDI NYUMBANI"):
                    st.session_state.room_id = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.session_state.room_id = None
            st.rerun()

# --- FOOTER ---
st.markdown('<div style="text-align:center; padding:30px; color:#4b5563; font-size:10px; font-weight:bold; letter-spacing:2px;">KONDOWE EDUCATION LABS &copy; 2026</div>', unsafe_allow_html=True)