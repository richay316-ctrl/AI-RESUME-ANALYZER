from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity


from text_processing import (
    clean_text,
    remove_stopwords
)



def calculate_similarity(
        resume,
        job):


    resume = remove_stopwords(
        clean_text(resume)
    )


    job = remove_stopwords(
        clean_text(job)
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
    )[0][0]*100


    return round(score,2),resume,job