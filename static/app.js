class WebWorkspace {
    constructor() {
        this.currentProject = null;
        this.currentFile = null;
        this.editor = null;
        this.files = [];
        this.isDarkTheme = true;
        
        this.initializeApp();
    }

    initializeApp() {
        this.setupEventListeners();
        this.loadProjects();
        this.setupTheme();
    }

    setupEventListeners() {
        // Initializer form
        document.getElementById('init-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.initializeProject();
        });

        // Project management
        document.getElementById('new-project-btn').addEventListener('click', () => {
            this.showInitializer();
        });

        document.getElementById('load-project-btn').addEventListener('click', () => {
            this.loadSelectedProject();
        });

        document.getElementById('back-to-init').addEventListener('click', () => {
            this.showInitializer();
        });

        // File operations
        document.getElementById('save-file-btn').addEventListener('click', () => {
            this.saveCurrentFile();
        });

        document.getElementById('run-btn').addEventListener('click', () => {
            this.runProject();
        });

        document.getElementById('export-project-btn').addEventListener('click', () => {
            this.exportProject();
        });

        document.getElementById('refresh-preview').addEventListener('click', () => {
            this.updatePreview();
        });

        // Theme toggle
        document.getElementById('theme-toggle').addEventListener('click', () => {
            this.toggleTheme();
        });
    }

    async initializeProject() {
        const formData = new FormData(document.getElementById('init-form'));
        const utilities = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
            .map(cb => cb.value);
        
        const projectData = {
            name: formData.get('project-name') || document.getElementById('project-name').value,
            frontend: document.getElementById('frontend-select').value,
            backend: document.getElementById('backend-select').value,
            utilities: utilities
        };

        try {
            const response = await fetch('/api/init', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(projectData)
            });

            const result = await response.json();
            if (result.status === 'success') {
                this.currentProject = result.project;
                await this.loadProjectFiles();
                this.showIDE();
                this.showMessage('Project initialized successfully!', 'success');
            }
        } catch (error) {
            this.showMessage('Failed to initialize project', 'error');
        }
    }

    async loadProjects() {
        try {
            const response = await fetch('/api/projects');
            const data = await response.json();
            const projectList = document.getElementById('project-list');
            
            projectList.innerHTML = '<option value="">Select a project...</option>';
            data.projects.forEach(project => {
                const option = document.createElement('option');
                option.value = project;
                option.textContent = project;
                projectList.appendChild(option);
            });
        } catch (error) {
            console.error('Failed to load projects:', error);
        }
    }

    async loadSelectedProject() {
        const projectName = document.getElementById('project-list').value;
        if (!projectName) return;
        
        this.currentProject = projectName;
        await this.loadProjectFiles();
        this.showIDE();
    }

    async loadProjectFiles() {
        try {
            const response = await fetch(`/api/project/${this.currentProject}/files`);
            const data = await response.json();
            this.files = data.files;
            this.renderFileTree();
            
            // Load first file
            if (this.files.length > 0) {
                await this.loadFile(this.files[0]);
            }
        } catch (error) {
            console.error('Failed to load project files:', error);
        }
    }

    renderFileTree() {
        const fileTree = document.getElementById('file-tree');
        fileTree.innerHTML = '';
        
        this.files.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.textContent = file;
            fileItem.addEventListener('click', () => this.loadFile(file));
            fileTree.appendChild(fileItem);
        });
    }

    async loadFile(filename) {
        try {
            const response = await fetch(`/api/file?project=${this.currentProject}&path=${filename}`);
            const data = await response.json();
            
            if (data.content !== undefined) {
                this.currentFile = filename;
                this.setupEditor(data.content, filename);
                this.updateActiveTab(filename);
                this.updateActiveFile(filename);
            }
        } catch (error) {
            console.error('Failed to load file:', error);
        }
    }

    setupEditor(content, filename) {
        const editorElement = document.getElementById('code-editor');
        
        if (this.editor) {
            this.editor.toTextArea();
        }
        
        editorElement.innerHTML = '';
        const textarea = document.createElement('textarea');
        textarea.value = content;
        editorElement.appendChild(textarea);
        
        const mode = this.getEditorMode(filename);
        this.editor = CodeMirror.fromTextArea(textarea, {
            lineNumbers: true,
            mode: mode,
            theme: this.isDarkTheme ? 'default' : 'default',
            autoCloseBrackets: true,
            matchBrackets: true,
            indentUnit: 2,
            tabSize: 2
        });
        
        this.editor.on('change', () => {
            if (filename.endsWith('.html') || filename.endsWith('.css') || filename.endsWith('.js')) {
                this.updatePreview();
            }
        });
    }

    getEditorMode(filename) {
        if (filename.endsWith('.html')) return 'htmlmixed';
        if (filename.endsWith('.css')) return 'css';
        if (filename.endsWith('.js')) return 'javascript';
        if (filename.endsWith('.py')) return 'python';
        return 'text';
    }

    updateActiveTab(filename) {
        const tabs = document.querySelector('.editor-tabs');
        tabs.innerHTML = `<div class="tab active" data-file="${filename}">${filename}</div>`;
    }

    updateActiveFile(filename) {
        document.querySelectorAll('.file-item').forEach(item => {
            item.classList.toggle('active', item.textContent === filename);
        });
    }

    async saveCurrentFile() {
        if (!this.currentFile || !this.editor) return;
        
        try {
            const response = await fetch('/api/file', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    project: this.currentProject,
                    path: this.currentFile,
                    content: this.editor.getValue()
                })
            });
            
            const result = await response.json();
            if (result.status === 'saved') {
                this.showMessage('File saved successfully!', 'success');
            }
        } catch (error) {
            this.showMessage('Failed to save file', 'error');
        }
    }

    updatePreview() {
        if (!this.currentProject) return;
        
        const previewFrame = document.getElementById('preview-frame');
        
        if (this.currentFile && this.currentFile.endsWith('.html')) {
            const htmlContent = this.editor.getValue();
            previewFrame.srcdoc = htmlContent;
        } else {
            previewFrame.src = `/api/preview/${this.currentProject}`;
        }
    }

    async runProject() {
        if (!this.currentProject) return;
        
        const consoleOutput = document.getElementById('console-output');
        consoleOutput.innerHTML = 'Running project...\n';
        
        try {
            const response = await fetch(`/api/run/${this.currentProject}`, {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (result.output) {
                consoleOutput.innerHTML += `<span class="success">${result.output}</span>\n`;
            }
            if (result.error) {
                consoleOutput.innerHTML += `<span class="error">${result.error}</span>\n`;
            }
        } catch (error) {
            consoleOutput.innerHTML += `<span class="error">Failed to run project</span>\n`;
        }
    }

    exportProject() {
        if (!this.currentProject) return;
        window.location.href = `/api/export/${this.currentProject}`;
    }

    showInitializer() {
        document.getElementById('initializer-panel').style.display = 'block';
        document.getElementById('project-selector').style.display = 'block';
        document.getElementById('ide-container').style.display = 'none';
        this.loadProjects();
    }

    showIDE() {
        document.getElementById('initializer-panel').style.display = 'none';
        document.getElementById('project-selector').style.display = 'none';
        document.getElementById('ide-container').style.display = 'block';
        
        setTimeout(() => {
            if (this.editor) {
                this.editor.refresh();
            }
            this.updatePreview();
        }, 100);
    }

    setupTheme() {
        const theme = localStorage.getItem('theme') || 'dark';
        this.isDarkTheme = theme === 'dark';
        document.body.setAttribute('data-theme', theme);
        document.getElementById('theme-toggle').textContent = this.isDarkTheme ? '☀️' : '🌙';
    }

    toggleTheme() {
        this.isDarkTheme = !this.isDarkTheme;
        const theme = this.isDarkTheme ? 'dark' : 'light';
        document.body.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        document.getElementById('theme-toggle').textContent = this.isDarkTheme ? '☀️' : '🌙';
    }

    showMessage(message, type = 'info') {
        const messageEl = document.createElement('div');
        messageEl.className = `message ${type}`;
        messageEl.textContent = message;
        messageEl.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem;
            border-radius: 4px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            z-index: 1000;
        `;
        
        document.body.appendChild(messageEl);
        setTimeout(() => messageEl.remove(), 3000);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new WebWorkspace();
});
