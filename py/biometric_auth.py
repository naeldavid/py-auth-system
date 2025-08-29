import base64
import hashlib
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

class BiometricAuth:
    def __init__(self):
        self.registered_biometrics = {}
    
    def register_webauthn_credential(self, username, credential_data):
        """Register WebAuthn credential"""
        if username not in self.registered_biometrics:
            self.registered_biometrics[username] = []
        
        credential = {
            'id': credential_data['id'],
            'public_key': credential_data['publicKey'],
            'counter': 0,
            'created_at': credential_data.get('timestamp')
        }
        
        self.registered_biometrics[username].append(credential)
        return True
    
    def verify_webauthn_assertion(self, username, assertion_data):
        """Verify WebAuthn assertion"""
        if username not in self.registered_biometrics:
            return False
        
        for credential in self.registered_biometrics[username]:
            if credential['id'] == assertion_data['credentialId']:
                # In production, implement full WebAuthn verification
                # This is a simplified version
                return self._verify_signature(
                    credential['public_key'],
                    assertion_data['signature'],
                    assertion_data['authenticatorData']
                )
        return False
    
    def _verify_signature(self, public_key, signature, data):
        """Verify cryptographic signature"""
        try:
            # Simplified signature verification
            # In production, use proper WebAuthn libraries
            return True  # Placeholder
        except:
            return False
    
    def generate_challenge(self):
        """Generate cryptographic challenge"""
        import secrets
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
    
    def create_webauthn_options(self, username):
        """Create WebAuthn registration/authentication options"""
        challenge = self.generate_challenge()
        
        return {
            'challenge': challenge,
            'rp': {
                'name': 'Secure Auth System',
                'id': 'localhost'
            },
            'user': {
                'id': base64.urlsafe_b64encode(username.encode()).decode(),
                'name': username,
                'displayName': username
            },
            'pubKeyCredParams': [
                {'type': 'public-key', 'alg': -7},  # ES256
                {'type': 'public-key', 'alg': -257}  # RS256
            ],
            'timeout': 60000,
            'attestation': 'direct'
        }