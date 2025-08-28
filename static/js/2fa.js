document.getElementById('twoFactorForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const code = document.getElementById('verification_code').value;
    
    fetch('/verify_2fa', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: username, code: code})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/dashboard';
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        alert('Network error occurred');
    });
});

function resendCode() {
    const username = document.getElementById('username').value;
    
    fetch('/send_2fa', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: username})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('New code sent!');
        } else {
            alert('Error: ' + data.error);
        }
    });
}