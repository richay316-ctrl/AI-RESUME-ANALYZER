import streamlit as st

from pdf_extractor import extract_text_from_pdf
from similarity import calculate_similarity
from keyword_extractor import (
    get_missing_keywords,
    extract_skills,
)
from charts import pie_chart, gauge_chart


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* Buttons */

.stButton>button{
    width:100%;
    background:#2563eb;
    color:white;
    border:none;
    border-radius:10px;
    padding:12px;
    font-size:16px;
    font-weight:600;
}

.stButton>button:hover{
    background:#1d4ed8;
}

/* Metric Cards */

div[data-testid="stMetric"]{
    border:1px solid #d1d5db;
    border-radius:12px;
    padding:15px;
}

/* File uploader */

div[data-testid="stFileUploader"]{
    border:2px dashed #cbd5e1;
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("📄 AI Resume Analyzer")

    st.markdown("---")

    st.subheader("Features")

    st.write("✅ Resume Match Score")
    st.write("✅ Missing Keywords")
    st.write("✅ Skills Detection")
    st.write("✅ ATS Optimization")
    st.write("✅ Resume Recommendation")

    st.markdown("---")

    st.subheader("How to Use")

    st.write("1. Upload Resume")
    st.write("2. Paste Job Description")
    st.write("3. Click Analyze Resume")
    st.write("4. View Results")

# ---------------------------------------------------
# MAIN PAGE
# ---------------------------------------------------

st.title("📄 AI Resume Match Analyzer")

st.markdown(
    """
    <p style="color:#2563eb; font-size:18px;">
    Upload your resume and compare it with a job description 
    to measure ATS compatibility.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="color:#2563eb; font-size:18px; font-weight:700; margin-bottom:5px;">
    Upload Resume (PDF)
    </p>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "",
    type=["pdf"]
)

st.markdown(
    """
    <div style="margin-top:30px;">
    <p style="color:#2563eb; font-size:18px; font-weight:700;">
    Paste Job Description
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

job_description = st.text_area(
    "",
    height=220,
    placeholder="Paste the job description here..."
)

# Analyze Button
analyze = st.button("Analyze Resume")

# ---------------------------------------------------
# ANALYSIS
# ---------------------------------------------------

if analyze:

    if uploaded_file is None:
        st.warning("Please upload your resume.")
        st.stop()

    if not job_description.strip():
        st.warning("Please paste the job description.")
        st.stop()

    with st.spinner("Analyzing Resume..."):

        resume_text = extract_text_from_pdf(uploaded_file)

        score, _, _ = calculate_similarity(
            resume_text,
            job_description,
        )

    st.success("Analysis Completed Successfully")

    st.markdown("---")

    col1, col2 = st.columns([1,1])

    with col1:

        st.metric(
            "Resume Match Score",
            f"{score}%"
        )

        pie_chart(score)

    with col2:

        gauge_chart(score)

    st.markdown("---")

    st.subheader("Missing Keywords")

    missing = get_missing_keywords(
        resume_text,
        job_description,
    )

    if missing:

        cols = st.columns(4)

        for i, keyword in enumerate(missing):

            cols[i % 4].success(keyword)

    else:

        st.success("No important keywords are missing.")

    st.markdown("---")

    st.subheader("Skills Found")

    skills = extract_skills(resume_text)

    if skills:

        cols = st.columns(4)

        for i, skill in enumerate(skills):

            cols[i % 4].info(skill)

    else:

        st.info("No skills detected.")

    st.markdown("---")

    st.subheader("Recommendation")

    if score >= 80:

        st.markdown(
            """
            <div style="
            background-color:#dcfce7;
            border-left:6px solid #16a34a;
            padding:20px;
            border-radius:10px;
            color:#166534;">
            
            <h3>🟢 Excellent Match</h3>
            <p>Your resume is highly aligned with the job description.</p>
            
            ✔ Strong ATS Compatibility<br>
            ✔ Good Skill Match<br>
            ✔ Ready to Apply
            
            </div>
            """,
            unsafe_allow_html=True
        )


    elif score >= 70:

        st.markdown(
            """
            <div style="
            background-color:#fef9c3;
            border-left:6px solid #eab308;
            padding:20px;
            border-radius:10px;
            color:#854d0e;">
            
            <h3>🟡 Good Match</h3>
            <p>Your resume matches well but needs some improvements.</p>
            
            ✔ Add missing keywords<br>
            ✔ Improve project descriptions<br>
            ✔ Highlight technical skills
            
            </div>
            """,
            unsafe_allow_html=True
        )


    else:

        st.markdown(
            """
            <div style="
            background-color:#fee2e2;
            border-left:6px solid #dc2626;
            padding:20px;
            border-radius:10px;
            color:#991b1b;">
            
            <h3>🔴 Needs Improvement</h3>
            <p>Your resume needs more optimization for ATS compatibility.</p>
            
            ✔ Add required skills<br>
            ✔ Include job-specific keywords<br>
            ✔ Customize your resume
            
            </div>
            """,
            unsafe_allow_html=True
        )
            # ------------------------------------------------
    # Resume Rating
    # ------------------------------------------------

    st.markdown("---")
    st.subheader("⭐ Resume Rating")

    if score >= 90:
        rating = "⭐⭐⭐⭐⭐ Outstanding"
        st.success(rating)

    elif score >= 80:
        rating = "⭐⭐⭐⭐⭐ Excellent"
        st.success(rating)

    elif score >= 70:
        rating = "⭐⭐⭐⭐ Very Good"
        st.info(rating)

    elif score >= 60:
        rating = "⭐⭐⭐ Good"
        st.warning(rating)

    elif score >= 40:
        rating = "⭐⭐ Fair"
        st.warning(rating)

    else:
        rating = "⭐ Needs Improvement"
        st.error(rating)

    # ------------------------------------------------
    # Download Report
    # ------------------------------------------------

    st.markdown("---")
    st.subheader("📥 Download Analysis Report")

    report = f"""
==================================================
            AI RESUME ANALYSIS REPORT
==================================================

Resume Match Score : {score}%

Resume Rating : {rating}

--------------------------------------------------

Detected Skills

{', '.join(skills) if skills else 'No skills detected'}

--------------------------------------------------

Missing Keywords

{', '.join(missing) if missing else 'No missing keywords'}

--------------------------------------------------

Recommendation

"""

    if score >= 80:
        report += """
Excellent Match

Your resume is highly compatible with the job description.
You are ready to apply.
"""

    elif score >= 60:
        report += """
Good Match

Improve your resume by adding missing keywords,
technical skills and relevant projects.
"""

    else:
        report += """
Needs Improvement

Customize your resume according to the job description,
add relevant skills and improve project descriptions.
"""

    report += """

==================================================
Generated by AI Resume Analyzer
==================================================
"""

    st.download_button(
        label="📄 Download Report",
        data=report,
        file_name="Resume_Analysis_Report.txt",
        mime="text/plain",
    )

st.markdown("---")
st.caption("© 2026 AI Resume Analyzer | Built with Streamlit")

