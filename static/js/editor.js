function saveFile() {
    const filename = document.getElementById('filename').value;
    const content = document.getElementById('editor').value;
    
    if (!filename) {
        alert('Enter filename');
        return;
    }
    
    fetch('/save_file', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({filename: filename, content: content})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('File saved!');
        } else {
            alert('Error: ' + data.error);
        }
    });
}

function loadFile() {
    const filename = document.getElementById('filename').value;
    
    if (!filename) {
        alert('Enter filename to load');
        return;
    }
    
    fetch(`/load_file/${filename}`)
    .then(response => response.json())
    .then(data => {
        if (data.content !== undefined) {
            document.getElementById('editor').value = data.content;
            alert('File loaded!');
        } else {
            alert('Error loading file');
        }
    });
}

// Auto-save every 30 seconds
setInterval(function() {
    const filename = document.getElementById('filename').value;
    const content = document.getElementById('editor').value;
    
    if (filename && content) {
        fetch('/save_file', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({filename: filename, content: content})
        });
    }
}, 30000);

// Load file from URL parameter
const urlParams = new URLSearchParams(window.location.search);
const fileParam = urlParams.get('file');
if (fileParam) {
    document.getElementById('filename').value = fileParam;
    loadFile();
}