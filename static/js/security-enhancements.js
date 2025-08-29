// Advanced Security Features
class SecurityEnhancements {
    constructor() {
        this.init();
    }

    init() {
        this.setupCSRFProtection();
        this.setupBiometricAuth();
        this.setupDeviceFingerprinting();
        this.setupSecurityMonitoring();
    }

    setupCSRFProtection() {
        // Add CSRF token to all forms
        const csrfToken = this.generateCSRFToken();
        document.cookie = `csrf_token=${csrfToken}; path=/; secure; samesite=strict`;
        
        document.querySelectorAll('form').forEach(form => {
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrf_token';
            csrfInput.value = csrfToken;
            form.appendChild(csrfInput);
        });

        // Add CSRF header to AJAX requests
        const originalFetch = window.fetch;
        window.fetch = function(url, options = {}) {
            if (options.method && options.method !== 'GET') {
                options.headers = options.headers || {};
                options.headers['X-CSRF-Token'] = csrfToken;
            }
            return originalFetch(url, options);
        };
    }

    generateCSRFToken() {
        return Array.from(crypto.getRandomValues(new Uint8Array(32)))
            .map(b => b.toString(16).padStart(2, '0')).join('');
    }

    setupBiometricAuth() {
        if (window.PublicKeyCredential) {
            this.addBiometricButton();
        }
    }

    addBiometricButton() {
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            const biometricBtn = document.createElement('button');
            biometricBtn.type = 'button';
            biometricBtn.className = 'btn btn-outline-primary w-100 mt-2';
            biometricBtn.innerHTML = '<i class="fas fa-fingerprint"></i> Use Biometric Login';
            biometricBtn.onclick = () => this.authenticateWithBiometric();
            
            loginForm.appendChild(biometricBtn);
        }
    }

    async authenticateWithBiometric() {
        try {
            const options = await this.getWebAuthnOptions();
            const credential = await navigator.credentials.get({
                publicKey: options
            });
            
            const response = await fetch('/auth/webauthn/verify', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    credentialId: credential.id,
                    signature: Array.from(new Uint8Array(credential.response.signature)),
                    authenticatorData: Array.from(new Uint8Array(credential.response.authenticatorData))
                })
            });
            
            if (response.ok) {
                window.location.href = '/dashboard';
            }
        } catch (error) {
            showNotification('Biometric authentication failed', 'danger');
        }
    }

    async getWebAuthnOptions() {
        const response = await fetch('/auth/webauthn/options');
        return await response.json();
    }

    setupDeviceFingerprinting() {
        this.deviceFingerprint = this.generateDeviceFingerprint();
        
        // Send fingerprint with login requests
        document.addEventListener('submit', (e) => {
            if (e.target.id === 'loginForm') {
                const fingerprintInput = document.createElement('input');
                fingerprintInput.type = 'hidden';
                fingerprintInput.name = 'device_fingerprint';
                fingerprintInput.value = this.deviceFingerprint;
                e.target.appendChild(fingerprintInput);
            }
        });
    }

    generateDeviceFingerprint() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        ctx.textBaseline = 'top';
        ctx.font = '14px Arial';
        ctx.fillText('Device fingerprint', 2, 2);
        
        const fingerprint = {
            userAgent: navigator.userAgent,
            language: navigator.language,
            platform: navigator.platform,
            screen: `${screen.width}x${screen.height}`,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            canvas: canvas.toDataURL(),
            webgl: this.getWebGLFingerprint()
        };
        
        return btoa(JSON.stringify(fingerprint)).substring(0, 32);
    }

    getWebGLFingerprint() {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl');
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            return gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
        } catch {
            return 'unknown';
        }
    }

    setupSecurityMonitoring() {
        // Monitor for suspicious activity
        let clickCount = 0;
        let keyCount = 0;
        
        document.addEventListener('click', () => {
            clickCount++;
            if (clickCount > 100) { // Suspicious rapid clicking
                this.reportSuspiciousActivity('rapid_clicking');
            }
        });
        
        document.addEventListener('keydown', () => {
            keyCount++;
            if (keyCount > 500) { // Suspicious rapid typing
                this.reportSuspiciousActivity('rapid_typing');
            }
        });
        
        // Reset counters periodically
        setInterval(() => {
            clickCount = 0;
            keyCount = 0;
        }, 60000);
        
        // Monitor for developer tools
        setInterval(() => {
            if (this.isDevToolsOpen()) {
                this.reportSuspiciousActivity('devtools_open');
            }
        }, 5000);
    }

    isDevToolsOpen() {
        const threshold = 160;
        return window.outerHeight - window.innerHeight > threshold ||
               window.outerWidth - window.innerWidth > threshold;
    }

    reportSuspiciousActivity(type) {
        fetch('/security/report', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                type: type,
                timestamp: Date.now(),
                fingerprint: this.deviceFingerprint
            })
        });
    }
}

// Initialize security enhancements
document.addEventListener('DOMContentLoaded', () => {
    new SecurityEnhancements();
});