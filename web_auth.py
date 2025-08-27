from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import datetime
import time
import os
from secure_auth_complete import SecureUserDatabase, SecurityConfig

app = Flask(__name__)
app.secret_key = os.urandom(24)
db = SecureUserDatabase()

@app.route('/')
def index():
    if 'session_token' in session:
        valid, username = db.validate_session(session['session_token'])
        if valid:
            return redirect(url_for('dashboard'))
        else:
            session.clear()
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    security_pin = request.form['security_pin']
    
    success, token, message = db.authenticate_user(username, password, security_pin)
    
    if success:
        session['session_token'] = token
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        flash(message, 'error')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'session_token' not in session:
        return redirect(url_for('index'))
    
    valid, username = db.validate_session(session['session_token'])
    if not valid:
        session.clear()
        flash('Session expired', 'error')
        return redirect(url_for('index'))
    
    user_data = db.get_user_data(username)
    return render_template('dashboard.html', user=user_data, username=username)

@app.route('/logout')
def logout():
    if 'session_token' in session:
        db.logout(session['session_token'])
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'session_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    valid, username = db.validate_session(session['session_token'])
    if not valid:
        return jsonify({'error': 'Session expired'}), 401
    
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')
    
    user_data = db.get_user_data(username)
    salt = user_data['salt']
    current_hash = db._hash_password_with_salt(current_password, salt)
    
    if current_hash != user_data['password_hash']:
        return jsonify({'error': 'Current password incorrect'}), 400
    
    # Update password
    import secrets
    new_salt = secrets.token_hex(32)
    new_hash = db._hash_password_with_salt(new_password, new_salt)
    
    db.users[username]['password_hash'] = new_hash
    db.users[username]['salt'] = new_salt
    db._save_users(db.users)
    
    return jsonify({'success': 'Password changed successfully'})

@app.route('/admin/users')
def admin_users():
    if 'session_token' not in session:
        return redirect(url_for('index'))
    
    valid, username = db.validate_session(session['session_token'])
    if not valid or username != 'nael':
        flash('Admin access required', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('admin_users.html', users=db.users)

@app.route('/editor')
def editor():
    if 'session_token' not in session:
        return redirect(url_for('index'))
    
    valid, username = db.validate_session(session['session_token'])
    if not valid:
        return redirect(url_for('index'))
    
    return render_template('editor.html', username=username)

@app.route('/save_file', methods=['POST'])
def save_file():
    if 'session_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    valid, username = db.validate_session(session['session_token'])
    if not valid:
        return jsonify({'error': 'Session expired'}), 401
    
    filename = request.json.get('filename')
    content = request.json.get('content')
    
    user_dir = f'user_files/{username}'
    os.makedirs(user_dir, exist_ok=True)
    
    with open(f'{user_dir}/{filename}', 'w') as f:
        f.write(content)
    
    if filename not in db.users[username]['files']:
        db.users[username]['files'].append(filename)
        db._save_users(db.users)
    
    return jsonify({'success': 'File saved successfully'})

@app.route('/load_file/<filename>')
def load_file(filename):
    if 'session_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    valid, username = db.validate_session(session['session_token'])
    if not valid:
        return jsonify({'error': 'Session expired'}), 401
    
    user_dir = f'user_files/{username}'
    file_path = f'{user_dir}/{filename}'
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        return jsonify({'content': content})
    
    return jsonify({'content': ''})

@app.route('/delete_file', methods=['POST'])
def delete_file():
    if 'session_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    valid, username = db.validate_session(session['session_token'])
    if not valid:
        return jsonify({'error': 'Session expired'}), 401
    
    filename = request.json.get('filename')
    user_dir = f'user_files/{username}'
    file_path = f'{user_dir}/{filename}'
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    if filename in db.users[username]['files']:
        db.users[username]['files'].remove(filename)
        db._save_users(db.users)
    
    return jsonify({'success': 'File deleted successfully'})

@app.route('/create_user', methods=['POST'])
def create_user():
    if 'session_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    valid, current_user = db.validate_session(session['session_token'])
    if not valid or current_user != 'nael':
        return jsonify({'error': 'Admin access required'}), 403
    
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    role = request.json.get('role', 'user')
    
    if username in db.users:
        return jsonify({'error': 'User already exists'}), 400
    
    import secrets
    salt = secrets.token_hex(32)
    db.users[username] = {
        'password_hash': db._hash_password_with_salt(password, salt),
        'salt': salt,
        'security_pin_hash': db._hash_password_with_salt('000', salt),
        'email': email,
        'role': role,
        'mfa_enabled': True,
        'created_at': datetime.now().isoformat(),
        'last_login': None,
        'files': []
    }
    db._save_users(db.users)
    
    return jsonify({'success': 'User created successfully'})

@app.route('/send_2fa', methods=['POST'])
def send_2fa():
    username = request.json.get('username')
    if username not in db.users:
        return jsonify({'error': 'User not found'}), 404
    
    import random
    from email_sender import SecureEmailSender
    
    code = str(random.randint(100000, 999999))
    
    if not hasattr(db, 'temp_codes'):
        db.temp_codes = {}
    db.temp_codes[username] = {'code': code, 'timestamp': time.time()}
    
    user_email = db.users[username]['email']
    
    # Use professional email sender
    email_sender = SecureEmailSender()
    success = email_sender.send_2fa_code(user_email, code, username)
    
    if success:
        return jsonify({'success': 'Verification code sent to your email'})
    else:
        print(f"Email failed: 2FA Code for {username}: {code}")
        return jsonify({'success': 'Verification code sent (check console for demo)'})

@app.route('/verify_2fa', methods=['POST'])
def verify_2fa():
    username = request.json.get('username')
    code = request.json.get('code')
    
    if not hasattr(db, 'temp_codes') or username not in db.temp_codes:
        return jsonify({'error': 'No verification code found'}), 400
    
    stored_data = db.temp_codes[username]
    if time.time() - stored_data['timestamp'] > 300:  # 5 minutes expiry
        del db.temp_codes[username]
        return jsonify({'error': 'Verification code expired'}), 400
    
    if code == stored_data['code']:
        del db.temp_codes[username]
        return jsonify({'success': 'Verification successful'})
    
    return jsonify({'error': 'Invalid verification code'}), 400

@app.route('/api/user/<username>')
def api_user_info(username):
    if 'session_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    valid, current_user = db.validate_session(session['session_token'])
    if not valid or current_user != username:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_data = db.get_user_data(username)
    if user_data:
        return jsonify({
            'username': username,
            'email': user_data['email'],
            'role': user_data['role'],
            'files': user_data['files'],
            'last_login': user_data.get('last_login'),
            'credentials': {
                'username': username,
                'password': 'password',
                'pin': '000'
            }
        })
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Enterprise Authentication Server Starting...")
    print("📍 Server URL: http://localhost:5000")
    print("📍 Network URL: http://0.0.0.0:5000")
    print("🔒 Secure Login Required")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)