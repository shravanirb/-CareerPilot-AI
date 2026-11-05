import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
from pathlib import Path

from recommendations import get_required_skills, get_career_roadmap, get_career_description
from ai_career_assistant import generate_career_guidance

# ==================================================
# PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="CareerPilot AI — Career Prediction System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# GLOBAL CSS
# ==================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    .main .block-container { padding-top: 1.5rem; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%); }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    section[data-testid="stSidebar"] .stRadio label:hover { color: #38bdf8 !important; }
    
    /* Hero card */
    .hero-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 50%, #312e81 100%);
        border-radius: 16px;
        padding: 40px 30px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(15, 23, 42, 0.3);
    }
    .hero-card h1 { color: #ffffff; font-weight: 800; font-size: 2.4rem; margin: 0 0 8px 0; }
    .hero-card p { color: #94a3b8; font-size: 1.1rem; margin: 0; }
    
    /* Section headers */
    .section-header {
        color: #1e293b;
        font-weight: 700;
        font-size: 1.4rem;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 8px;
        margin: 25px 0 15px 0;
        display: inline-block;
    }
    
    /* Result card */
    .result-hero {
        background: linear-gradient(135deg, #1e3a5f 0%, #312e81 100%);
        border-radius: 16px;
        padding: 35px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(15, 23, 42, 0.25);
        margin-bottom: 20px;
    }
    .result-hero .label { color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px; }
    .result-hero .career { color: #ffffff; font-size: 2.4rem; font-weight: 800; margin: 10px 0; }
    .result-hero .sub { color: #cbd5e1; font-size: 0.95rem; }
    
    /* Metric card */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .metric-card .value { font-size: 2rem; font-weight: 800; color: #1e3a8a; margin: 5px 0; }
    .metric-card .label { font-size: 0.85rem; color: #64748b; }
    
    /* Career match card */
    .match-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 8px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        transition: transform 0.15s;
    }
    .match-card:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .match-card.top { border-left: 4px solid #10b981; background: #f0fdf4; }
    .match-row { display: flex; justify-content: space-between; align-items: center; }
    .match-rank { color: #3b82f6; font-weight: 700; font-size: 0.85rem; min-width: 28px; }
    .match-name { font-weight: 600; color: #1e293b; flex: 1; margin: 0 12px; }
    .match-pct { color: #3b82f6; font-weight: 700; font-size: 0.95rem; }
    
    /* Roadmap */
    .roadmap-step {
        display: flex;
        align-items: flex-start;
        margin-bottom: 0;
    }
    .roadmap-line {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-right: 16px;
        min-width: 36px;
    }
    .roadmap-dot {
        width: 36px; height: 36px;
        border-radius: 50%;
        background: #3b82f6;
        color: white;
        font-weight: 700;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(59,130,246,0.3);
    }
    .roadmap-connector {
        width: 2px;
        height: 28px;
        background: #cbd5e1;
    }
    .roadmap-content {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 10px 16px;
        flex: 1;
        margin-bottom: 8px;
    }
    .roadmap-content p { margin: 0; font-weight: 500; color: #334155; font-size: 0.95rem; }
    
    /* Readiness gauge */
    .readiness-big {
        text-align: center;
        padding: 30px 20px;
    }
    .readiness-big .score { font-size: 4rem; font-weight: 800; margin: 0; line-height: 1; }
    .readiness-big .out-of { font-size: 1.2rem; color: #94a3b8; font-weight: 500; }
    .readiness-big .level { font-size: 1.1rem; font-weight: 600; margin-top: 10px; }
    
    /* Priority badges */
    .badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
    .badge-high { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
    .badge-medium { background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }
    .badge-low { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
    
    /* Scale legend */
    .scale-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f1f5f9; font-size: 0.85rem; }
    .scale-range { font-weight: 600; color: #1e293b; }
    .scale-label { color: #64748b; }
    
    /* Insight card */
    .insight-box {
        background: linear-gradient(135deg, #eff6ff 0%, #f5f3ff 100%);
        border: 1px solid #c7d2fe;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    .insight-box p { margin: 0; color: #334155; font-size: 0.95rem; line-height: 1.6; }
    
    /* Next step card */
    .nextstep-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #312e81 100%);
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
    }
    .nextstep-box h4 { color: #f8fafc; margin: 0 0 10px 0; }
    .nextstep-box p { color: #cbd5e1; margin: 0; line-height: 1.6; }
    
    /* Hide default streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ==================================================
# LOAD TRAINED MODEL & DATA
# ==================================================
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "career_model.pkl"
DATA_PATH = BASE_DIR / "data" / "student_career_success_dataset.csv"


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_dataset():
    return pd.read_csv(DATA_PATH)


model = load_model()
df = load_dataset()


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================
with st.sidebar:
    st.markdown("## 🚀 CareerPilot AI")
    st.caption("Student Career Prediction System")
    st.divider()
    page = st.radio(
        "Navigation",
        ["🏠 Overview", "🎯 Career Predictor", "📊 Model Analytics", "💡 Career Insights"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("Powered by Random Forest ML Model")
    st.caption(f"Dataset: {len(df):,} student records")
    st.caption(f"Career Categories: {len(model.classes_)}")


# ==================================================
# HELPER FUNCTIONS
# ==================================================
def calculate_readiness_score(cgpa, prog, proj, intern, comm, resume, interview, employ):
    """Calculates a transparent placement readiness score out of 100."""
    cgpa_norm = (cgpa / 10.0) * 100
    prog_norm = (prog / 10.0) * 100
    proj_norm = min((proj / 5.0) * 100, 100)
    intern_norm = min((intern / 3.0) * 100, 100)
    comm_norm = (comm / 10.0) * 100
    score = (
        cgpa_norm * 0.10 + prog_norm * 0.15 + proj_norm * 0.15 +
        intern_norm * 0.10 + comm_norm * 0.10 + resume * 0.15 +
        interview * 0.15 + employ * 0.10
    )
    return round(min(max(score, 0), 100), 1)


def get_readiness_level(score):
    if score >= 80: return "Excellent Readiness", "#10b981"
    elif score >= 60: return "Good Progress", "#3b82f6"
    elif score >= 40: return "Developing", "#f59e0b"
    else: return "Needs Improvement", "#ef4444"


# =====================================================================
# PAGE: OVERVIEW
# =====================================================================
if page == "🏠 Overview":
    st.markdown("""
    <div class="hero-card">
        <h1>🚀 CareerPilot AI</h1>
        <p>Discover Your Career Potential — Powered by Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "CareerPilot AI is an intelligent career guidance system that uses a trained "
        "**Random Forest machine learning model** to predict suitable career paths for students "
        "based on their academic performance, technical skills, and professional profile."
    )

    st.divider()

    # Dataset Statistics
    st.markdown('<div class="section-header">📈 Dataset Overview</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Records", f"{len(df):,}")
    m2.metric("Features", f"{len(model.feature_names_in_)}")
    m3.metric("Career Categories", f"{len(model.classes_)}")
    m4.metric("Model Type", "Random Forest")

    # Career Distribution
    st.markdown('<div class="section-header">🎯 Career Category Distribution</div>', unsafe_allow_html=True)

    career_counts = df["Career_Field"].value_counts().reset_index()
    career_counts.columns = ["Career", "Count"]
    # Exclude "Not Placed" from chart for cleaner view
    career_counts_filtered = career_counts[career_counts["Career"] != "Not Placed"]

    fig_dist = px.bar(
        career_counts_filtered.sort_values("Count", ascending=True),
        x="Count", y="Career", orientation="h",
        color="Count",
        color_continuous_scale=["#c7d2fe", "#3b82f6", "#1e3a8a"],
    )
    fig_dist.update_layout(
        height=500, showlegend=False, coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Number of Students", gridcolor="#f1f5f9"),
        yaxis=dict(title=""),
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Inter")
    )
    st.plotly_chart(fig_dist, use_container_width=True)

    # Model Info
    st.markdown('<div class="section-header">🤖 Model Information</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Model Pipeline**")
        st.markdown("- **Preprocessor:** ColumnTransformer (StandardScaler + OneHotEncoder)")
        st.markdown("- **Classifier:** Random Forest (200 estimators)")
        st.markdown(f"- **Input Features:** {len(model.feature_names_in_)}")
        st.markdown(f"- **Output Classes:** {len(model.classes_)}")
    with col_b:
        st.markdown("**Career Categories Predicted**")
        for c in sorted(model.classes_):
            st.markdown(f"• {c}")


# =====================================================================
# PAGE: CAREER PREDICTOR
# =====================================================================
elif page == "🎯 Career Predictor":
    st.markdown("""
    <div class="hero-card">
        <h1>🎯 Discover Your Career Potential</h1>
        <p>Fill in your profile below and let our AI model recommend the best career path for you.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- INPUT FORM ---
    st.markdown('<div class="section-header">👨‍🎓 Student Profile</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=17, max_value=40, value=21)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    with col2:
        university_year = st.selectbox("University Year", ["Freshman", "Sophomore", "Junior", "Senior"])
        major = st.selectbox("Major", [
            "Computer Science", "Information Technology", "Software Engineering",
            "Artificial Intelligence", "Business Analytics", "Data Science",
            "Cybersecurity", "Electrical Engineering"
        ])
    with col3:
        attendance = st.number_input("Attendance %", min_value=0, max_value=100, value=85)
        study_hours = st.number_input("Study Hours / Week", min_value=0, max_value=100, value=25)

    st.markdown('<div class="section-header">💻 Technical Skills</div>', unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    with col4:
        cgpa = st.number_input("CGPA (0-10)", min_value=0.0, max_value=10.0, value=8.5, step=0.1)
        academic_performance = st.selectbox("Academic Performance", ["Excellent", "Good", "Average", "Poor"])
    with col5:
        programming_skill = st.slider("Programming Skill", 0, 10, 8)
        projects = st.number_input("Projects Completed", min_value=0, max_value=50, value=4)
    with col6:
        certifications = st.number_input("Certifications", min_value=0, max_value=30, value=2)
        hackathons = st.number_input("Hackathons Attended", min_value=0, max_value=30, value=2)

    st.markdown('<div class="section-header">💼 Professional Profile</div>', unsafe_allow_html=True)
    col7, col8, col9 = st.columns(3)
    with col7:
        github = st.selectbox("GitHub Profile", ["Yes", "No"])
        linkedin = st.selectbox("LinkedIn Profile", ["Yes", "No"])
    with col8:
        internships = st.number_input("Internships", min_value=0, max_value=20, value=1)
        leadership = st.selectbox("Leadership Experience", ["Yes", "No"])
    with col9:
        resume_score = st.slider("Resume Score", 0, 100, 80)
        english = st.selectbox("English Proficiency", ["Advanced", "Intermediate", "Basic"])

    st.markdown('<div class="section-header">📊 Interview & Employability</div>', unsafe_allow_html=True)
    col10, col11, col12 = st.columns(3)
    with col10:
        communication = st.slider("Communication Skills", 0, 10, 8)
        teamwork = st.slider("Teamwork", 0, 10, 8)
    with col11:
        problem_solving = st.slider("Problem Solving", 0, 10, 9)
        interview_score = st.slider("Interview Score", 0, 100, 80)
    with col12:
        employability_score = st.slider("Employability Score", 0, 100, 85)

    st.write("")
    predict_btn = st.button("🚀 Predict My Career", type="primary", use_container_width=True)

    # =============================================
    # PREDICTION FLOW
    # =============================================
    if predict_btn:
      st.session_state["show_prediction_results"] = True
      st.session_state.pop("ollama_guidance", None)
      st.session_state.pop("ollama_guidance_error", None)

    if predict_btn or st.session_state.get("show_prediction_results", False):

        # Build input DataFrame with exact feature names the pipeline expects
        student_data = pd.DataFrame([{
            "Age": age,
            "Gender": gender,
            "University_Year": university_year,
            "Major": major,
            "Attendance_Percentage": attendance,
            "Study_Hours_Per_Week": study_hours,
            "CGPA": cgpa,
            "Academic_Performance": academic_performance,
            "Programming_Skill": programming_skill,
            "Projects_Completed": projects,
            "Certifications": certifications,
            "Hackathons": hackathons,
            "GitHub_Profile": github,
            "Internships": internships,
            "Leadership_Experience": leadership,
            "LinkedIn_Profile": linkedin,
            "Resume_Score": resume_score,
            "Communication_Skills": communication,
            "Teamwork": teamwork,
            "Problem_Solving": problem_solving,
            "English_Proficiency": english,
            "Interview_Score": interview_score,
            "Employability_Score": employability_score
        }])

        # --- Run prediction ---
        prediction = model.predict(student_data)
        predicted_career = prediction[0]

        probabilities = model.predict_proba(student_data)[0]
        classes = model.classes_

        probability_df = pd.DataFrame({
            "Career": classes,
            "Probability": probabilities
        }).sort_values(by="Probability", ascending=False)

        top_probability = probability_df.iloc[0]["Probability"]

        st.divider()

        # =============================================
        # 1. HERO RESULT — Recommended Career
        # =============================================
        st.markdown(f"""
        <div class="result-hero">
            <div class="label">🎯 Your Recommended Career</div>
            <div class="career">{predicted_career}</div>
            <div class="sub">Based on your academic, technical and professional profile</div>
        </div>
        """, unsafe_allow_html=True)

        # =============================================
        # 2. MODEL CONFIDENCE & CAREER INSIGHT
        # =============================================
        conf_col1, conf_col2 = st.columns([1, 2])

        with conf_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Model Confidence</div>
                <div class="value">{top_probability * 100:.1f}%</div>
                <div class="label">Probability assigned to this career</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("⚠️ Model confidence represents how strongly the model associates your profile "
                       "with this career. It is not a probability of getting a job.")

        with conf_col2:
            career_desc = get_career_description(predicted_career)
            st.markdown(f"""
            <div class="insight-box">
                <p><strong>💡 Career Insight — {predicted_career}</strong></p>
                <p>{career_desc}</p>
                <p style="margin-top:10px;">Your profile shows a strong combination of
                {'programming ability' if programming_skill >= 7 else 'academic focus'},
                {'hands-on project experience' if projects >= 3 else 'foundational knowledge'},
                and {'strong problem-solving skills' if problem_solving >= 7 else 'good communication skills'}
                — aligning well with this career path.</p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # =============================================
        # 3. TOP 5 CAREER MATCHES
        # =============================================
        st.markdown('<div class="section-header">🔎 Top Career Predictions</div>', unsafe_allow_html=True)

        top5 = probability_df.head(5)
        for rank, (_, row) in enumerate(top5.iterrows(), 1):
            pct = row["Probability"] * 100
            card_cls = "match-card top" if rank == 1 else "match-card"
            st.markdown(f"""
            <div class="{card_cls}">
                <div class="match-row">
                    <span class="match-rank">#{rank}</span>
                    <span class="match-name">{row['Career']}</span>
                    <span class="match-pct">{pct:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(float(row["Probability"]))

        st.divider()

        # =============================================
        # 4 & 5. SKILL GAP ANALYSIS — Strengths + Improve
        # =============================================
        st.markdown('<div class="section-header">🧠 Skill Gap Analysis</div>', unsafe_allow_html=True)

        strengths = []
        improvements = []

        skill_checks = [
            ("Programming Skill", programming_skill, 10, 7),
            ("Problem Solving", problem_solving, 10, 7),
            ("Communication", communication, 10, 7),
            ("Teamwork", teamwork, 10, 7),
            ("Interview Score", interview_score, 100, 70),
            ("Resume Score", resume_score, 100, 70),
        ]
        for name, val, max_val, threshold in skill_checks:
            if val >= threshold:
                strengths.append((name, val, max_val))
            else:
                pri = "High" if val < threshold * 0.6 else "Medium"
                improvements.append((name, val, max_val, pri))

        if cgpa >= 7.5: strengths.append(("CGPA", cgpa, 10))
        else: improvements.append(("CGPA", cgpa, 10, "Medium" if cgpa >= 5 else "High"))

        if projects >= 3: strengths.append(("Projects", projects, 5))
        else: improvements.append(("Practical Projects", projects, 5, "High"))

        if internships >= 1: strengths.append(("Internships", internships, 3))
        else: improvements.append(("Industry Experience", internships, 3, "Medium"))

        gap_col1, gap_col2 = st.columns(2)

        with gap_col1:
            st.markdown("#### 💪 Your Strengths")
            if strengths:
                for name, val, max_val in strengths:
                    pct = min(val / max_val, 1.0)
                    st.markdown(f"**{name}** — {val}/{max_val}")
                    st.progress(pct)
            else:
                st.info("Focus on building your foundational skills!")

        with gap_col2:
            st.markdown("#### 🚀 Skills to Improve")
            if improvements:
                for name, val, max_val, pri in improvements:
                    badge_cls = f"badge-{pri.lower()}"
                    st.markdown(f'**{name}** <span class="badge {badge_cls}">{pri} Priority</span>', unsafe_allow_html=True)
                    st.progress(min(val / max_val, 1.0))
            else:
                st.success("🌟 You have a very well-rounded profile!")

        # Domain skills
        required_skills = get_required_skills(predicted_career)
        st.markdown(f"**Domain skills for {predicted_career}:** " + " · ".join(required_skills))

        st.divider()

        # =============================================
        # 6. CAREER ROADMAP
        # =============================================
        st.markdown('<div class="section-header">🗺️ Learning Roadmap</div>', unsafe_allow_html=True)

        roadmap = get_career_roadmap(predicted_career)

        road_col1, road_col2, road_col3 = st.columns([1, 3, 1])
        with road_col2:
            for i, step in enumerate(roadmap, 1):
                connector = '<div class="roadmap-connector"></div>' if i < len(roadmap) else ""
                st.markdown(f"""
                <div class="roadmap-step">
                    <div class="roadmap-line">
                        <div class="roadmap-dot">{i:02d}</div>
                        {connector}
                    </div>
                    <div class="roadmap-content"><p>{step}</p></div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # =============================================
        # 7. PLACEMENT READINESS
        # =============================================
        st.markdown('<div class="section-header">📊 Placement Readiness Score</div>', unsafe_allow_html=True)

        readiness = calculate_readiness_score(
            cgpa, programming_skill, projects, internships,
            communication, resume_score, interview_score, employability_score
        )
        level_text, level_color = get_readiness_level(readiness)

        ready_col1, ready_col2 = st.columns([1, 1])

        with ready_col1:
            st.markdown(f"""
            <div class="readiness-big">
                <div class="score" style="color: {level_color};">{readiness}</div>
                <div class="out-of">/ 100</div>
                <div class="level" style="color: {level_color};">{level_text}</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(readiness / 100.0)

        with ready_col2:
            st.markdown("**Score Interpretation**")
            st.markdown("""
            <div class="scale-row"><span class="scale-range">80–100</span><span class="scale-label">Excellent Readiness</span></div>
            <div class="scale-row"><span class="scale-range">60–79</span><span class="scale-label">Good Progress</span></div>
            <div class="scale-row"><span class="scale-range">40–59</span><span class="scale-label">Developing</span></div>
            <div class="scale-row"><span class="scale-range">0–39</span><span class="scale-label">Needs Improvement</span></div>
            """, unsafe_allow_html=True)
            st.caption("ℹ️ This is an application-level readiness assessment, not a probability of "
                       "placement or a guarantee of employment.")

        st.divider()

        # =============================================
        # 8. PERSONALIZED FEEDBACK
        # =============================================
        if readiness >= 80:
            msg = ("You're showing strong preparation for your career journey. "
                   "Focus now on projects, portfolio quality, and interview practice.")
        elif readiness >= 60:
            msg = ("You're on the right track. Strengthening the highlighted skills "
                   "can significantly improve your career readiness.")
        elif readiness >= 40:
            msg = ("You have a foundation to build on. Focus on the highlighted "
                   "skills and practical projects to move forward.")
        else:
            msg = ("Don't worry — this is a starting point. Focus on the "
                   "highest-priority skills and build practical projects step by step.")

        st.markdown(f"""
        <div class="nextstep-box">
            <h4>✨ Your Personalized Feedback</h4>
            <p>{msg}</p>
        </div>
        """, unsafe_allow_html=True)


        # =============================================
        # AI CAREER ASSISTANT - OLLAMA CLOUD
        # =============================================

        st.divider()
        st.markdown("### 🤖 AI Career Assistant")
        st.write(
            "Get personalized career guidance, an 8-week learning "
            "roadmap, skill suggestions, and project ideas."
        )

        if st.button(
            "✨ Generate AI Career Guidance",
            type="primary",
            use_container_width=True,
            key="generate_ollama_guidance"
        ):
            student_profile = {
                "Age": age,
                "Major": major,
                "University Year": university_year,
                "CGPA": cgpa,
                "Programming Skill": programming_skill,
                "Projects Completed": projects,
                "Certifications": certifications,
                "Study Hours Per Week": study_hours,
                "Communication Skills": communication,
                "Problem Solving": problem_solving,
                "Placement Readiness Score": readiness,
                "Strengths": strengths,
                "Skills to Improve": improvements,
            }

            existing_recommendations = {
                "Required Skills": required_skills,
                "Career Roadmap": roadmap,
                "Career Description": career_desc,
                "Placement Readiness": readiness,
            }

            with st.spinner("Generating your personalized career plan..."):
                try:
                    guidance = generate_career_guidance(
                        student_profile=student_profile,
                        predicted_career=predicted_career,
                        existing_recommendations=existing_recommendations,
                    )
                    st.session_state["ollama_guidance"] = guidance
                    st.session_state.pop("ollama_guidance_error", None)

                except Exception as error:
                    st.session_state.pop("ollama_guidance", None)
                    st.session_state["ollama_guidance_error"] = str(error)
                    print(f"Ollama error: {error}")

        if st.session_state.get("ollama_guidance"):
            st.markdown("#### 🎯 Your Personalized AI Career Plan")
            st.markdown(st.session_state["ollama_guidance"])

        if st.session_state.get("ollama_guidance_error"):
            st.error(
                "Could not generate guidance. Check the VS Code terminal "
                "for the error details."
            )


# =====================================================================
# PAGE: MODEL ANALYTICS
# =====================================================================
elif page == "📊 Model Analytics":
    st.markdown("""
    <div class="hero-card">
        <h1>📊 Model Analytics</h1>
        <p>Explore the performance and internals of the trained Random Forest model.</p>
    </div>
    """, unsafe_allow_html=True)

    # Feature Importance
    st.markdown('<div class="section-header">🔬 Feature Importance</div>', unsafe_allow_html=True)

    preprocessor = model.named_steps["preprocessor"]
    rf_model = model.named_steps["model"]
    feature_names = preprocessor.get_feature_names_out()
    importances = rf_model.feature_importances_

    fi_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values("Importance", ascending=True)

    # Show top 20
    fi_top = fi_df.tail(20)
    # Clean names
    fi_top["Feature"] = fi_top["Feature"].str.replace("num__", "").str.replace("cat__", "")

    fig_fi = px.bar(
        fi_top, x="Importance", y="Feature", orientation="h",
        color="Importance", color_continuous_scale=["#c7d2fe", "#3b82f6", "#1e3a8a"]
    )
    fig_fi.update_layout(
        height=600, showlegend=False, coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Importance Score", gridcolor="#f1f5f9"),
        yaxis=dict(title=""),
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Inter")
    )
    st.plotly_chart(fig_fi, use_container_width=True)

    st.caption("Feature importances are extracted directly from the trained Random Forest model. "
               "Higher values indicate features that contribute more to the model's predictions.")

    # Model Details
    st.divider()
    st.markdown('<div class="section-header">🤖 Model Configuration</div>', unsafe_allow_html=True)

    det_col1, det_col2, det_col3 = st.columns(3)
    det_col1.metric("Algorithm", "Random Forest")
    det_col2.metric("Estimators", f"{rf_model.n_estimators}")
    det_col3.metric("Max Depth", f"{rf_model.max_depth if rf_model.max_depth else 'None (auto)'}")

    det_col4, det_col5, det_col6 = st.columns(3)
    det_col4.metric("Input Features", f"{len(model.feature_names_in_)}")
    det_col5.metric("Transformed Features", f"{len(feature_names)}")
    det_col6.metric("Output Classes", f"{len(model.classes_)}")

    # Career distribution in training data
    st.divider()
    st.markdown('<div class="section-header">📈 Training Data Distribution</div>', unsafe_allow_html=True)

    career_dist = df["Career_Field"].value_counts()
    career_dist = career_dist[career_dist.index != "Not Placed"]  # Filter Not Placed

    fig_pie = px.pie(
        values=career_dist.values,
        names=career_dist.index,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig_pie.update_layout(
        height=450,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Inter")
    )
    st.plotly_chart(fig_pie, use_container_width=True)


# =====================================================================
# PAGE: CAREER INSIGHTS
# =====================================================================
elif page == "💡 Career Insights":
    st.markdown("""
    <div class="hero-card">
        <h1>💡 Career Insights</h1>
        <p>Explore all career categories the model can predict and their key requirements.</p>
    </div>
    """, unsafe_allow_html=True)

    
    # Career categories overview
    st.markdown(
        '<div class="section-header">🎯 Career Categories</div>',
        unsafe_allow_html=True
    )

    for career in sorted(model.classes_):
        desc = get_career_description(career)
        skills = get_required_skills(career)
        roadmap = get_career_roadmap(career)

        with st.container(border=True):
            st.markdown(f"### 🎯 {career}")
            st.markdown(f"**About:** {desc}")
            st.markdown("**Key Skills:** " + " · ".join(skills))

            with st.expander("📚 View Learning Roadmap"):
                for i, step in enumerate(roadmap, 1):
                    st.markdown(f"{i}. {step}")

    

    # Feature Importance Summary
    st.divider()
    st.markdown('<div class="section-header">🔑 What Matters Most</div>', unsafe_allow_html=True)

    preprocessor = model.named_steps["preprocessor"]
    rf_model = model.named_steps["model"]
    feature_names = preprocessor.get_feature_names_out()
    importances = rf_model.feature_importances_

    fi_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values("Importance", ascending=False)

    fi_top10 = fi_df.head(10).copy()
    fi_top10["Feature"] = fi_top10["Feature"].str.replace("num__", "").str.replace("cat__", "")

    fig_bar = px.bar(
        fi_top10, x="Feature", y="Importance",
        color="Importance", color_continuous_scale=["#c7d2fe", "#3b82f6", "#1e3a8a"]
    )
    fig_bar.update_layout(
        height=400, showlegend=False, coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="", tickangle=-45),
        yaxis=dict(title="Importance", gridcolor="#f1f5f9"),
        margin=dict(l=10, r=10, t=10, b=80),
        font=dict(family="Inter")
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.caption("These are the top features that most influence the model's career predictions, "
               "extracted directly from the trained Random Forest.") 