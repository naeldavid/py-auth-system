// Dashboard Enhancements
class DashboardEnhancements {
    constructor() {
        this.init();
    }

    init() {
        this.addRealTimeStats();
        this.addCharts();
        this.addQuickActions();
        this.addNotificationCenter();
    }

    addRealTimeStats() {
        // Simulate real-time updates
        setInterval(() => {
            this.updateStats();
        }, 5000);
    }

    updateStats() {
        const stats = document.querySelectorAll('.stat-value');
        stats.forEach(stat => {
            const currentValue = parseInt(stat.textContent);
            const change = Math.floor(Math.random() * 10) - 5;
            const newValue = Math.max(0, currentValue + change);
            
            if (newValue !== currentValue) {
                stat.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    stat.textContent = newValue;
                    stat.style.transform = 'scale(1)';
                }, 150);
            }
        });
    }

    addCharts() {
        // Add simple activity chart
        const chartContainer = document.getElementById('activity-chart');
        if (chartContainer) {
            this.createActivityChart(chartContainer);
        }
    }

    createActivityChart(container) {
        const data = Array.from({length: 7}, () => Math.floor(Math.random() * 100));
        const maxValue = Math.max(...data);
        
        container.innerHTML = data.map((value, index) => `
            <div class="chart-bar" style="height: ${(value/maxValue) * 100}%; animation-delay: ${index * 0.1}s">
                <div class="chart-value">${value}</div>
            </div>
        `).join('');
    }

    addQuickActions() {
        const quickActions = document.querySelector('.quick-actions');
        if (quickActions) {
            quickActions.addEventListener('click', (e) => {
                if (e.target.classList.contains('quick-action-btn')) {
                    e.target.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        e.target.style.transform = 'scale(1)';
                    }, 150);
                }
            });
        }
    }

    addNotificationCenter() {
        const notifications = [
            { type: 'info', message: 'System backup completed successfully', time: '2 min ago' },
            { type: 'warning', message: 'High CPU usage detected', time: '5 min ago' },
            { type: 'success', message: 'New user registered', time: '10 min ago' }
        ];

        const notificationContainer = document.getElementById('notifications');
        if (notificationContainer) {
            notificationContainer.innerHTML = notifications.map(notif => `
                <div class="notification-item alert alert-${notif.type} fade-in">
                    <div class="d-flex justify-content-between">
                        <span>${notif.message}</span>
                        <small class="text-muted">${notif.time}</small>
                    </div>
                </div>
            `).join('');
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DashboardEnhancements();
});