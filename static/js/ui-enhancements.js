// Modern UI Enhancements
class UIEnhancements {
    constructor() {
        this.init();
    }

    init() {
        this.addLoadingStates();
        this.addFormValidation();
        this.addNotifications();
        this.addProgressBars();
        this.addAnimations();
    }

    addLoadingStates() {
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<span class="loading-spinner"></span> Processing...';
                    submitBtn.disabled = true;
                }
            });
        });
    }

    addFormValidation() {
        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('blur', this.validateField);
            input.addEventListener('input', this.clearValidation);
        });
    }

    validateField(e) {
        const field = e.target;
        const value = field.value.trim();
        
        if (field.required && !value) {
            field.classList.add('is-invalid');
            this.showFieldError(field, 'This field is required');
        } else if (field.type === 'email' && value && !this.isValidEmail(value)) {
            field.classList.add('is-invalid');
            this.showFieldError(field, 'Please enter a valid email');
        } else {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
            this.hideFieldError(field);
        }
    }

    clearValidation(e) {
        const field = e.target;
        field.classList.remove('is-invalid', 'is-valid');
        this.hideFieldError(field);
    }

    showFieldError(field, message) {
        let errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            field.parentNode.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
    }

    hideFieldError(field) {
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    addNotifications() {
        window.showNotification = (message, type = 'info') => {
            const notification = document.createElement('div');
            notification.className = `alert alert-${type} fade-in position-fixed`;
            notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
            notification.innerHTML = `
                <i class="fas fa-${this.getIcon(type)}"></i> ${message}
                <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
            `;
            document.body.appendChild(notification);
            
            setTimeout(() => notification.remove(), 5000);
        };
    }

    getIcon(type) {
        const icons = {
            success: 'check-circle',
            danger: 'exclamation-triangle',
            warning: 'exclamation-circle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    addProgressBars() {
        window.showProgress = (percentage) => {
            let progressBar = document.querySelector('.progress-bar');
            if (!progressBar) {
                const progressContainer = document.createElement('div');
                progressContainer.innerHTML = '<div class="progress-bar"></div>';
                progressContainer.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; z-index: 9999;';
                document.body.appendChild(progressContainer);
                progressBar = progressContainer.querySelector('.progress-bar');
            }
            progressBar.style.width = percentage + '%';
            
            if (percentage >= 100) {
                setTimeout(() => progressBar.parentElement.remove(), 500);
            }
        };
    }

    addAnimations() {
        // Add fade-in animation to cards
        document.querySelectorAll('.card').forEach((card, index) => {
            card.style.animationDelay = (index * 0.1) + 's';
            card.classList.add('fade-in');
        });

        // Add hover effects to buttons
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
            });
            
            btn.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new UIEnhancements();
});