from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import anthropic
from dotenv import load_dotenv
import PyPDF2
import io

load_dotenv()

app = FastAPI()


# ── 读取PDF（从上传的文件）──────────────────
def read_pdf_from_bytes(file_bytes: bytes) -> str:
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    pages = [page.extract_text() for page in reader.pages]
    return "\n".join(pages)


# ── 分析简历 ────────────────────────────────
def analyze_resume(resume_text: str, jd_text: str = "") -> str:
    if jd_text:
        prompt = f"""
            分析简历和以下职位描述的匹配度：
                    
            职位描述：
            {jd_text}

            简历：
            {resume_text}

            请给出：
            1. 匹配的技能
            2. 缺少的关键词
            3. 简历需要修改的地方
            """
    else:

        prompt = f"""你是一个资深的澳洲IT招聘顾问。
                请分析以下简历，给出：

                1. 核心技术栈总结（3行以内）
                2. 最适合的3个岗位方向（附理由）
                3. 简历的3个优点
                4. 简历的3个需要改进的地方
                5. 针对MLOps Engineer岗位，还缺哪些关键词

                简历内容：
                {resume_text}
                """
    client = anthropic.Anthropic()  # 自动读取 ANTHROPIC_API_KEY
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


# ── API接口1：只分析简历 ────────────────────
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    pdf_content = read_pdf_from_bytes(contents)
    result = analyze_resume(pdf_content)
    return {"result": result}


# ── API接口2：简历+JD对比 ───────────────────
@app.post("/match")
async def match(file: UploadFile = File(...), jd: str = ""):
    contents = await file.read()
    pdf_content = read_pdf_from_bytes(contents)
    result = analyze_resume(pdf_content, jd)
    return {"result": result}


# ── 启动服务 ────────────────────────────────
# 终端运行：uvicorn api:app --reload
