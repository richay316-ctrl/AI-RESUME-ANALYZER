from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.corpus import stopwords

# ---------------------------------------------------
# Download Stopwords
# ---------------------------------------------------

try:
    stop_words = set(stopwords.words("english"))
except:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))

# ---------------------------------------------------
# Load AI Models
# ---------------------------------------------------

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
kw_model = KeyBERT(embedding_model)

# ---------------------------------------------------
# AI Categories
# ---------------------------------------------------

SECTION_TEXT = {
    "Technical Skills":
        "programming python java c++ sql html css javascript react node docker kubernetes aws cloud machine learning artificial intelligence deep learning database",

    "Professional Skills":
        "communication teamwork leadership presentation management collaboration analytical thinking problem solving",

    "Projects / Experience":
        "project internship work experience software development implementation deployment research",

    "Education":
        "degree university certification education training"
}

# ---------------------------------------------------
# Extract Skills (AI)
# ---------------------------------------------------

def extract_skills(text):

    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1,3),
        stop_words="english",
        top_n=30
    )

    skills = []

    for keyword, score in keywords:

        if score > 0.20:
            skills.append(keyword.title())

    return list(dict.fromkeys(skills))


# ---------------------------------------------------
# AI Section Finder
# ---------------------------------------------------

def predict_section(keyword):

    keyword_embedding = embedding_model.encode(
        keyword,
        convert_to_tensor=True
    )

    best_section = "Experience"
    best_score = 0

    for section, desc in SECTION_TEXT.items():

        section_embedding = embedding_model.encode(
            desc,
            convert_to_tensor=True
        )

        similarity = util.cos_sim(
            keyword_embedding,
            section_embedding
        ).item()

        if similarity > best_score:

            best_score = similarity
            best_section = section

    return best_section


# ---------------------------------------------------
# AI Priority
# ---------------------------------------------------

def get_priority(keyword, jd_keywords):

    for word, score in jd_keywords:

        if word.lower() == keyword.lower():

            if score >= 0.60:
                return "High"

            elif score >= 0.40:
                return "Medium"

            else:
                return "Low"

    return "Low"


# ---------------------------------------------------
# Missing Keyword Detection
# ---------------------------------------------------

def get_missing_keywords_with_reason(
        resume_text,
        job_description
):

    resume_keywords = extract_skills(resume_text)

    jd_keywords = kw_model.extract_keywords(
        job_description,
        keyphrase_ngram_range=(1,3),
        stop_words="english",
        top_n=40
    )

    resume_embeddings = embedding_model.encode(
        resume_keywords,
        convert_to_tensor=True
    )

    results = []

    jd_lines = job_description.split("\n")

    for keyword, confidence in jd_keywords:

        keyword_embedding = embedding_model.encode(
            keyword,
            convert_to_tensor=True
        )

        found = False

        if len(resume_keywords) > 0:

            similarity = util.cos_sim(
                keyword_embedding,
                resume_embeddings
            )

            if similarity.max().item() > 0.70:
                found = True

        if not found:

            jd_line = "AI detected requirement"

            for line in jd_lines:

                if keyword.lower() in line.lower():

                    jd_line = line.strip()
                    break

            section = predict_section(keyword)

            priority = get_priority(
                keyword,
                jd_keywords
            )

            reason = (
                f"AI semantic analysis identified '{keyword}' "
                f"as an important requirement in the Job Description "
                f"but it could not find a matching skill or experience "
                f"in your resume."
            )

            suggestion = (
                f"If you possess experience related to '{keyword}', "
                f"include it in the '{section}' section with "
                f"projects, internships, certifications, or work experience."
            )

            results.append({

                "keyword": keyword.title(),

                "reason": reason,

                "priority": priority,

                "jd_line": jd_line,

                "section": section,

                "suggestion": suggestion

            })

    return results
