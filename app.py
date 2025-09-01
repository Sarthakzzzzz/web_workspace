from flask import Flask, render_template, request, send_file, jsonify
import os
import zipfile
import json
import subprocess
import tempfile

app = Flask(__name__)
PROJECTS_DIR = "projects"

if not os.path.exists(PROJECTS_DIR):
    os.makedirs(PROJECTS_DIR)

# Project templates
TEMPLATES = {
    'react': {
        'files': {
            'src/App.js': 'import React from "react";\n\nfunction App() {\n  return <div><h1>React App</h1></div>;\n}\n\nexport default App;',
            'src/index.js': 'import React from "react";\nimport ReactDOM from "react-dom";\nimport App from "./App";\n\nReactDOM.render(<App />, document.getElementById("root"));',
            'public/index.html': '<!DOCTYPE html>\n<html><head><title>React App</title></head><body><div id="root"></div></body></html>',
            'package.json': '{"name":"react-app","dependencies":{"react":"^18.0.0","react-dom":"^18.0.0"}}'
        }
    },
    'django': {
        'files': {
            'manage.py': '#!/usr/bin/env python\nimport os\nimport sys\nif __name__ == "__main__":\n    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")\n    from django.core.management import execute_from_command_line\n    execute_from_command_line(sys.argv)',
            'myproject/settings.py': 'DEBUG = True\nSECRET_KEY = "dev-key"\nINSTALLED_APPS = ["django.contrib.contenttypes", "django.contrib.auth"]\nROOT_URLCONF = "myproject.urls"',
            'myproject/urls.py': 'from django.urls import path\nfrom django.http import HttpResponse\n\ndef home(request):\n    return HttpResponse("<h1>Django App</h1>")\n\nurlpatterns = [path("", home)]'
        }
    },
    'html': {
        'files': {
            'index.html': '<!DOCTYPE html>\n<html><head><title>Web App</title><link rel="stylesheet" href="style.css"></head><body><h1>Hello World</h1><script src="script.js"></script></body></html>',
            'style.css': 'body { font-family: Arial, sans-serif; margin: 2rem; }\nh1 { color: #333; }',
            'script.js': 'console.log("Hello from JavaScript!");'
        }
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/init', methods=['POST'])
def init_project():
    data = request.json
    name = data.get('name', 'untitled')
    frontend = data.get('frontend', 'html')
    backend = data.get('backend', '')
    utilities = data.get('utilities', [])
    
    project_path = os.path.join(PROJECTS_DIR, name)
    os.makedirs(project_path, exist_ok=True)
    
    # Create frontend structure
    if frontend in TEMPLATES:
        for file_path, content in TEMPLATES[frontend]['files'].items():
            full_path = os.path.join(project_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
    
    # Create backend structure
    if backend and backend in TEMPLATES:
        backend_path = os.path.join(project_path, 'backend')
        os.makedirs(backend_path, exist_ok=True)
        for file_path, content in TEMPLATES[backend]['files'].items():
            full_path = os.path.join(backend_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
    
    # Save project config
    config = {'frontend': frontend, 'backend': backend, 'utilities': utilities}
    with open(os.path.join(project_path, 'project.json'), 'w') as f:
        json.dump(config, f)
    
    return jsonify({'status': 'success', 'project': name})

@app.route('/api/projects', methods=['GET'])
def list_projects():
    projects = [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]
    return jsonify({'projects': projects})

@app.route('/api/project/<name>/files', methods=['GET'])
def get_project_files(name):
    project_path = os.path.join(PROJECTS_DIR, name)
    files = []
    for root, dirs, filenames in os.walk(project_path):
        for filename in filenames:
            if filename.endswith(('.html', '.css', '.js', '.py', '.json')):
                rel_path = os.path.relpath(os.path.join(root, filename), project_path)
                files.append(rel_path)
    return jsonify({'files': files})

@app.route('/api/file', methods=['GET'])
def get_file():
    project = request.args.get('project')
    path = request.args.get('path')
    file_path = os.path.join(PROJECTS_DIR, project, path)
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return jsonify({'content': content})
    except:
        return jsonify({'error': 'File not found'}), 404

@app.route('/api/file', methods=['POST'])
def save_file():
    data = request.json
    project = data['project']
    path = data['path']
    content = data['content']
    file_path = os.path.join(PROJECTS_DIR, project, path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)
    return jsonify({'status': 'saved'})

@app.route('/api/preview/<project>')
def preview_project(project):
    project_path = os.path.join(PROJECTS_DIR, project)
    index_path = os.path.join(project_path, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            return f.read()
    return '<h1>No preview available</h1>'

@app.route('/api/run/<project>', methods=['POST'])
def run_backend(project):
    project_path = os.path.join(PROJECTS_DIR, project)
    backend_path = os.path.join(project_path, 'backend')
    
    if os.path.exists(os.path.join(backend_path, 'manage.py')):
        try:
            result = subprocess.run(['python', 'manage.py', 'runserver', '--noreload'], 
                                  cwd=backend_path, capture_output=True, text=True, timeout=5)
            return jsonify({'output': result.stdout, 'error': result.stderr})
        except:
            return jsonify({'error': 'Backend execution failed'})
    
    return jsonify({'error': 'No backend found'})

@app.route('/api/export/<project>')
def export_project(project):
    project_path = os.path.join(PROJECTS_DIR, project)
    zip_path = os.path.join(PROJECTS_DIR, f'{project}.zip')
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if not file.endswith('.zip'):
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, project_path)
                    zipf.write(file_path, arc_path)
    
    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
