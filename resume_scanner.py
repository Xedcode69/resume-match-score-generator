import fitz

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import string
import os


def extract_pdf_txt(name):
    path = os.path.join("uploads", name)
    resume = fitz.open(path)  # open a document
    res_content = ""
    for page in resume:  # iterate the document pages
        res_content += page.get_text()

    resume.close()
    return res_content


def clean(text):

    text = " ".join(text.split()).lower()  # removes extra spaces

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )  # remove special characters

    stop_words = set(stopwords.words("english"))

    final_txt = [word for word in text.split() if word not in stop_words]

    return " ".join(final_txt)


def get_match_score(jd_text, res_text):
    vector = TfidfVectorizer()

    matrix = vector.fit_transform([jd_text, res_text])

    similarity_scores = cosine_similarity(matrix[0], matrix[1])[0][0]

    return float(similarity_scores * 100)
