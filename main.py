import streamlit as st

from pdf_extractor import extract_text_from_pdf
from similarity import calculate_similarity
from keyword_extractor import (
    get_missing_keywords,
    extract_skills
)
from charts import (
    pie_chart,
    gauge_chart
)

# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="Resume Job Match Scorer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Sidebar ---------------- #

with st.sidebar:

    st.title("📄 Resume Analyzer")

    st.markdown("""
### 🚀 Features

- ✅ Measure Resume Match Score
- 🔍 Find Missing Keywords
- 💼 Detect Resume Skills
- 📈 Improve ATS Score
- 🎯 ATS-Friendly Analysis

---

### 📌 How to Use

1. Upload your Resume (PDF)
2. Paste the Job Description
3. Click **Analyze Match**
4. View Match Score
5. Check Missing Keywords
6. Improve Your Resume

---

### 💡 Tips

- Upload a clear PDF resume.
- Paste the complete job description.
- Add missing keywords to improve your ATS score.

---
Made with ❤️ using Streamlit
""")

# ---------------- Main Page ---------------- #

st.title("📄 Resume Job Match Scorer")

st.write(
    "Upload your resume and compare it with the job description."
)

uploaded_file = st.file_uploader(
    "📄 Upload Resume PDF",
    type=["pdf"]
)

job_description = st.text_area(
    "📝 Paste Job Description",
    height=220,
    placeholder="Paste the complete job description here..."
)

analyze = st.button("🚀 Analyze Match")

# ---------------- Analysis ---------------- #

if analyze:

    if uploaded_file is None:
        st.warning("⚠️ Please upload a Resume PDF.")
        st.stop()

    if not job_description.strip():
        st.warning("⚠️ Please paste the Job Description.")
        st.stop()

    with st.spinner("Analyzing Resume..."):

        resume_text = extract_text_from_pdf(uploaded_file)

        score, _, _ = calculate_similarity(
            resume_text,
            job_description
        )

    st.success("✅ Analysis Completed!")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🎯 Resume Match Score",
            f"{score}%"
        )

        pie_chart(score)

    with col2:
        gauge_chart(score)

    st.divider()

    st.subheader("🔍 Missing Keywords")

    missing = get_missing_keywords(
        resume_text,
        job_description
    )

    if missing:
        st.write(", ".join(missing))
    else:
        st.success("🎉 No important keywords are missing.")

    st.divider()

    st.subheader("💼 Skills Found")

    skills = extract_skills(resume_text)

    if skills:
        st.write(", ".join(skills))
    else:
        st.info("No skills detected.")

    st.divider()

    st.subheader("📈 Recommendation")

    if score >= 80:
        st.success("Excellent! Your resume is highly matched with the job description.")
    elif score >= 60:
        st.info("Good match. Add the missing keywords to improve your ATS score.")
    else:
        st.error("Low match score. Update your resume with relevant skills and keywords from the job description.")
