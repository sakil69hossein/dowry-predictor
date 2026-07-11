import streamlit as st
import pandas as pd 
import joblib
import plotly.graph_objects as go
import time
st.set_page_config(page_title="Sakil Hossein AI Presence", page_icon="🤑", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #1a082c 0%, #050505 80%);
        color: #00e5ff;
        font-family: 'Courier New', Courier, monospace;
    }
    h1, h2, h3 { 
        color: #ff00ff !important; 
        text-shadow: 0 0 5px #ff00ff, 0 0 15px #ff00ff;
        text-align: center; 
        text-transform: uppercase; 
        letter-spacing: 3px;
    }
    p, label {
        color: #00e5ff !important; font-weight: bold; font-size: 1.2rem !important;
    }
    .metric-card {
        background: rgba(10, 10, 15, 0.7); border: 1px solid #00e5ff;
        box-shadow: 0 0 15px #00e5ff, inset 0 0 10px #00e5ff;
        padding: 30px; border-radius: 12px; text-align: center; 
        margin-top: 20px; backdrop-filter: blur(10px);
    }
    .stButton>button {
        background-color: transparent !important; color: #ff00ff !important;
        border: 2px solid #ff00ff !important; box-shadow: 0 0 10px #ff00ff, inset 0 0 5px #ff00ff !important;
        border-radius: 8px; height: 3.5em; width: 100%; 
        transition: all 0.3s ease-in-out; font-weight: bold; font-size: 1.2rem !important; letter-spacing: 2px;
    }
    .stButton>button:hover {
        background-color: #ff00ff !important; color: #000000 !important;
        box-shadow: 0 0 25px #ff00ff, 0 0 50px #ff00ff !important;
    }
    div.row-widget.stRadio > div { flex-direction: row; align-items: center; justify-content: center; gap: 20px;}
    </style>
""", unsafe_allow_html=True)
@st.cache_resource
def load_assets():
    model = joblib.load("Dowry.pkl")
    scaler = joblib.load("Scaler.pkl")
    expected_columns = joblib.load("columns.pkl")
    return model, scaler, expected_columns

model, scaler, expected_columns = load_assets()
if 'step' not in st.session_state:
    st.session_state.step = 1

defaults = {
    'g_age':28,'b_age':20,
    'g_inc': 8.0, 'g_edu': 'Graduate', 'g_sec': 'Private',
    'b_inc': 4.0, 'b_edu': 'Graduate', 'f_wealth': 25.0, 
    'land': 2.0, 'locale': 'Urban'
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1
st.markdown("<h1>❤️ DOWRY PREDICTOR ❤️</h1>", unsafe_allow_html=True)
st.progress(st.session_state.step / 4) 
st.write("---")

edu_options = ["School", "Graduate", "Postgraduate", "PhD"]
if st.session_state.step == 1:
    st.markdown("### STEP 1: GROOM PARAMETERS")
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    
    st.session_state.g_age = st.slider("Groom Age ", 18, 100.0, st.session_state.g_inc, 0.5)
    st.write("<br>", unsafe_allow_html=True)
    st.session_state.g_inc = st.slider("Groom Income (LPA)", 0.0, 100.0, st.session_state.g_inc, 0.5)
    st.write("<br>", unsafe_allow_html=True)
    st.session_state.g_edu = st.selectbox(
        "Groom Education Level", 
        edu_options, 
        index=edu_options.index(st.session_state.g_edu)
    )
    st.write("<br>", unsafe_allow_html=True)
    
    st.session_state.g_sec = st.radio("Employment Sector", ["Private", "Government", "Business"], horizontal=True, index=["Private", "Government", "Business"].index(st.session_state.g_sec))
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    st.button("NEXT ⏩", on_click=next_step, key="next1")
elif st.session_state.step == 2:
    st.markdown("### STEP 2: BRIDE PARAMETERS")
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    
    st.session_state.b_age = st.slider("Bride Age ", 18, 100.0, st.session_state.b_inc, 0.5)
    st.write("<br>", unsafe_allow_html=True)
    st.session_state.b_inc = st.slider("Bride Income (LPA)", 0.0, 100.0, st.session_state.b_inc, 0.5)
    st.write("<br>", unsafe_allow_html=True)
    st.session_state.b_edu = st.selectbox(
        "Bride Education Level", 
        edu_options, 
        index=edu_options.index(st.session_state.b_edu)
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: st.button("⏪ BACK", on_click=prev_step, key="back2")
    with col2: st.button("NEXT ⏩", on_click=next_step, key="next2")
elif st.session_state.step == 3:
    st.markdown("### STEP 3: ASSETS & LOCALE")
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    
    st.session_state.f_wealth = st.slider("Family Net Worth (Lakhs)", 0.0, 500.0, st.session_state.f_wealth, 1.0)
    st.write("<br>", unsafe_allow_html=True)
    st.session_state.land = st.slider("Agricultural Land (Acres)", 0.0, 100.0, st.session_state.land, 0.1)
    st.write("<br>", unsafe_allow_html=True)
    st.session_state.locale = st.radio("Geographic Locale", ["Urban", "Rural"], horizontal=True, index=["Urban", "Rural"].index(st.session_state.locale))
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: st.button("⏪ BACK", on_click=prev_step, key="back3")
    with col2: st.button("EXECUTE ⚡", on_click=next_step, key="next3")
elif st.session_state.step == 4:
    with st.spinner('⚡ BYPASSING FIREWALL... COMPILING TENSORS ⚡'):
        time.sleep(1.5) 
        
        try:
            raw_input = {
                "Groom_Income_LPA": st.session_state.g_inc,
                "Bride_Income_LPA": st.session_state.b_inc,
                "Family_Asset_NetWorth_Lakhs": st.session_state.f_wealth,
                "Groom_Family_Land_Acres": st.session_state.land,
                "Groom_Education_" + st.session_state.g_edu: 1,
                "Bride_Education_" + st.session_state.b_edu: 1,
                "Groom_Employment_Sector_" + st.session_state.g_sec: 1,
                "Urban_Rural_" + st.session_state.locale: 1
            }
            
            input_df = pd.DataFrame([raw_input])
            for col in expected_columns:
                if col not in input_df.columns:
                    input_df[col] = 0

            input_df = input_df[expected_columns]
            scaled_input = scaler.transform(input_df)
            prediction = max(0, model.predict(scaled_input)[0])
            
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style='margin:0; color:#ff00ff; text-shadow: none;'>FINAL OUTPUT</h3>
                    <h1 style='margin:0;'>₹ {prediction:,.2f}</h1>
                    <p style='color:#00e5ff; margin-top: 5px;'>[ LAKHS ]</p>
                </div>
            """, unsafe_allow_html=True)
            
            max_gauge_value = max(100, prediction * 1.5) 
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = prediction,
                number = {'prefix': "₹ ", 'suffix': " L", 'font': {'color': '#00e5ff'}},
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, max_gauge_value], 'tickwidth': 2, 'tickcolor': "#ff00ff"},
                    'bar': {'color': "#00e5ff", 'thickness': 0.75}, 
                    'bgcolor': "rgba(0,0,0,0)", 'borderwidth': 2, 'bordercolor': "#ff00ff", 
                    'steps': [
                        {'range': [0, max_gauge_value*0.33], 'color': 'rgba(255, 0, 255, 0.1)'},
                        {'range': [max_gauge_value*0.33, max_gauge_value*0.66], 'color': 'rgba(255, 0, 255, 0.25)'},
                        {'range': [max_gauge_value*0.66, max_gauge_value], 'color': 'rgba(255, 0, 255, 0.4)'}],
                }
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "#00e5ff"}, height=350, margin=dict(t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"SYSTEM FAILURE: {e}")
            
    st.button("🔄 RESTART SEQUENCE", on_click=lambda: st.session_state.update(step=1))
