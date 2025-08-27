const htmlEditor = document.getElementById("html-editor");
const cssEditor = document.getElementById("css-editor");
const jsEditor = document.getElementById("js-editor");
const preview = document.getElementById("live-preview");
const saveBtn = document.getElementById("save-btn");
const exportBtn = document.getElementById("export-btn");

// Function to update live preview
function updatePreview() {
  const html = htmlEditor.value;
  const css = `<style>${cssEditor.value}</style>`;
  const js = `<script>${jsEditor.value}<\/script>`;
  preview.srcdoc = html + css + js;
}

// Event listeners to update preview
htmlEditor.addEventListener("input", updatePreview);
cssEditor.addEventListener("input", updatePreview);
jsEditor.addEventListener("input", updatePreview);

// Initial preview render
updatePreview();

// Save project to backend
saveBtn.addEventListener("click", () => {
  const projectName = prompt("Enter project name:");
  if (!projectName) return;
  fetch("/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: projectName,
      html: htmlEditor.value,
      css: cssEditor.value,
      js: jsEditor.value,
    }),
  })
    .then((res) => res.json())
    .then((data) => alert("Project saved!"));
});

// Export project as ZIP
exportBtn.addEventListener("click", () => {
  const projectName = prompt("Enter project name to export:");
  if (!projectName) return;
  window.location.href = `/export/${projectName}`;
});
