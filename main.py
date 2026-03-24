from fastapi import FastAPI, UploadFile, File, Form
from resume_scanner import extract_pdf_txt, clean, get_match_score
import shutil
import os


app = FastAPI()


@app.post("/scan")
async def scanner(jd: str = Form(...), file: UploadFile = File(...)):

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    filepath = os.path.join("uploads", file.filename)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    res_content = extract_pdf_txt(file.filename)

    res_txt = clean(res_content)
    jd_txt = clean(jd)

    score = get_match_score(jd_txt, res_txt)
    return {"Matching score": score}
