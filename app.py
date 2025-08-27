from flask import Flask, render_template, request, send_file
import os
import zipfile

app = Flask(__name__)
PROJECT_DIR = "projects"

# Create projects folder if not exists
if not os.path.exists(PROJECT_DIR):
    os.mkdir(PROJECT_DIR)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/save", methods=["POST"])
def save_project():
    data = request.json
    name = data['name']
    html = data['html']
    css = data['css']
    js = data['js']

    project_path = os.path.join(PROJECT_DIR, name)
    os.makedirs(project_path, exist_ok=True)

    with open(os.path.join(project_path, "index.html"), "w") as f:
        f.write(html)
    with open(os.path.join(project_path, "style.css"), "w") as f:
        f.write(css)
    with open(os.path.join(project_path, "script.js"), "w") as f:
        f.write(js)

    return {"status": "success"}


@app.route("/export/<name>")
def export_project(name):
    project_path = os.path.join(PROJECT_DIR, name)
    zip_path = os.path.join(PROJECT_DIR, f"{name}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir(project_path):
            zipf.write(os.path.join(project_path, file), arcname=file)
    return send_file(zip_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
