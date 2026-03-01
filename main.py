from fastapi import FastAPI
from resume_scanner import extract_pdf_txt, clean, get_match_score


app = FastAPI()


@app.get("/scan")
def scanner(jd, name):
    res_content = extract_pdf_txt(name)

    res_txt = clean(res_content)
    jd_txt = clean(jd)

    score = get_match_score(jd_txt, res_txt)

    return {"Matching score": score}
