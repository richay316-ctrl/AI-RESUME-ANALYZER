import streamlit as st

from pdf_extractor import extract_text_from_pdf
from similarity import calculate_similarity
from keyword_extractor import (
    extract_skills,
    get_missing_keywords_with_reason
)
from charts import pie_chart, gauge_chart
import re  # Contact aur Email parse karne ke liye regular expressions
from charts import pie_chart, gauge_chart

import re
import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# HERO SECTION
# -----------------------------
left, right = st.columns([1.2, 1])

with left:

    st.markdown("""
    <h1 style="
        font-size:60px;
        font-weight:800;
        color:#1E1B4B;
        margin-bottom:5px;">
        AI Resume Analyzer
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
        font-size:18px;
        color:#6B7280;
        line-height:1.7;">
        Upload your resume and compare it with the job description.
        Get ATS Score, Missing Keywords, Skills Detection,
        and AI-powered Recommendations instantly.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.button("🚀 Analyze Resume")

    with c2:
        st.button("📄 Upload Resume")

with right:
    st.image(
        "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=900",
        use_container_width=True
    )

st.markdown("<br><br>", unsafe_allow_html=True)


# MySQL Database Functions
from database import (
    create_table,
    save_analysis
)


# Create Database Table
create_table()
# ---------------------------------------------------
# LOGIN & SIGNUP SYSTEM
# ---------------------------------------------------

import streamlit as st

# -----------------------------
# Demo Users
# -----------------------------
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": "12345",
        "user": "password"
    }

if "page" not in st.session_state:
    st.session_state.page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login_page():

    st.markdown("""
<style>
                /* Login form heading */
div[data-testid="stForm"] h3{
    color:#111827 !important;
}

/* Labels */
div[data-testid="stForm"] label{
    color:#111827 !important;
    font-weight:600;
}

/* Input text */
div[data-testid="stForm"] input{
    color:#111827 !important;
}

/* Placeholder */
div[data-testid="stForm"] input::placeholder{
    color:#6b7280 !important;
}

.main{
    background:#f5f7fb;
}

/* Header Card */
.header-card{
    max-width:500px;
    margin:auto;
    margin-top:30px;
    padding:30px;
    background:white;
    border-radius:20px;
    text-align:center;
    box-shadow:0 8px 25px rgba(0,0,0,.15);
}

/* Force text color */
.header-card h2{
    color:#111827 !important;
    font-size:38px;
    font-weight:700;
}

.header-card p{
    color:#6B7280 !important;
    font-size:16px;
}

.header-card h4{
    color:#2563eb !important;
}

/* Login Form */
div[data-testid="stForm"]{
    max-width:450px;
    margin:auto;
    padding:30px;
    border-radius:20px;
    background:white;
    box-shadow:0 8px 25px rgba(0,0,0,.18);
    margin-top:20px;
}

/* Buttons */
.stButton>button{
    width:100%;
    border-radius:10px;
    font-weight:bold;
    height:48px;
}

</style>
""", unsafe_allow_html=True)

    # ---------------- HOME ----------------

    if st.session_state.page == "home":

        col1, col2, col3 = st.columns([1,1,1])

        with col2:

            if st.button("🔑 Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

            st.write("")

            if st.button("📝 Sign Up", use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()

    # ---------------- LOGIN ----------------

    elif st.session_state.page == "login":

        with st.form("login_form"):

            st.subheader("🔐 Login Account")

            username = st.text_input(
                "Username",
                placeholder="Enter username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )

            login = st.form_submit_button("🚀 Login Now")

            if login:

                if (
                    username in st.session_state.users
                    and
                    st.session_state.users[username] == password
                ):

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.success("Login Successful")
                    st.rerun()

                else:
                    st.error("Invalid Username or Password")

        if st.button("⬅ Back"):
            st.session_state.page = "home"
            st.rerun()

    # ---------------- SIGNUP ----------------

    elif st.session_state.page == "signup":

        with st.form("signup_form"):

            st.subheader("📝 Create Account")

            new_username = st.text_input("Create Username")

            new_password = st.text_input(
                "Create Password",
                type="password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            signup = st.form_submit_button("Create Account")

            if signup:

                if new_username == "" or new_password == "":
                    st.warning("Please fill all fields")

                elif new_username in st.session_state.users:
                    st.error("Username already exists")

                elif new_password != confirm_password:
                    st.error("Passwords do not match")

                else:

                    st.session_state.users[new_username] = new_password

                    st.success("Account Created Successfully")

                    st.session_state.page = "login"

                    st.rerun()

        if st.button("⬅ Back"):
            st.session_state.page = "home"
            st.rerun()


# -----------------------------
# LOGIN CHECK
# -----------------------------

if not st.session_state.logged_in:
    login_page()
    st.stop()
# ---------------------------------------------------
# HELPER FUNCTIONS FOR EXTRACTION
# ---------------------------------------------------

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else "Not Detected"

def extract_contact(text):
    match = re.search(r'\b\d{10}\b|\+?\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}', text)
    return match.group(0) if match else "Not Detected"



# ---------------------------------------------------
# INITIALIZE STATE VARIABLES
# ---------------------------------------------------
if 'analyzed_data' not in st.session_state:
    st.session_state['analyzed_data'] = None

# ---------------------------------------------------
# SIDEBAR UI & NAVIGATION
# ---------------------------------------------------

with st.sidebar:
    # Profile metadata dynamic showcase card
    if st.session_state['analyzed_data'] is not None:
        data = st.session_state['analyzed_data']
        st.markdown(f"""
        <div class="sidebar-profile">
            <h4 style='margin:0; font-size:16px;'>👤 Profile</h4>
            <p style='margin:8px 0 2px 0; font-size:13px;'><b>Email:</b><br>{data['email']}</p>
            <p style='margin:0; font-size:13px;'><b>Contact:</b> {data['contact']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sidebar-profile">
            <h4 style='margin:0; font-size:16px;'>🚀 Workspace Active</h4>
            <p style='margin:5px 0 0 0; font-size:13px;'>
            Upload your resume document to unlock instant candidate meta metrics.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("✨ Select Feature")
    
    feature_choice = st.radio(
        "Choose what you want to view:",
        [
         "📊 Full Dashboard",
        "🎯 Resume Match Score",
        "📞 Contact Details",
        "📧 Email Extraction",
        "🔍 Missing Keywords",
        "🛠 Skills Detection",
        "📝 Recommendation & Rating",
        "📥 Download Report"
        ],
        label_visibility="collapsed"  # Clean look ke liye label hide kiya hai
    )

# ---------------------------------------------------
# MAIN PAGE
# ---------------------------------------------------

st.title("📄 AI Resume Match Analyzer")

st.markdown(
    """
    <p style="color:#2563eb; font-size:18px;">
    Upload your resume and compare it with a job description to measure ATS compatibility.
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

uploaded_file = st.file_uploader("", type=["pdf"])

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

job_description = st.text_area("", height=220, placeholder="Paste the job description here...")

# Analyze Button
analyze = st.button("Analyze Resume")

# ---------------------------------------------------
# PROCESSING METRICS
# ---------------------------------------------------

if analyze or st.session_state['analyzed_data'] is not None:

    if uploaded_file is None:
        st.warning("Please upload your resume.")
        st.stop()

    if not job_description.strip():
        st.warning("Please paste the job description.")
        st.stop()


    if analyze or st.session_state['analyzed_data'] is None:

        with st.spinner("Analyzing Resume..."):

            resume_text = extract_text_from_pdf(uploaded_file)

            score, _, _ = calculate_similarity(
                resume_text,
                job_description
            )

            missing = get_missing_keywords_with_reason(

             
             resume_text,
            job_description
            )

            skills = extract_skills(
    resume_text
)

            email_id = extract_email(resume_text)

            contact_num = extract_contact(resume_text)


            st.session_state['analyzed_data'] = {

                'score': score,
                'missing': missing,
                'skills': skills,
                'email': email_id,
                'contact': contact_num,
                'resume_text': resume_text

            }
            
            missing_keywords = [item["keyword"] for item in missing]

            # SAVE DATA INTO MYSQL
            save_analysis(
    uploaded_file.name,
    job_description,
    score,
    skills,
    [item["keyword"] for item in missing]
)


            st.success("Resume Analysis Saved in Database")

            st.rerun()




# -------------------------------
# After rerun display data
# -------------------------------

if st.session_state['analyzed_data'] is None:
    st.stop()


data = st.session_state['analyzed_data']

score = data['score']
missing = data['missing']
skills = data['skills']
email = data['email']
contact = data['contact']


# Resume Rating

if score >= 90:
    rating = "⭐⭐⭐⭐⭐ Outstanding"

elif score >= 80:
    rating = "⭐⭐⭐⭐⭐ Excellent"

elif score >= 70:
    rating = "⭐⭐⭐⭐ Very Good"

elif score >= 60:
    rating = "⭐⭐⭐ Good"

elif score >= 40:
    rating = "⭐⭐ Fair"

else:
    rating = "⭐ Needs Improvement"



st.markdown("---")

st.info(
    f"Showing Results for: **{feature_choice}**"
)



# 1. MATCH SCORE & CHARTS

if feature_choice in [
    "📊 Full Dashboard",
    "🎯 Resume Match Score"
]:

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



# 2. CONTACT DETAILS

if feature_choice in [
    "📊 Full Dashboard",
    "📞 Contact Details"
]:

    st.subheader(
        "📞 Extracted Contact Information"
    )

    st.info(
        f"**Phone / Contact Identifier:** {contact}"
    )

    st.markdown("---")



# 3. EMAIL EXTRACTION

if feature_choice in [
    "📊 Full Dashboard",
    "📧 Email Extraction"
]:

    st.subheader(
        "📧 Extracted Email Address"
    )

    st.success(
        f"**Primary Email Address:** {email}"
    )

    st.markdown("---")


# 4. MISSING KEYWORDS

if feature_choice in [
    "📊 Full Dashboard",
    "🔍 Missing Keywords"
]:

    st.subheader("🔍 Missing Keywords Analysis")

    if missing:

        for item in missing:

            with st.expander(f"❌ {item['keyword']}"):

                st.markdown("### 🔴 Reason")
                st.error(item["reason"])

                st.markdown("### ⭐ Priority")
                st.write(item["priority"])

                st.markdown("### 📄 Found in Job Description")
                st.code(item["jd_line"])

                st.markdown("### 📍 Add In Resume")
                st.info(item["section"])

                st.markdown("### 💡 Suggestion")
                st.success(item["suggestion"])

    else:

        st.success("✅ No important keywords are missing.")

    st.markdown("---")


# 5. SKILLS

if feature_choice in [
    "📊 Full Dashboard",
    "🛠 Skills Detection"
]:

    st.subheader(
        "Skills Found"
    )


    if skills:

        cols = st.columns(4)

        for i, skill in enumerate(skills):

            cols[i % 4].info(skill)

    else:

        st.info(
            "No skills detected."
        )


    st.markdown("---")
    



# 6. RECOMMENDATION

if feature_choice in [
    "📊 Full Dashboard",
    "📝 Recommendation & Rating"
]:


    st.subheader(
        "Recommendation"
    )


    if score >= 80:

        st.success(
            "🟢 Excellent Match\n\nYour resume is highly aligned with the job description."
        )


    elif score >= 70:

        st.warning(
            "🟡 Good Match\n\nImprove keywords and project descriptions."
        )


    else:

        st.error(
            "🔴 Needs Improvement\n\nCustomize your resume according to job requirements."
        )



    st.subheader(
        "⭐ Resume Rating"
    )


    if score >= 80:

        st.success(rating)

    elif score >= 60:

        st.info(rating)

    else:

        st.warning(rating)



    st.markdown("---")



# 7. DOWNLOAD REPORT

if feature_choice in [
    "📊 Full Dashboard",
    "📥 Download Report"
]:

    st.subheader(
        "📥 Download Analysis Report"
    )


    report = f"""
==================================================
          AI RESUME ANALYSIS REPORT
==================================================

Resume Match Score : {score}%

Resume Rating      : {rating}

Email Detected     : {email}

Contact Info       : {contact}


--------------------------------------------------
Detected Skills

{', '.join(skills) if skills else 'No skills detected'}


--------------------------------------------------
Missing Keywords




{', '.join([item['keyword'] for item in missing]) if missing else 'No missing keywords'}


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

Improve your resume by adding missing keywords and skills.
"""


    else:

        report += """
Needs Improvement

Customize your resume according to the job description.
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

        mime="text/plain"

    )



st.markdown("---")

st.caption(
    "© 2026 AI Resume Analyzer | Built with Streamlit"
)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="font-size:14px;">

    <h3 style="font-size:18px;">🤖 About AI Resume Analyzer</h3>

    AI Resume Analyzer is an intelligent tool that analyzes your resume 
    with job descriptions and calculates ATS compatibility, missing keywords, 
    and required skills to improve your career opportunities.

    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown("""
    <div style="text-align:center; font-size:14px;">

    <h3 style="font-size:18px;">🌐 Website</h3>

    www.airesumeanalyzer.com

    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown("""
    <div style="font-size:14px;">

    <h3 style="font-size:18px;">📞 Contact Details</h3>

    📧 Email:<br>
    support@airesumeanalyzer.com<br>

    📱 Phone:<br>
    +91 9876543210

    </div>
    """, unsafe_allow_html=True)
