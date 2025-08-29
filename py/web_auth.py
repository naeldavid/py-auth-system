from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import datetime
import time
import os
from py.secure_auth_complete import SecureUserDatabase, SecurityConfig

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'secure-auth-system-secret-key-2024'  # Use fixed key for persistent sessions
db = SecureUserDatabase("data/secure_users.json")

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
    
    # Validate credentials first
    if username not in db.users:
        flash('Invalid credentials', 'error')
        return redirect(url_for('index'))
    
    user_data = db.get_user_data(username)
    salt = user_data['salt']
    
    if (db._hash_password_with_salt(password, salt) != user_data['password_hash'] or
        db._hash_password_with_salt(security_pin, salt) != user_data['security_pin_hash']):
        flash('Invalid credentials', 'error')
        return redirect(url_for('index'))
    
    # If MFA enabled, send 2FA code
    if user_data.get('mfa_enabled', False):
        import secrets
        from py.email_sender import SecureEmailSender
        
        # Generate cryptographically secure 6-digit code
        code = str(secrets.randbelow(900000) + 100000)
        
        if not hasattr(db, 'temp_codes'):
            db.temp_codes = {}
        db.temp_codes[username] = {'code': code, 'timestamp': time.time()}
        
        email_sender = SecureEmailSender()
        success = email_sender.send_2fa_code(user_data['email'], code, username)
        
        if not success:
            print(f"Email failed: 2FA Code for {username}: {code}")
        
        session['pending_2fa'] = username
        return redirect(url_for('login_2fa'))
    
    # No MFA - direct login
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
    if not valid or username != 'admin':
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
    if not valid or current_user != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    pin = request.json.get('pin')
    role = request.json.get('role', 'user')
    
    if not username or not email or not password or not pin:
        return jsonify({'error': 'Username, email, password, and PIN are required'}), 400
    
    if username in db.users:
        return jsonify({'error': 'User already exists'}), 400
    
    import secrets
    salt = secrets.token_hex(32)
    db.users[username] = {
        'password_hash': db._hash_password_with_salt(password, salt),
        'salt': salt,
        'security_pin_hash': db._hash_password_with_salt(pin, salt),
        'email': email,
        'role': role,
        'mfa_enabled': True,
        'created_at': datetime.datetime.now().isoformat(),
        'last_login': None,
        'files': []
    }
    db._save_users(db.users)
    
    return jsonify({'success': 'User created successfully with 2FA enabled'})

@app.route('/delete_user', methods=['POST'])
def delete_user():
    if 'session_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    valid, current_user = db.validate_session(session['session_token'])
    if not valid or current_user != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    username = request.json.get('username')
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    if username == 'admin':
        return jsonify({'error': 'Cannot delete admin user'}), 400
    
    if username not in db.users:
        return jsonify({'error': 'User not found'}), 404
    
    # Delete user files
    import shutil
    user_dir = f'user_files/{username}'
    if os.path.exists(user_dir):
        shutil.rmtree(user_dir)
    
    # Remove user from database
    del db.users[username]
    db._save_users(db.users)
    
    return jsonify({'success': 'User deleted successfully'})

@app.route('/send_2fa', methods=['POST'])
def send_2fa():
    username = request.json.get('username')
    if username not in db.users:
        return jsonify({'error': 'User not found'}), 404
    
    import secrets
    from py.email_sender import SecureEmailSender
    
    # Generate cryptographically secure 6-digit code
    code = str(secrets.randbelow(900000) + 100000)
    
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

@app.route('/login_2fa')
def login_2fa():
    if 'pending_2fa' not in session:
        return redirect(url_for('index'))
    return render_template('login_2fa.html', username=session['pending_2fa'])

@app.route('/verify_2fa', methods=['POST'])
def verify_2fa():
    username = request.json.get('username')
    code = request.json.get('code')
    
    # Clean up expired codes first
    if hasattr(db, 'temp_codes'):
        expired_users = []
        for user, data in db.temp_codes.items():
            if time.time() - data['timestamp'] > 300:  # 5 minutes
                expired_users.append(user)
        for user in expired_users:
            del db.temp_codes[user]
    
    if not hasattr(db, 'temp_codes') or username not in db.temp_codes:
        return jsonify({'error': 'No verification code found or expired'}), 400
    
    stored_data = db.temp_codes[username]
    if time.time() - stored_data['timestamp'] > 300:  # 5 minutes expiry
        del db.temp_codes[username]
        return jsonify({'error': 'Verification code expired'}), 400
    
    if code == stored_data['code']:
        # Immediately dispose of the code after successful verification
        del db.temp_codes[username]
        
        # Create session after successful 2FA
        token = db._generate_session_token()
        db.active_sessions[token] = {
            'username': username,
            'created_at': time.time(),
            'last_activity': time.time()
        }
        
        session['session_token'] = token
        session['username'] = username
        session.pop('pending_2fa', None)
        
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
            'last_login': user_data.get('last_login')
        })
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Enterprise Authentication Server Starting...")
    print("📍 Server URL: http://localhost:8080")
    print("📍 Network URL: http://0.0.0.0:8080")
    print("🔒 Secure Login Required")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=8080)