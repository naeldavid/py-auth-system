function editFile(filename) {
    window.location.href = `/editor?file=${filename}`;
}

function deleteFile(filename) {
    if (confirm(`Delete ${filename}?`)) {
        fetch('/delete_file', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({filename: filename})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('File deleted!');
                location.reload();
            } else {
                alert('Error: ' + data.error);
            }
        });
    }
}

function loadUserInfo() {
    fetch(`/api/user/${document.querySelector('[data-username]').dataset.username}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                alert('Info refreshed!');
            }
        });
}

function showPasswordChange() {
    new bootstrap.Modal(document.getElementById('passwordModal')).show();
}

function showCreateUser() {
    new bootstrap.Modal(document.getElementById('createUserModal')).show();
}

document.getElementById('passwordForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    fetch('/change_password', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            current_password: document.getElementById('currentPassword').value,
            new_password: document.getElementById('newPassword').value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Password changed!');
            bootstrap.Modal.getInstance(document.getElementById('passwordModal')).hide();
        } else {
            alert('Error: ' + data.error);
        }
    });
});

document.getElementById('createUserForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    fetch('/create_user', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            username: document.getElementById('newUsername').value,
            email: document.getElementById('newEmail').value,
            password: document.getElementById('newUserPassword').value,
            role: document.getElementById('newRole').value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('User created!');
            bootstrap.Modal.getInstance(document.getElementById('createUserModal')).hide();
            document.getElementById('createUserForm').reset();
        } else {
            alert('Error: ' + data.error);
        }
    });
});