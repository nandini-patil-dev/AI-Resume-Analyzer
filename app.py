
import streamlit as st
import html

from resume_parser import extract_resume_text
from skill_matcher import compare_skills
from ai_analyzer import generate_resume_feedback


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="NexaAI | Resume Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. SESSION STATE
# =========================================================

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "ai_feedback" not in st.session_state:
    st.session_state.ai_feedback = None

if "resume_name" not in st.session_state:
    st.session_state.resume_name = None


# =========================================================
# 3. CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ---------- GLOBAL ---------- */

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --background: #09090f;
    --sidebar: #0e0d17;
    --card: #141320;
    --card-hover: #1b192a;
    --purple: #9b72ff;
    --purple-light: #b69aff;
    --text: #f5f3ff;
    --muted: #9895aa;
    --border: rgba(167, 139, 250, 0.15);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            ellipse at 70% 0%,
            rgba(91, 45, 160, 0.13),
            transparent 40%
        ),
        #09090f;
    color: var(--text);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: #0e0d17;
    border-right: 1px solid rgba(167, 139, 250, 0.12);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

.brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 25px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -1px;
    margin-bottom: 4px;
}

.brand span {
    color: #a78bfa;
}

.brand-caption {
    color: #77738b;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 35px;
}

.sidebar-label {
    color: #77738b;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin: 20px 0 10px 0;
}

.sidebar-footer {
    background: #171426;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 15px;
    margin-top: 35px;
}

.sidebar-footer p {
    color: #aaa4c0;
    font-size: 12px;
    margin-bottom: 0;
}

/* ---------- TYPOGRAPHY ---------- */

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #f5f3ff !important;
}

.main-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(27px, 4vw, 39px);
    font-weight: 700;
    letter-spacing: -1.5px;
    color: #ffffff;
    margin-bottom: 5px;
}

.subtitle {
    color: #9691a9;
    font-size: 14px;
    margin-bottom: 25px;
}

.section-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #f5f3ff;
    margin-top: 28px;
    margin-bottom: 15px;
}

/* ---------- HERO ---------- */

.hero-card {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(
            circle at 90% 20%,
            rgba(167, 139, 250, 0.35),
            transparent 32%
        ),
        linear-gradient(
            120deg,
            #211638,
            #17132c 60%,
            #24164a
        );
    border: 1px solid rgba(167, 139, 250, 0.25);
    border-radius: 22px;
    padding: 35px;
    margin-bottom: 27px;
}

.hero-card h1 {
    font-size: clamp(25px, 3vw, 36px);
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 12px;
}

.hero-card p {
    color: #c2b8dc;
    font-size: 14px;
    max-width: 600px;
}

.hero-tag {
    display: inline-block;
    background: rgba(167, 139, 250, 0.15);
    color: #c4aaff;
    border: 1px solid rgba(167, 139, 250, 0.25);
    padding: 6px 12px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 18px;
}

.hero-visual {
    font-size: 85px;
    text-align: center;
    color: #c4aaff;
    text-shadow: 0 0 35px rgba(167, 139, 250, 0.7);
}

/* ---------- CARDS ---------- */

.stat-card {
    background: linear-gradient(145deg, #191727, #12111c);
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 21px;
    min-height: 135px;
}

.stat-icon {
    font-size: 23px;
    margin-bottom: 12px;
}

.stat-label {
    color: #9994ad;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 8px;
}

.stat-value {
    color: #ffffff;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 27px;
    font-weight: 700;
}

.panel {
    background: #141320;
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 23px;
    margin-bottom: 17px;
}

.panel-title {
    font-size: 16px;
    font-weight: 700;
    color: #f5f3ff;
    margin-bottom: 7px;
}

.panel-description {
    color: #9691a9;
    font-size: 12px;
}

/* ---------- SKILL TAGS ---------- */

.skill-tag {
    display: inline-block;
    background: rgba(167, 139, 250, 0.12);
    border: 1px solid rgba(167, 139, 250, 0.23);
    color: #c4aaff;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
    font-weight: 600;
    margin: 4px 4px 4px 0;
}

.matched-tag {
    background: rgba(34, 197, 94, 0.10);
    border: 1px solid rgba(34, 197, 94, 0.22);
    color: #86efac;
}

.missing-tag {
    background: rgba(251, 146, 60, 0.10);
    border: 1px solid rgba(251, 146, 60, 0.22);
    color: #fdba74;
}

/* ---------- UPLOAD ---------- */

[data-testid="stFileUploader"] {
    background: #171525;
    border: 1px dashed #8062c9;
    border-radius: 15px;
    padding: 18px;
}

[data-testid="stFileUploader"] section {
    background: transparent;
}

[data-testid="stFileUploader"] label {
    color: #e9e4f7 !important;
}

/* ---------- INPUTS ---------- */

.stTextArea textarea {
    background: #171525 !important;
    color: #f5f3ff !important;
    border: 1px solid #38304e !important;
    border-radius: 12px !important;
}

.stTextArea textarea:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 1px #a78bfa !important;
}

.stTextInput input {
    background: #171525 !important;
    color: white !important;
    border: 1px solid #38304e !important;
}

/* ---------- BUTTONS ---------- */

.stButton > button {
    background: linear-gradient(100deg, #8b5cf6, #6d28d9);
    color: #ffffff;
    border: none;
    border-radius: 11px;
    min-height: 46px;
    font-weight: 700;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background: linear-gradient(100deg, #a78bfa, #8b5cf6);
    color: white;
    border: none;
    box-shadow: 0 5px 22px rgba(139, 92, 246, 0.3);
    transform: translateY(-2px);
}

.stDownloadButton > button {
    background: #211b34;
    border: 1px solid #7252b7;
    color: #c4aaff;
    border-radius: 10px;
}

/* ---------- METRICS ---------- */

[data-testid="stMetric"] {
    background: #191727;
    border: 1px solid var(--border);
    padding: 17px;
    border-radius: 15px;
}

[data-testid="stMetricLabel"] {
    color: #aaa4bd !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
    font-family: 'Space Grotesk', sans-serif;
}

/* ---------- PROGRESS ---------- */

.stProgress > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #c4aaff);
}

/* ---------- EXPANDER ---------- */

.streamlit-expanderHeader {
    background: #191727;
    border-radius: 10px;
    color: white;
}

/* ---------- DIVIDER ---------- */

hr {
    border-color: rgba(167, 139, 250, 0.13);
}

/* ---------- FOOTER ---------- */

.footer {
    text-align: center;
    color: #6f6a80;
    font-size: 11px;
    padding: 25px 0 5px 0;
}

/* ---------- RESPONSIVE ---------- */

@media(max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    .hero-card {
        padding: 23px;
    }

    .hero-visual {
        font-size: 55px;
    }

    .stat-card {
        padding: 14px;
    }

    .stat-value {
        font-size: 22px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. HELPER FUNCTIONS
# =========================================================

def render_skill_tags(skills, css_class=""):
    """Display skills as styled tags."""

    if not skills:
        st.caption("No skills found.")
        return

    tags = ""

    for skill in skills:
        safe_skill = html.escape(str(skill))

        tags += (
            f'<span class="skill-tag {css_class}">'
            f'{safe_skill}</span>'
        )

    st.markdown(
        f'<div>{tags}</div>',
        unsafe_allow_html=True
    )


def render_stat(icon, label, value):
    """Display dashboard statistic cards."""

    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">{icon}</div>
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 5. SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="brand">Nexa<span>AI</span> ✦</div>
    <div class="brand-caption">Resume Intelligence</div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-label">WORKSPACE</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Analyze Resume",
            "About Project"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("""
    <div class="sidebar-label">POWERED BY</div>

    <div class="panel">
        <div class="panel-title">✦ Gemini AI</div>
        <div class="panel-description">
            Generative AI-powered resume insights
        </div>
    </div>

    <div class="sidebar-footer">
        <div style="color:#c4aaff;font-weight:700;">
            🚀 Career Growth
        </div>
        <p>Discover your strengths. Improve your skills. Get career-ready.</p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 6. DASHBOARD PAGE
# =========================================================

if page == "Dashboard":

    st.markdown("""
    <div class="hero-card">
        <div class="hero-tag">✦ AI-POWERED CAREER PLATFORM</div>
        <h1>Your Career Journey,<br>Powered by Intelligence.</h1>
        <p>
            Analyze your resume, discover skill gaps, and understand
            how well your profile matches your dream job.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">Your Workspace</div>',
        unsafe_allow_html=True
    )

    result = st.session_state.analysis_result

    if result:

        score = result["match_score"]

        matched_count = len(result["matched_skills"])
        missing_count = len(result["missing_skills"])
        resume_count = len(result["resume_skills"])

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            render_stat("🎯", "SKILL MATCH", f"{score}%")

        with c2:
            render_stat("✓", "MATCHED SKILLS", matched_count)

        with c3:
            render_stat("⚡", "SKILL GAPS", missing_count)

        with c4:
            render_stat("📄", "RESUME SKILLS", resume_count)

        st.markdown(
            '<div class="section-heading">Latest Analysis</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 1])

        with col1:

            st.markdown(f"""
            <div class="panel">
                <div class="panel-title">📄 Analyzed Resume</div>
                <p class="panel-description">
                    {html.escape(str(st.session_state.resume_name or "Uploaded resume"))}
                </p>
                <br>
                <div style="color:#c4aaff;font-size:13px;">
                    Resume successfully processed
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:

            st.markdown(f"""
            <div class="panel">
                <div class="panel-title">🎯 Job Compatibility</div>
                <div style="font-size:35px;font-weight:700;color:#c4aaff;">
                    {score}%
                </div>
                <div class="panel-description">
                    Keyword-based skill match score
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("View Latest Analysis →"):
            st.session_state.show_latest = True

        if st.session_state.get("show_latest", False):

            st.markdown("### Matched Skills")
            render_skill_tags(
                result["matched_skills"],
                "matched-tag"
            )

            st.markdown("### Missing Skills")
            render_skill_tags(
                result["missing_skills"],
                "missing-tag"
            )

            if st.session_state.ai_feedback:
                st.markdown("### AI Feedback")
                st.markdown(st.session_state.ai_feedback)

    else:

        c1, c2, c3 = st.columns(3)

        with c1:
            render_stat("📄", "RESUME ANALYSIS", "Ready")

        with c2:
            render_stat("🤖", "AI ENGINE", "Gemini")

        with c3:
            render_stat("🎯", "JOB MATCHING", "Ready")

        st.markdown("""
        <div class="panel">
            <div class="panel-title">Welcome to NexaAI</div>
            <p class="panel-description">
                You haven't analyzed a resume yet.
                Start your first analysis to see your career insights here.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.info("Open Analyze Resume from the sidebar to get started.")

    st.markdown(
        '<div class="section-heading">How It Works</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="panel">
            <div style="font-size:27px;">📤</div>
            <div class="panel-title">01. Upload Resume</div>
            <div class="panel-description">
                Upload your PDF resume securely for text extraction.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="panel">
            <div style="font-size:27px;">🔍</div>
            <div class="panel-title">02. Analyze Skills</div>
            <div class="panel-description">
                Compare your skills with the requirements of a job.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="panel">
            <div style="font-size:27px;">✨</div>
            <div class="panel-title">03. Get AI Insights</div>
            <div class="panel-description">
                Receive suggestions to improve your resume and skills.
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# 7. ANALYZE RESUME PAGE
# =========================================================

elif page == "Analyze Resume":

    st.markdown(
        '<div class="main-title">Resume Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="subtitle">
        Upload your resume and add a job description to discover your compatibility.
    </div>
    """, unsafe_allow_html=True)

    # Upload section

    st.markdown("""
    <div class="panel">
        <div class="panel-title">📄 Upload Your Resume</div>
        <div class="panel-description">
            Select a PDF file containing your resume.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose your resume",
        type=["pdf"],
        help="Upload a text-based PDF resume."
    )

    # Job description

    st.markdown("""
    <div class="panel">
        <div class="panel-title">🎯 Job Description</div>
        <div class="panel-description">
            Paste the job description you want to compare your resume against.
        </div>
    </div>
    """, unsafe_allow_html=True)

    job_description = st.text_area(
        "Job description",
        height=220,
        placeholder="""Example:

Role: Associate Cloud Engineer

Required Skills:
- AWS EC2, S3, IAM, VPC
- Linux
- Python
- Docker
- SQL
- Git and GitHub

Responsibilities:
- Deploy cloud applications
- Monitor cloud infrastructure
- Troubleshoot technical issues
""",
        label_visibility="collapsed"
    )

    st.markdown("")

    analyze_button = st.button(
        "✦  Analyze My Resume",
        type="primary",
        use_container_width=True
    )

    if analyze_button:

        if uploaded_file is None:
            st.error("Please upload your PDF resume.")

        elif not job_description.strip():
            st.error("Please paste a job description.")

        else:

            try:

                with st.spinner(
                    "Extracting resume details and analyzing your skills..."
                ):

                    # STEP 1: Extract PDF text

                    resume_text = extract_resume_text(uploaded_file)

                    if not resume_text.strip():
                        st.error(
                            "No readable text was found in this PDF. "
                            "Please upload a text-based PDF."
                        )
                        st.stop()

                    # STEP 2: Compare skills

                    result = compare_skills(
                        resume_text,
                        job_description
                    )

                    # STEP 3: Generate AI feedback

                    feedback = None
                    ai_error_message = None

                    try:

                        feedback = generate_resume_feedback(
                            resume_text,
                            job_description
                        )

                    except Exception as error:

                        ai_error_message = str(error)
                        print("Gemini API Error:", error)

                # Save results

                st.session_state.analysis_result = result
                st.session_state.ai_feedback = feedback
                st.session_state.resume_name = uploaded_file.name
                st.session_state.show_latest = False

                st.success("Resume analysis completed!")

                if ai_error_message:
                    st.warning(
                        "Gemini AI feedback could not be generated. "
                        "Your skill analysis is still available below. "
                        "Check your API quota or connection and try again later."
                    )

            except Exception as error:

                st.error(f"Something went wrong: {error}")

    # Display latest results

    result = st.session_state.analysis_result

    if result:

        st.markdown("---")

        st.markdown(
            '<div class="main-title">Your Analysis Results</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="subtitle">Here is your resume compatibility report.</div>',
            unsafe_allow_html=True
        )

        score = result["match_score"]

        # Score dashboard

        col1, col2 = st.columns([1, 2])

        with col1:

            st.markdown("""
            <div class="panel">
                <div class="panel-description">YOUR SKILL MATCH SCORE</div>
            </div>
            """, unsafe_allow_html=True)

            st.metric(
                label="Job Skill Match",
                value=f"{score}%"
            )

            st.progress(score / 100)

        with col2:

            st.markdown(f"""
            <div class="panel">
                <div class="panel-title">Your Career Compatibility</div>
                <p class="panel-description">
                    Your resume contains
                    <b style="color:#c4aaff;">
                    {len(result["matched_skills"])}
                    </b>
                    of the
                    <b style="color:#c4aaff;">
                    {len(result["required_skills"])}
                    </b>
                    detected skills required by this job description.
                </p>
                <p class="panel-description">
                    This is a keyword-based skill match indicator,
                    not a guaranteed job suitability score.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Skill statistics

        st.markdown(
            '<div class="section-heading">Skill Breakdown</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            render_stat(
                "✓",
                "MATCHED SKILLS",
                len(result["matched_skills"])
            )

        with c2:
            render_stat(
                "⚡",
                "MISSING SKILLS",
                len(result["missing_skills"])
            )

        with c3:
            render_stat(
                "📚",
                "TOTAL RESUME SKILLS",
                len(result["resume_skills"])
            )

        # Matched and missing skills

        st.markdown(
            '<div class="section-heading">Detailed Skill Analysis</div>',
            unsafe_allow_html=True
        )

        matched_col, missing_col = st.columns(2)

        with matched_col:

            st.markdown("""
            <div class="panel">
                <div class="panel-title">
                    <span style="color:#86efac;">●</span>
                    Matched Skills
                </div>
                <div class="panel-description">
                    Skills found in both your resume and the job description.
                </div>
            </div>
            """, unsafe_allow_html=True)

            render_skill_tags(
                result["matched_skills"],
                "matched-tag"
            )

        with missing_col:

            st.markdown("""
            <div class="panel">
                <div class="panel-title">
                    <span style="color:#fdba74;">●</span>
                    Missing Skills
                </div>
                <div class="panel-description">
                    Detected job requirements not found in your resume.
                </div>
            </div>
            """, unsafe_allow_html=True)

            render_skill_tags(
                result["missing_skills"],
                "missing-tag"
            )

        # Resume skills

        with st.expander("📄 View all skills detected in your resume"):

            render_skill_tags(result["resume_skills"])

        # AI Feedback

        st.markdown(
            '<div class="section-heading">✦ Gemini AI Resume Insights</div>',
            unsafe_allow_html=True
        )

        if st.session_state.ai_feedback:

            st.markdown("""
            <div class="panel">
                <div class="panel-title">Your Personalized AI Report</div>
                <div class="panel-description">
                    AI-generated recommendations based on your resume
                    and the provided job description.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(st.session_state.ai_feedback)

        else:

            st.warning(
                "AI feedback is currently unavailable. "
                "Your skill matching results are available above."
            )


# =========================================================
# 8. ABOUT PROJECT PAGE
# =========================================================

elif page == "About Project":

    st.markdown(
        '<div class="main-title">About NexaAI</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="subtitle">
        An AI-powered resume analysis and job matching application.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-card">
        <div class="hero-tag">ABOUT THE PROJECT</div>
        <h1>Making Job Preparation Smarter.</h1>
        <p>
            NexaAI helps candidates understand how their resume
            aligns with a job description. It combines PDF text
            extraction, skill matching, and Generative AI feedback.
        </p>
        <div class="hero-visual">✦</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Technology Stack")

    technologies = [
        ("🐍", "Python", "Core programming"),
        ("🎈", "Streamlit", "Interactive dashboard"),
        ("📄", "PyPDF", "PDF text extraction"),
        ("🔗", "LangChain", "LLM integration"),
        ("🤖", "Google Gemini", "AI feedback"),
        ("🧠", "NLP", "Skill analysis")
    ]

    cols = st.columns(3)

    for index, (icon, name, description) in enumerate(technologies):

        with cols[index % 3]:

            st.markdown(f"""
            <div class="panel">
                <div style="font-size:25px;">{icon}</div>
                <div class="panel-title">{name}</div>
                <div class="panel-description">{description}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Project Workflow")

    st.markdown("""
    <div class="panel">
        <p>01. Upload resume in PDF format</p>
        <p>↓</p>
        <p>02. Extract text using PyPDF</p>
        <p>↓</p>
        <p>03. Identify skills using Python</p>
        <p>↓</p>
        <p>04. Compare resume skills with job requirements</p>
        <p>↓</p>
        <p>05. Generate feedback using Gemini and LangChain</p>
        <p>↓</p>
        <p>06. Display the analysis dashboard</p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 9. FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    ✦ NEXAAI — RESUME INTELLIGENCE PLATFORM
    <br><br>
    Built with Python · Streamlit · LangChain · Google Gemini
</div>
""", unsafe_allow_html=True)
