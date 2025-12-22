// DOM Elements
const sidebar = document.getElementById('sidebar');
const mobileToggle = document.getElementById('mobileToggle');
const tabButtons = document.querySelectorAll('.tab-btn');
const uploadForms = document.querySelectorAll('.upload-form');
const chartPeriodButtons = document.querySelectorAll('.chart-btn');

// Mobile Toggle Sidebar
mobileToggle.addEventListener('click', () => {
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
        uploadForms.forEach(form => {
            form.classList.remove('active');
        });
        
        // Show selected form
        document.getElementById(formId).classList.add('active');
    });
});

// File upload click handlers
const blogImageUpload = document.getElementById('blogImageUpload');
if (blogImageUpload) {
    blogImageUpload.addEventListener('click', () => {
        document.getElementById('blogImage').click();
    });
}

const projectImageUpload = document.getElementById('projectImageUpload');
if (projectImageUpload) {
    projectImageUpload.addEventListener('click', () => {
        document.getElementById('projectImage').click();
    });
}

// Handle tag input for blog
const blogTagsInput = document.getElementById('blogTags');
const blogTagsContainer = document.getElementById('blogTagsContainer');
if (blogTagsInput && blogTagsContainer) {
    blogTagsInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault();
            const tag = blogTagsInput.value.trim();
            if (tag) {
                addTag(tag, blogTagsContainer);
                blogTagsInput.value = '';
            }
        }
    });
    // Initialize with some tags
    addTag('Python', blogTagsContainer);
    addTag('Data Visualization', blogTagsContainer);
    addTag('Tutorial', blogTagsContainer);
}

// Handle tools input for projects
const projectToolsInput = document.getElementById('projectTools');
const projectToolsContainer = document.getElementById('projectToolsContainer');
if (projectToolsInput && projectToolsContainer) {
    projectToolsInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault();
            const tool = projectToolsInput.value.trim();
            if (tool) {
                addTag(tool, projectToolsContainer);
                projectToolsInput.value = '';
            }
        }
    });
    // Initialize with some tags
    addTag('Power BI', projectToolsContainer);
    addTag('SQL', projectToolsContainer);
    addTag('DAX', projectToolsContainer);
}

// Function to add a tag
function addTag(text, container) {
    const tag = document.createElement('div');
    tag.className = 'tag';
    tag.innerHTML = `
        ${text}
        <button class="tag-remove">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add remove functionality
    const removeBtn = tag.querySelector('.tag-remove');
    removeBtn.addEventListener('click', () => {
        tag.remove();
    });
    
    container.appendChild(tag);
}

// Form submission handlers
const blogForm = document.getElementById('blogForm');
if (blogForm) {
    blogForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Blog post published successfully!');
        // In a real app, submit via AJAX or form action
    });
}

const projectForm = document.getElementById('projectForm');
if (projectForm) {
    projectForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Project published successfully!');
        // In a real app, submit via AJAX or form action
    });
}

const saveDraftBtn = document.getElementById('saveDraftBtn');
if (saveDraftBtn) {
    saveDraftBtn.addEventListener('click', () => {
        alert('Blog post saved as draft!');
    });
}

// Chart Period Toggle
chartPeriodButtons.forEach(button => {
    button.addEventListener('click', function() {
        chartPeriodButtons.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
        updateCharts(this.getAttribute('data-period'));
    });
});

// Initialize Charts
let blogPerformanceChart, contentDistributionChart, engagementChart, categoriesChart;

function initializeCharts() {
    // Blog Performance Chart
    const blogCtx = document.getElementById('blogPerformanceChart');
    if (blogCtx) {
        blogPerformanceChart = new Chart(blogCtx.getContext('2d'), {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Views',
                    data: [320, 450, 620, 580, 490, 720, 680],
                    borderColor: '#4361ee',
                    backgroundColor: 'rgba(67, 97, 238, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }, {
                    label: 'Likes',
                    data: [45, 62, 78, 65, 52, 85, 72],
                    borderColor: '#f72585',
                    backgroundColor: 'rgba(247, 37, 133, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            drawBorder: false
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
    
    // Content Distribution Chart
    const contentCtx = document.getElementById('contentDistributionChart');
    if (contentCtx) {
        contentDistributionChart = new Chart(contentCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Tutorials', 'Analysis', 'Tools', 'Case Studies', 'Trends'],
                datasets: [{
                    data: [35, 25, 20, 12, 8],
                    backgroundColor: [
                        '#4361ee',
                        '#f72585',
                        '#4cc9f0',
                        '#06d6a0',
                        '#ffd166'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                    }
                }
            }
        });
    }
    
    // Engagement Chart
    const engagementCtx = document.getElementById('engagementChart');
    if (engagementCtx) {
        engagementChart = new Chart(engagementCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Comments',
                    data: [12, 19, 8, 15, 10, 5, 14],
                    backgroundColor: '#4361ee',
                    borderRadius: 8
                }, {
                    label: 'Shares',
                    data: [8, 12, 5, 9, 7, 3, 10],
                    backgroundColor: '#f72585',
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            drawBorder: false
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
    
    // Categories Chart
    const categoriesCtx = document.getElementById('categoriesChart');
    if (categoriesCtx) {
        categoriesChart = new Chart(categoriesCtx.getContext('2d'), {
            type: 'polarArea',
            data: {
                labels: ['Tutorial', 'Analysis', 'Tools', 'Case Study'],
                datasets: [{
                    data: [1245, 982, 756, 543],
                    backgroundColor: [
                        'rgba(67, 97, 238, 0.7)',
                        'rgba(247, 37, 133, 0.7)',
                        'rgba(76, 201, 240, 0.7)',
                        'rgba(6, 214, 160, 0.7)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                    }
                }
            }
        });
    }
}

// Update charts based on period
function updateCharts(period) {
    // This would normally fetch new data from server based on period
    // For demo, we'll just log
    console.log(`Updating charts for period: ${period}`);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initializeCharts);

// Handle table action buttons
document.querySelectorAll('.action-btn.edit').forEach(button => {
    button.addEventListener('click', function() {
        alert('Edit functionality would open an edit form here.');
    });
});

document.querySelectorAll('.action-btn.delete').forEach(button => {
    button.addEventListener('click', function() {
        if (confirm('Are you sure you want to delete this item?')) {
            // In real app, would delete from server
            alert('Item deleted successfully!');
        }
    });
});

document.querySelectorAll('.action-btn.view').forEach(button => {
    button.addEventListener('click', function() {
        alert('View functionality would open the item in a new tab.');
    });
});