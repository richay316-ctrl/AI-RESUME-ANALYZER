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


st.set_page_config(
    page_title="Resume Job Match Scorer",
    page_icon="📄",
    layout="wide"
)


st.title("📄 Resume Job Match Scorer")


def main():

    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )


    job_description = st.text_area(
        "Paste Job Description"
    )


    if st.button("Analyze Match"):


        resume_text = extract_text_from_pdf(
            uploaded_file
        )


        score,_,_ = calculate_similarity(
            resume_text,
            job_description
        )


        st.metric(
            "Match Score",
            f"{score}%"
        )


        pie_chart(score)


        missing = get_missing_keywords(
            resume_text,
            job_description
        )


        st.subheader(
            "Missing Keywords"
        )

        st.write(missing)


        skills = extract_skills(
            resume_text
        )


        st.subheader(
            "Skills Found"
        )

        st.write(skills)



if __name__=="__main__":
    main()