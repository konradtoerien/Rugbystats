import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Swartland 7s Stats", layout="centered")

# Donkerblou tema, Swartland-goud aksente en watermerk agtergrond
st.markdown("""
    <style>
    /* Donkerblou Hoof-agtergrond */
    .stApp {
        background-color: #0b132b !important;
        color: #ffffff !important;
    }
    
    /* Watermerk Logo Agtergrond */
    .stAppViewContainer::before {
        content: "";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 85vw;
        height: 85vw;
        max-width: 400px;
        max-height: 400px;
        background-image: url('https://raw.githubusercontent.com/konradtoerien/Rugby-S/main/211923.jpg');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        opacity: 0.12;
        pointer-events: none;
        z-index: 0;
    }

    /* Knoppie-stilerings (Kompak vir foon) */
    .stButton>button {
        width: 100%;
        height: 38px;
        font-size: 11px !important;
        font-weight: bold;
        border-radius: 6px;
        padding: 2px 2px;
        border: 1px solid #f4c430 !important;
        background-color: #1c2541 !important;
        color: #ffffff !important;
    }

    /* Aktiewe speler knoppie uitlig */
    div.stButton > button:first-child[aria-pressed="true"] {
        background-color: #f4c430 !important;
        color: #0b132b !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0.2rem;
    }

    /* Eksplisiete wit teks vir titels en spyskaarte */
    h1, h2, h3, h4, label, p {
        color: #f4c430 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inisialiseer Session States
if "events" not in st.session_state:
    st.session_state.events = []
if "score_us" not in st.session_state:
    st.session_state.score_us = 0
if "score_them" not in st.session_state:
    st.session_state.score_them = 0
if "active_player" not in st.session_state:
    st.session_state.active_player = "Span"

st.title("🏉 Swartland 7s Stats")

# Wedstryd Instellings
with st.expander("⚙️ Wedstryd Instellings & Name", expanded=False):
    col_m1, col_m2 = st.columns(2)
    wedstryd_nr = col_m1.text_input("Wedstryd #", value="Wedstryd 1")
    tekenaar = col_m2.text_input("Teenstander", value="Opponent")
    
    default_players = "Speler 1, Speler 2, Speler 3, Speler 4, Speler 5, Speler 6, Speler 7, Speler 8, Speler 9, Speler 10, Speler 11, Speler 12"
    raw_players = st.text_area("Spelername (geskei met 'n komma):", value=default_players)
    player_list = [p.strip() for p in raw_players.split(",") if p.strip()]

# Telbord
st.markdown(f"### 🏆 **Swartland: {st.session_state.score_us}** | **{tekenaar}: {st.session_state.score_them}**")

def log_event(kat, detail, speler, punte=0, vir_ons=True):
    t_min = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.events.append({
        "Wedstryd": wedstryd_nr,
        "Tyd": t_min,
        "Speler": speler,
        "Kategorie": kat,
        "Aksie": detail,
        "Punte": punte
    })
    
    if punte > 0:
        if vir_ons:
            st.session_state.score_us += punte
        else:
            st.session_state.score_them += punte
            
    st.toast(f"✅ {speler}: {detail}")

# 1. Speler Knoppies (3 Kollome)
st.markdown(f"#### 1. Kies Speler (Aktief: **{st.session_state.active_player}**)")

# 'Span' Knoppie
if st.button("📋 HELE SPAN / ALGEMEEN"):
    st.session_state.active_player = "Span"

# Verdeel spelers in 3 kollome
cols = st.columns(3)
for idx, p_name in enumerate(player_list):
    col_idx = idx % 3
    if cols[col_idx].button(f"🏃 {p_name}"):
        st.session_state.active_player = p_name

st.divider()

# 2. Aksie Knoppies (Super Kompak)
st.markdown("#### 2. Tik Aksie")

curr_p = st.session_state.active_player

# Punte Knoppies (4 Kollome)
p1, p2, p3, p4 = st.columns(4)
if p1.button("🏉 Drie (+5)"): log_event("Punte", "Drie Gedruk", curr_p, punte=5)
if p2.button("🎯 Verstell (+2)"): log_event("Punte", "Verstelling Gewen", curr_p, punte=2)
if p3.button("❌ Verstell Gemis"): log_event("Punte", "Verstelling Gemis", curr_p)
if p4.button("👟 Strafskop (+3)"): log_event("Punte", "Strafskop Gewen", curr_p, punte=3)

# Punte Teenstander & Drop Goal (3 Kollome)
p5, p6, p7 = st.columns(3)
if p5.button("🎯 Skepskop (+3)"): log_event("Punte", "Drop Goal", curr_p, punte=3)
if p6.button("🔴 Drie Teen (+5)"): log_event("Punte Teen", "Drie Teenstander", tekenaar, punte=5, vir_ons=False)
if p7.button("🔴 Verstell Teen (+2)"): log_event("Punte Teen", "Verstelling Teenstander", tekenaar, punte=2, vir_ons=False)

# Spelaksies (3 Kollome)
c1, c2, c3 = st.columns(3)
if c1.button("💥 Duikslag Gewen"): log_event("Verdediging", "Dominante Duikslag", curr_p)
if c2.button("⚠️ Duikslag Gemis"): log_event("Verdediging", "Gemiste Duikslag", curr_p)
if c3.button("⚡ Omkeer Gewen"): log_event("Afbreekpunt", "Turnover Gewen", curr_p)

c4, c5, c6 = st.columns(3)
if c4.button("❌ Aangeslaan"): log_event("Fout", "Aangeslaan", curr_p)
if c5.button("🟢 Lynstaan Gewen"): log_event("Set Piece", "Lynstaan Gewen", "Span")
if c6.button("🔴 Skrum Gewen"): log_event("Set Piece", "Skrum Gewen", "Span")

# Wedstryd Log & CSV
if st.session_state.events:
    df = pd.DataFrame(st.session_state.events)
    st.markdown("#### 📊 Wedstryd Log")
    st.dataframe(df.tail(3), use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Laai Stats Af (CSV)", csv, f"{wedstryd_nr}_stats.csv", "text/csv")
