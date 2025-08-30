function refreshActivity() {
    fetch('/api/admin/activity')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            const tbody = document.getElementById('loginActivity');
            tbody.innerHTML = '';
            
            data.activity.forEach(user => {
                const row = document.createElement('tr');
                const lastLogin = user.last_login === 'Never' ? 'Never' : 
                    new Date(user.last_login).toLocaleString();
                
                row.innerHTML = `
                    <td><strong>${user.username}</strong></td>
                    <td>${user.email}</td>
                    <td>${lastLogin}</td>
                    <td><span class="badge bg-${user.role === 'admin' ? 'danger' : 'primary'}">${user.role}</span></td>
                    <td><span class="badge bg-${user.last_login === 'Never' ? 'secondary' : 'success'}">${user.last_login === 'Never' ? 'Not logged in' : 'Active'}</span></td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('loginActivity').innerHTML = 
                '<tr><td colspan="5" class="text-center text-danger">Failed to load activity</td></tr>';
        });
}

// Load activity when page loads
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('loginActivity')) {
        refreshActivity();
    }
});