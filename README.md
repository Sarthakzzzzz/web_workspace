# 🚀 Web_Workspace - Full-Stack Online Development Environment

A browser-based full-stack development environment where developers can build, test, and export projects without installing dependencies locally.

## ✨ Features

### 🎯 Project Initializer
- **Frontend Frameworks**: HTML/CSS/JS, React, Vue.js, Angular
- **Backend Frameworks**: Flask, Django, Express.js, FastAPI
- **Utilities**: TailwindCSS, Bootstrap, jQuery, Axios
- **Auto-generated project structure** based on selected stack

### 💻 Online IDE
- **Multi-pane code editor** with syntax highlighting (CodeMirror)
- **File explorer** with project navigation
- **Live preview** for frontend projects
- **Backend execution** sandbox for server-side code
- **Dark/Light theme** toggle
- **Resizable panels** for optimal workflow

### 🔧 Development Tools
- **Real-time preview** updates as you type
- **Project save/load** functionality
- **Export to ZIP** for local development
- **Console output** for debugging
- **Multi-file editing** with tabbed interface

## 🚀 Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Open your browser** and navigate to `http://localhost:5000`

4. **Create a new project**:
   - Choose your frontend framework (React, Vue, Angular, or HTML/CSS/JS)
   - Select a backend framework (optional)
   - Pick utilities like TailwindCSS or Bootstrap
   - Click "Initialize Project"

5. **Start coding**:
   - Use the file explorer to navigate your project
   - Edit files in the code editor
   - See live preview updates
   - Save and export when ready

## 🏗️ Project Structure

```
web_workspace/
├── app.py              # Flask backend server
├── templates/
│   └── index.html      # Main IDE interface
├── static/
│   ├── app.js         # Frontend JavaScript logic
│   └── styles.css     # IDE styling
├── projects/          # User projects storage
└── requirements.txt   # Python dependencies
```

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Editor**: CodeMirror for syntax highlighting
- **Storage**: File-based project management
- **Preview**: iframe for frontend, subprocess for backend

## 📋 API Endpoints

- `POST /api/init` - Initialize new project
- `GET /api/projects` - List all projects
- `GET /api/project/<name>/files` - Get project files
- `GET /api/file` - Load file content
- `POST /api/file` - Save file content
- `GET /api/preview/<project>` - Preview project
- `POST /api/run/<project>` - Run backend project
- `GET /api/export/<project>` - Export project as ZIP

## 🎨 Supported File Types

- **Frontend**: HTML, CSS, JavaScript, JSX, Vue, TypeScript
- **Backend**: Python, Node.js
- **Config**: JSON, YAML, XML
- **Styling**: CSS, SCSS, LESS

## 🔮 Future Enhancements

- [ ] Multi-user collaboration
- [ ] AI code suggestions
- [ ] Git integration
- [ ] Package manager integration
- [ ] Database connections
- [ ] Deployment to cloud platforms
- [ ] Real-time collaboration
- [ ] Plugin system

## 📝 License

MIT License - feel free to use this project for learning and development!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Web_Workspace** - Your personal cloud IDE, powered by Python + JavaScript 🚀