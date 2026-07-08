import streamlit as st
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


from database import (
    create_table,
    save_analysis
)


# NLTK Download
nltk.download("punkt")
nltk.download("stopwords")


# Page Config
st.set_page_config(
    page_title="Resume Job Match Scorer",
    page_icon="📄",
    layout="wide"
)


# Database Table Create
create_table()


st.title("📄 Resume Job Match Scorer")


st.markdown("""
Upload your resume PDF and paste a job description.
This tool uses **TF-IDF + Cosine Similarity**
to check resume-job matching.
""")


# Sidebar

with st.sidebar:

    st.header("About")

    st.info("""
    This tool helps you:

    - Measure resume match score
    - Find missing keywords
    - Detect skills
    - Improve resume
    """)



# -----------------------------
# PDF Extractor
# -----------------------------

def extract_text_from_pdf(uploaded_file):

    try:

        pdf_reader = PyPDF2.PdfReader(
            uploaded_file
        )

        text = ""

        for page in pdf_reader.pages:

            text += page.extract_text()


        return text


    except Exception as e:

        st.error(
            f"PDF Error: {e}"
        )

        return ""



# -----------------------------
# Text Processing
# -----------------------------

def clean_text(text):

    text = text.lower()


    text = re.sub(
        r'[^a-zA-Z\s]',
        '',
        text
    )


    return text.strip()



def remove_stopwords(text):

    stop_words = set(
        stopwords.words("english")
    )


    words = word_tokenize(
        text
    )


    filtered = [
        word for word in words
        if word not in stop_words
    ]


    return " ".join(filtered)



# -----------------------------
# Similarity
# -----------------------------

def calculate_similarity(
        resume_text,
        job_description
):

    resume = remove_stopwords(
        clean_text(resume_text)
    )


    job = remove_stopwords(
        clean_text(job_description)
    )


    vectorizer = TfidfVectorizer()


    matrix = vectorizer.fit_transform(
        [
            resume,
            job
        ]
    )


    score = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0] * 100


    return round(score,2)



# -----------------------------
# Keywords
# -----------------------------

def get_missing_keywords(
        resume,
        job
):


    resume_words = set(
        remove_stopwords(
            clean_text(resume)
        ).split()
    )


    job_words = set(
        remove_stopwords(
            clean_text(job)
        ).split()
    )


    missing = job_words - resume_words


    return list(missing)[:20]



# -----------------------------
# Skills
# -----------------------------

SKILLS = [

"python",
"java",
"sql",
"excel",
"power bi",
"tableau",
"machine learning",
"deep learning",
"tensorflow",
"pandas",
"numpy",
"aws",
"docker",
"git",
"flask",
"django"

]



def extract_skills(text):

    text = text.lower()


    return [
        skill
        for skill in SKILLS
        if skill in text
    ]



# -----------------------------
# Main App
# -----------------------------

def main():


    uploaded_file = st.file_uploader(

        "Upload Resume PDF",

        type=["pdf"]

    )


    job_description = st.text_area(

        "Paste Job Description",

        height=200

    )



    if st.button("Analyze Match"):



        if uploaded_file is None:

            st.warning(
                "Please upload resume"
            )

            return



        if job_description.strip()=="":


            st.warning(
                "Please enter job description"
            )

            return




        with st.spinner(
            "Analyzing..."
        ):


            resume_text = extract_text_from_pdf(
                uploaded_file
            )



            if not resume_text:

                st.error(
                    "Cannot read PDF"
                )

                return



            score = calculate_similarity(

                resume_text,

                job_description

            )



            st.subheader(
                "Result"
            )



            st.metric(

                "Match Score",

                f"{score}%"

            )



            # Status

            if score < 40:

                st.warning(
                    "Low Match"
                )

            elif score < 70:

                st.info(
                    "Good Match"
                )

            else:

                st.success(
                    "Excellent Match"
                )




            # Pie Chart

            fig, ax = plt.subplots()


            ax.pie(

                [
                    score,
                    100-score
                ],

                labels=[

                    "Matched",
                    "Missing"

                ],

                autopct="%1.1f%%"

            )


            st.pyplot(fig)




            # Missing Keywords

            missing = get_missing_keywords(

                resume_text,

                job_description

            )


            st.subheader(
                "Missing Keywords"
            )


            st.write(
                missing
            )



            # Skills

            skills = extract_skills(

                resume_text

            )


            st.subheader(
                "Skills Found"
            )


            st.write(
                skills
            )



            # Save Database

            save_analysis(

                uploaded_file.name,

                job_description,

                score,

                skills,

                missing

            )


            st.success(
                "Data saved successfully"
            )



            # Gauge Chart


            fig, ax = plt.subplots(

                figsize=(6,1)

            )


            ax.barh(

                [0],

                [score],

                color="green"

            )


            ax.set_xlim(

                0,

                100

            )


            ax.set_yticks([])


            ax.set_xlabel(
                "Match Percentage"
            )


            st.pyplot(fig)





if __name__=="__main__":

    main()