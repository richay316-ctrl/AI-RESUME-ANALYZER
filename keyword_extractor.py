from text_processing import (
    clean_text,
    remove_stopwords
)


SKILLS=[
"python",
"java",
"sql",
"excel",
"machine learning",
"deep learning",
"tensorflow",
"pandas",
"numpy",
"aws",
"docker",
"git"
]


def extract_skills(text):

    text=text.lower()


    return [
        skill
        for skill in SKILLS
        if skill in text
    ]



def get_missing_keywords(
        resume,
        job):


    resume_words=set(
        remove_stopwords(
            clean_text(resume)
        ).split()
    )


    job_words=set(
        remove_stopwords(
            clean_text(job)
        ).split()
    )


    return list(
        job_words-resume_words
    )[:20]