# مشروع PlusInspector - نسخة HTML جاهزة للرفع على GitHub

# هيكل المشروع:
# PlusInspector/
# ├── README.md
# ├── .gitignore
# ├── backend/
# │   ├── app.py
# │   ├── analyzer.py
# │   ├── requirements.txt
# │   └── index.html
# └── uploads/

# backend/requirements.txt
"""
fastapi
uvicorn
androguard
python-multipart
"""

# backend/analyzer.py
from androguard.core.bytecodes.apk import APK

def analyze_apk(file_path):
    apk = APK(file_path)
    permissions = apk.get_permissions()
    package_name = apk.get_package()
    version = apk.get_androidversion_name()
    activities = apk.get_activities()
    
    return {
        "package": package_name,
        "version": version,
        "permissions": permissions,
        "activities_count": len(activities)
    }

# backend/app.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from analyzer import analyze_apk
import shutil, os

app = FastAPI()
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("index.html")

@app.post("/upload/")
async def upload_apk(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = analyze_apk(file_path)
    os.remove(file_path)
    return result

# backend/index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PlusInspector</title>
</head>
<body>
  <h1>PlusInspector - رفع وتحليل APK</h1>
  <form id="uploadForm">
    <input type="file" id="fileInput" accept=".apk" required />
    <button type="submit">Upload APK</button>
  </form>
  <pre id="result"></pre>

  <script>
    const form = document.getElementById('uploadForm');
    const result = document.getElementById('result');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fileInput = document.getElementById('fileInput');
      const formData = new FormData();
      formData.append('file', fileInput.files[0]);

      const res = await fetch('/upload/', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      result.textContent = JSON.stringify(data, null, 2);
    });
  </script>
</body>
</html>
