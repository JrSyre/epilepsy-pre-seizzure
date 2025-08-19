// Notification System
class NotificationSystem {
    constructor() {
        this.notifications = JSON.parse(localStorage.getItem('notifications')) || [];
        this.notificationBell = document.getElementById('notificationBell');
        this.notificationBadge = document.getElementById('notificationBadge');
        this.notificationDropdown = document.getElementById('notificationDropdown');
        this.notificationList = document.getElementById('notificationList');
        this.clearAllBtn = document.getElementById('clearAllNotifications');
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateBadge();
        this.renderNotifications();
        this.checkForReminders();
        
        // Check for reminders every minute
        setInterval(() => this.checkForReminders(), 60000);
    }

    setupEventListeners() {
        // Toggle notification dropdown
        this.notificationBell.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleDropdown();
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.notificationDropdown.contains(e.target) && 
                !this.notificationBell.contains(e.target)) {
                this.hideDropdown();
            }
        });

        // Clear all notifications
        this.clearAllBtn.addEventListener('click', () => {
            this.clearAllNotifications();
        });
    }

    toggleDropdown() {
        this.notificationDropdown.classList.toggle('show');
    }

    hideDropdown() {
        this.notificationDropdown.classList.remove('show');
    }

    addNotification(notification) {
        const newNotification = {
            id: Date.now() + Math.random(),
            ...notification,
            timestamp: new Date().toISOString(),
            unread: true
        };

        this.notifications.unshift(newNotification);
        this.saveNotifications();
        this.updateBadge();
        this.renderNotifications();
        
        // Show browser notification if supported
        this.showBrowserNotification(newNotification);
    }

    markAsRead(notificationId) {
        const notification = this.notifications.find(n => n.id === notificationId);
        if (notification) {
            notification.unread = false;
            this.saveNotifications();
            this.updateBadge();
            this.renderNotifications();
        }
    }

    removeNotification(notificationId) {
        this.notifications = this.notifications.filter(n => n.id !== notificationId);
        this.saveNotifications();
        this.updateBadge();
        this.renderNotifications();
    }

    clearAllNotifications() {
        this.notifications = [];
        this.saveNotifications();
        this.updateBadge();
        this.renderNotifications();
    }

    updateBadge() {
        const unreadCount = this.notifications.filter(n => n.unread).length;
        this.notificationBadge.textContent = unreadCount;
        this.notificationBadge.style.display = unreadCount > 0 ? 'flex' : 'none';
    }

    renderNotifications() {
        if (this.notifications.length === 0) {
            this.notificationList.innerHTML = '<div class="no-notifications">No notifications</div>';
            return;
        }

        this.notificationList.innerHTML = this.notifications.map(notification => `
            <div class="notification-item ${notification.unread ? 'unread' : ''}" 
                 data-id="${notification.id}">
                <div class="notification-content">
                    <div class="notification-icon ${notification.type}">
                        ${this.getIconForType(notification.type)}
                    </div>
                    <div class="notification-text">
                        <div class="notification-title">${notification.title}</div>
                        <div class="notification-message">${notification.message}</div>
                        <div class="notification-time">${this.formatTime(notification.timestamp)}</div>
                    </div>
                </div>
            </div>
        `).join('');

        // Add click listeners to notification items
        this.notificationList.querySelectorAll('.notification-item').forEach(item => {
            item.addEventListener('click', () => {
                const notificationId = parseFloat(item.dataset.id);
                this.markAsRead(notificationId);
                this.handleNotificationClick(notificationId);
            });
        });
    }

    getIconForType(type) {
        const icons = {
            medication: '💊',
            appointment: '📅',
            alert: '⚠️',
            reminder: '🔔',
            seizure: '⚡',
            progress: '📊'
        };
        return icons[type] || '🔔';
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (minutes < 1) return 'Just now';
        if (minutes < 60) return `${minutes}m ago`;
        if (hours < 24) return `${hours}h ago`;
        if (days < 7) return `${days}d ago`;
        
        return date.toLocaleDateString();
    }

    saveNotifications() {
        localStorage.setItem('notifications', JSON.stringify(this.notifications));
    }

    showBrowserNotification(notification) {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(notification.title, {
                body: notification.message,
                icon: '/assets/favicon.ico',
                tag: notification.id
            });
        }
    }

    handleNotificationClick(notificationId) {
        const notification = this.notifications.find(n => n.id === notificationId);
        if (!notification) return;

        // Navigate based on notification type
        switch (notification.type) {
            case 'medication':
                window.location.href = '/medication';
                break;
            case 'appointment':
                window.location.href = '/appointments';
                break;
            case 'progress':
                window.location.href = '/progress';
                break;
            case 'seizure':
                window.location.href = '/predict';
                break;
        }
    }

    // Check for medication reminders
    async checkForReminders() {
        try {
            // Check medication reminders
            const medicationResponse = await fetch('/api/medication');
            if (medicationResponse.ok) {
                const data = await medicationResponse.json();
                const medications = data.medications || [];
                
                medications.forEach(medication => {
                    this.checkMedicationReminder(medication);
                });
            }

            // Check appointment reminders
            const appointmentResponse = await fetch('/api/appointments');
            if (appointmentResponse.ok) {
                const data = await appointmentResponse.json();
                const appointments = data.appointments || [];
                
                appointments.forEach(appointment => {
                    this.checkAppointmentReminder(appointment);
                });
            }
        } catch (error) {
            console.error('Error checking reminders:', error);
        }
    }

    checkMedicationReminder(medication) {
        const now = new Date();
        const times = medication.times || [];
        
        times.forEach(time => {
            const [hours, minutes] = time.split(':').map(Number);
            const medicationTime = new Date();
            medicationTime.setHours(hours, minutes, 0, 0);
            
            // Check if it's time for medication (within 5 minutes)
            const timeDiff = Math.abs(now - medicationTime);
            const fiveMinutes = 5 * 60 * 1000;
            
            if (timeDiff <= fiveMinutes) {
                // Check if we already sent a notification for this time today
                const today = now.toDateString();
                const notificationKey = `med_${medication.id}_${today}_${time}`;
                
                if (!localStorage.getItem(notificationKey)) {
                    this.addNotification({
                        type: 'medication',
                        title: 'Medication Reminder',
                        message: `Time to take ${medication.drug_name} - ${medication.dosage}`,
                        priority: 'high'
                    });
                    
                    // Mark as sent for today
                    localStorage.setItem(notificationKey, 'true');
                }
            }
        });
    }

    checkAppointmentReminder(appointment) {
        const now = new Date();
        const appointmentDate = new Date(appointment.date + ' ' + appointment.time);
        
        // Check if appointment is within 1 hour
        const timeDiff = appointmentDate - now;
        const oneHour = 60 * 60 * 1000;
        
        if (timeDiff > 0 && timeDiff <= oneHour) {
            const notificationKey = `apt_${appointment.id}_reminder`;
            
            if (!localStorage.getItem(notificationKey)) {
                this.addNotification({
                    type: 'appointment',
                    title: 'Upcoming Appointment',
                    message: `You have an appointment with ${appointment.doctor} in ${Math.floor(timeDiff / 60000)} minutes`,
                    priority: 'high'
                });
                
                localStorage.setItem(notificationKey, 'true');
            }
        }
    }

    // Add sample notifications for demonstration
    addSampleNotifications() {
        this.addNotification({
            type: 'medication',
            title: 'Medication Reminder',
            message: 'Time to take your morning medication - Lamotrigine 100mg',
            priority: 'high'
        });

        this.addNotification({
            type: 'appointment',
            title: 'Appointment Tomorrow',
            message: 'You have a follow-up appointment with Dr. Smith tomorrow at 2:00 PM',
            priority: 'medium'
        });

        this.addNotification({
            type: 'reminder',
            title: 'Seizure Log Reminder',
            message: 'Don\'t forget to log any seizure activity in your progress tracker',
            priority: 'low'
        });
    }
}

// Initialize notification system when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const notificationSystem = new NotificationSystem();
    
    // Add sample notifications for demonstration (remove in production)
    if (notificationSystem.notifications.length === 0) {
        notificationSystem.addSampleNotifications();
    }
    
    // Request notification permission
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
    
    // Make notification system globally available
    window.notificationSystem = notificationSystem;
});
