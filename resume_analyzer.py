import PyPDF2
import anthropic
import sys
from dotenv import load_dotenv

load_dotenv()


# ── 第一步：读取 PDF ──────────────────────────
def read_pdf(path: str) -> str:
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        pages = [page.extract_text() for page in reader.pages]
    return "\n".join(pages)


# ── 第二步：调用 Claude API 分析 ──────────────
def analyze_resume(resume_text: str, jd_text: str) -> str:
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


# ── 主程序 ────────────────────────────────────
if __name__ == "__main__":
    try:
        pdf_path = sys.argv[1] if len(sys.argv) > 1 else "resume.pdf"
        jd_path = sys.argv[2] if len(sys.argv) > 2 else ""

        print(f"读取简历: {pdf_path}")
        resume_text = read_pdf(pdf_path)
        print(f"共 {len(resume_text)} 个字符\n")

        jd_content = ""
        if jd_path:
            print(f"读取JD: {jd_path}")

            with open(jd_path, "r") as file:
                jd_content = file.read()
            print(jd_content)

        print("正在分析，请稍候...\n")
        result = analyze_resume(resume_text, jd_content)
        # print(result)
        with open("output.txt", "w") as f:
            f.write(result)
        print("done! result saved to output.txt")
    except FileNotFoundError:
        print(f"file can't be found: {pdf_path}")
    except anthropic.BadRequestError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"an unexpected error occurred: {e}")
