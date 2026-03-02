// Main JavaScript for Lab Management System

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideUp 0.3s ease-out reverse';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
    
    // Set active menu item
    setActiveMenuItem();
    
    // Initialize modals
    initializeModals();
    
    // Initialize form validations
    initializeFormValidations();
});

// Set active menu item based on current page
function setActiveMenuItem() {
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            item.classList.add('active');
        }
    });
}

// Modal functionality
function initializeModals() {
    // Open modal
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
        }
    };
    
    // Close modal
    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
        }
    };
    
    // Close modal on outside click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });
}

// Form validations
function initializeFormValidations() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = 'var(--danger)';
                } else {
                    field.style.borderColor = 'var(--gray-light)';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showAlert('Please fill in all required fields', 'danger');
            }
        });
    });
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    const container = document.querySelector('.main-content');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.style.animation = 'slideUp 0.3s ease-out reverse';
            setTimeout(() => alertDiv.remove(), 300);
        }, 5000);
    }
}

// Confirm delete action
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Format datetime
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Search functionality
function initializeSearch(inputId, tableId) {
    const searchInput = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (searchInput && table) {
        searchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }
}

// Load equipment details
async function loadEquipmentDetails(equipmentId) {
    try {
        const response = await fetch(`/api/equipment/${equipmentId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error loading equipment details:', error);
        return null;
    }
}

// Load student details
async function loadStudentDetails(studentId) {
    try {
        const response = await fetch(`/api/student/${studentId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error loading student details:', error);
        return null;
    }
}

// Update equipment availability display
function updateAvailability(equipmentId) {
    loadEquipmentDetails(equipmentId).then(equipment => {
        if (equipment) {
            const availabilitySpan = document.getElementById(`availability-${equipmentId}`);
            if (availabilitySpan) {
                availabilitySpan.textContent = `${equipment.available_quantity}/${equipment.total_quantity}`;
                
                // Update color based on availability
                if (equipment.available_quantity === 0) {
                    availabilitySpan.className = 'badge badge-danger';
                } else if (equipment.available_quantity <= 5) {
                    availabilitySpan.className = 'badge badge-warning';
                } else {
                    availabilitySpan.className = 'badge badge-success';
                }
            }
        }
    });
}

// Populate edit form
function populateEditForm(data, formId) {
    const form = document.getElementById(formId);
    if (form) {
        Object.keys(data).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = data[key];
            }
        });
    }
}

// Toggle sidebar on mobile
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }
}

// Print report
function printReport() {
    window.print();
}

// Export table to CSV
function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        cols.forEach(col => {
            csvRow.push(col.textContent.trim());
        });
        csv.push(csvRow.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}
