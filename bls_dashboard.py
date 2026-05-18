import streamlit as st

st.set_page_config(layout="wide", page_title="Brand Lift Power Tool")

# --- Sidebar: Global Controls ---
st.sidebar.header("Global Assumptions")
num_arms = st.sidebar.number_input("Number of Test Arms", min_value=2, max_value=4, value=3)
duration = st.sidebar.slider("Study Duration (Weeks)", 1, 26, 8)
geo_holdout = st.sidebar.slider("Geo Holdout %", 0.0, 0.5, 0.28)
olv_cpm = st.sidebar.number_input("OLV CPM ($)", value=12.50)
cpr = st.sidebar.number_input("Cost Per Response ($)", value=12.50)

st.sidebar.divider()
mde_target = st.sidebar.select_slider("Target MDE (%)", options=[0.5, 1.0, 1.5, 2.0, 4.0], value=2.0)

# --- Calculation Logic ---
mde_base_map = {4.0: 2000, 2.0: 7500, 1.5: 19000, 1.0: 42000, 0.5: 165000}
base_responses = mde_base_map[mde_target]

def calculate_metrics(num_questions):
    # Variance multiplier: Awareness requires 2.5x more data than Consideration
    multiplier = 1.0 if num_questions == 1 else 2.5
    needed_per_arm = base_responses * multiplier
    total_needed = needed_per_arm * num_arms
    
    # Budget Logic
    raw_budget = total_needed * cpr
    final_budget = raw_budget / (1 - geo_holdout)
    weekly_burn = final_budget / duration
    
    return total_needed, final_budget, weekly_burn

# --- Dashboard Header ---
st.title("📊 Google Brand Lift Strategy Dashboard")
st.write(f"Parameters: **{num_arms} Arms** | **{duration} Weeks** | **{int(geo_holdout*100)}% Holdout** | **{mde_target}% MDE**")

# --- Scenario Cards ---
scenarios =[
    ("Scenario A: 1-Question", 1, "Focus: Consideration (12% Base)"),
    ("Scenario B: 2-Questions", 2, "Focus: Awareness (45% Base)"),
    ("Scenario C: 3-Questions", 3, "Focus: Awareness (45% Base)")
]

cols = st.columns(3)
for i, (title, num_q, desc) in enumerate(scenarios):
    total_resp, total_budget, weekly_burn = calculate_metrics(num_q)
    
    with cols[i]:
        st.subheader(title)
        st.caption(desc)
        
        # Big Numbers
        st.metric("Total Responses", f"{int(total_resp):,}")
        st.metric("Total Budget", f"${int(total_budget):,}")
        st.metric("Weekly Burn Rate", f"${int(weekly_burn):,}")
        
        # Viability Logic
        if total_budget > 3000000:
            st.error("Viability: Prohibitively Expensive")
        elif total_budget > 1000000:
            st.warning("Viability: High Investment")
        else:
            st.success("Viability: Recommended")