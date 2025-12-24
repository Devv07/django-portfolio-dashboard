// DOM Elements
const sidebar = document.getElementById('sidebar');
const mobileToggle = document.getElementById('mobileToggle');
const tabButtons = document.querySelectorAll('.tab-btn');
const uploadForms = document.querySelectorAll('.upload-form');

// Mobile Toggle Sidebar
mobileToggle.addEventListener('click', (e) => {
    e.stopPropagation();
    sidebar.classList.toggle('active');
});

// Close sidebar when clicking outside on mobile
document.addEventListener('click', (e) => {
    if (window.innerWidth <= 992) {
        if (!sidebar.contains(e.target) && !mobileToggle.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    }
});

// Switch between upload tabs
tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all tabs
        tabButtons.forEach(btn => btn.classList.remove('active'));
        
        // Add active class to clicked tab
        button.classList.add('active');
        
        // Get form to show
        const formId = button.getAttribute('data-form');
        
        // Hide all forms
        uploadForms.forEach(form => form.classList.remove('active'));
        
        // Show selected form
        document.getElementById(formId).classList.add('active');
    });
});

// File upload click handlers
document.querySelectorAll('.file-upload').forEach(container => {
    const input = container.querySelector('input[type="file"]');
    if (input) {
        container.addEventListener('click', (e) => {
            // Prevent click if on remove button or tag
            if (!e.target.closest('.tag-remove')) {
                input.click();
            }
        });
        
        input.addEventListener('change', () => {
            if (input.files.length > 0) {
                container.querySelector('p').textContent = input.files[0].name;
            } else {
                container.querySelector('p').textContent = 'Click to upload or drag and drop';
            }
        });
    }
});

// Generic tag input handler
function setupTagInput(inputId, containerId) {
    const input = document.getElementById(inputId);
    const container = document.getElementById(containerId);
    
    if (!input || !container) return;
    
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault();
            const value = input.value.trim();
            if (value) {
                addTag(value, container, input);
            }
        }
    });
    
    input.addEventListener('blur', () => {
        const value = input.value.trim();
        if (value) {
            addTag(value, container, input);
        }
    });
}

// Function to add a tag
function addTag(text, container, input) {
    // Avoid duplicates
    const existing = Array.from(container.querySelectorAll('.tag-text')).some(el => el.textContent.trim() === text);
    if (existing) {
        input.value = '';
        return;
    }
    
    const tag = document.createElement('div');
    tag.className = 'tag';
    tag.innerHTML = `
        <span class="tag-text">${text}</span>
        <button type="button" class="tag-remove" aria-label="Remove tag">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    tag.querySelector('.tag-remove').addEventListener('click', () => {
        tag.remove();
        updateHiddenInput(container, input);
    });
    
    container.appendChild(tag);
    input.value = '';
    updateHiddenInput(container, input);
}

// Update hidden input with comma-separated tags (for form submission)
function updateHiddenInput(container, originalInput) {
    const tags = Array.from(container.querySelectorAll('.tag-text')).map(el => el.textContent.trim()).join(',');
    originalInput.value = tags;  // Assuming originalInput has name for submission
}

// Setup for blog tags
setupTagInput('blogTags', 'blogTagsContainer');

// Setup for project tools
setupTagInput('projectTools', 'projectToolsContainer');

// No form submission alerts - let Django handle it (remove preventDefault)
// Remove the alert-based submission handlers - forms submit normally to server

// Chart Period Toggle (if charts exist)
const chartPeriodButtons = document.querySelectorAll('.chart-btn');
if (chartPeriodButtons.length > 0) {
    chartPeriodButtons.forEach(button => {
        button.addEventListener('click', function() {
            chartPeriodButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            // Real apps would fetch new data here via AJAX
            console.log('Switch to period:', this.dataset.period);
        });
    });
}

// Table action buttons (placeholder alerts)
document.querySelectorAll('.action-btn.edit').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        alert('Edit functionality coming soon!');
    });
});

document.querySelectorAll('.action-btn.delete').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        if (confirm('Are you sure you want to delete this item?')) {
            alert('Delete functionality coming soon!');
        }
    });
});

document.querySelectorAll('.action-btn.view').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        alert('View in new tab coming soon!');
    });
});

// Notification Dropdown (if elements exist)
const notificationBtn = document.getElementById('notificationBtn');
const notificationDropdown = document.getElementById('notificationDropdown');
if (notificationBtn && notificationDropdown) {
    notificationBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        notificationDropdown.classList.toggle('active');
    });

    document.addEventListener('click', () => {
        notificationDropdown.classList.remove('active');
    });

    const markAllRead = document.getElementById('markAllRead');
    if (markAllRead) {
        markAllRead.addEventListener('click', () => {
            alert('Mark all as read coming soon!');
        });
    }
}


// Unified Tag Input for Skills, Blog Tags, and Project Tools
document.addEventListener('DOMContentLoaded', function() {
    // Generic function for any tag input
    function setupTagInput(inputId, containerId) {
        const input = document.getElementById(inputId);
        const container = document.getElementById(containerId);

        if (!input || !container) return;

        // Load existing tags on page load
        function loadExistingTags() {
            if (input.value.trim()) {
                const tags = input.value.split(',')
                    .map(t => t.trim())
                    .filter(t => t.length > 0);
                tags.forEach(tag => createTag(tag));
                input.value = ''; // Clear input after loading
            }
        }

        // Create a tag element
        function createTag(text) {
            text = text.trim();
            if (!text) return;

            // Prevent duplicates
            const exists = Array.from(container.querySelectorAll('.tag span'))
                .some(span => span.textContent.trim().toLowerCase() === text.toLowerCase());
            if (exists) return;

            const tag = document.createElement('div');
            tag.className = 'tag';
            tag.innerHTML = `
                <span>${text}</span>
                <button type="button" class="tag-remove"><i class="fas fa-times"></i></button>
            `;

            tag.querySelector('.tag-remove').addEventListener('click', () => {
                tag.remove();
                updateHiddenInput();
            });

            container.appendChild(tag);
            updateHiddenInput();
        }

        // Update the hidden/original input with current tags
        function updateHiddenInput() {
            const currentTags = Array.from(container.querySelectorAll('.tag span'))
                .map(span => span.textContent.trim())
                .join(',');
            input.value = currentTags;
        }

        // Add tag on Enter
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Prevent form submit
                const value = input.value.trim();
                if (value) {
                    createTag(value);
                    input.value = ''; // Clear input
                    input.focus(); // Focus back for next tag
                }
            }
        });

        // Add tag on blur (click outside)
        input.addEventListener('blur', function() {
            const value = input.value.trim();
            if (value) {
                createTag(value);
                input.value = ''; // Clear input
            }
        });

        // Load existing on start
        loadExistingTags();
    }

    // Initialize for all 3 fields
    setupTagInput('id_skills', 'skillsContainer');           // Settings Skills
    setupTagInput('id_tags', 'blogTagsContainer');           // Blog Tags
    setupTagInput('id_tools', 'projectToolsContainer');     // Project Tools
});