
from flask import Flask, request, send_file
import pandas as pd
from fpdf import FPDF
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return '''
    <html><body>
    <h2>KoStable - 스테이블코인 회계 리포트</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="업로드 및 리포트 생성">
    </form>
    </body></html>
    '''

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file and file.filename.endswith(".csv"):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        df = pd.read_csv(filepath)

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("ArialUnicode", "", fname="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
        pdf.set_font("ArialUnicode", size=12)
        pdf.cell(200, 10, txt="KoStable 회계 리포트", ln=True, align="C")
        pdf.ln(10)
        for i in range(len(df)):
            row = df.iloc[i]
            text = " | ".join(f"{col}: {row[col]}" for col in df.columns)
            pdf.cell(200, 10, txt=text, ln=True)
        output_path = os.path.join(UPLOAD_FOLDER, "report.pdf")
        pdf.output(output_path)
        return send_file(output_path, as_attachment=True)
    return "CSV 파일만 업로드 가능합니다."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
