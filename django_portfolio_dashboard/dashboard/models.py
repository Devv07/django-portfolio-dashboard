# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('tutorial', 'Tutorial'),
        ('analysis', 'Analysis'),
        ('tools', 'Tools'),
        ('case-study', 'Case Study'),
        ('trends', 'Trends'),
    ])
    tags = models.CharField(max_length=300, blank=True)
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('scheduled', 'Scheduled'),
    ], default='draft')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True) 

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-set published_date when status becomes 'published'
        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    project_type = models.CharField(max_length=50, choices=[
        ('dashboard', 'Dashboard'),
        ('analysis', 'Data Analysis'),
        ('visualization', 'Data Visualization'),
        ('machine-learning', 'Machine Learning'),
        ('business-intelligence', 'Business Intelligence'),
    ])
    tools = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    live_link = models.URLField(blank=True)
    code_link = models.URLField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    # dashboard/models.py
class PortfolioSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    portfolio_title = models.CharField(max_length=100, default="My Data Portfolio")
    portfolio_description = models.TextField(max_length=500, default="Welcome to my data analysis portfolio.")
    
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    
    theme_color = models.CharField(
        max_length=7,
        choices=[
            ('#4361ee', 'Blue'),
            ('#3a0ca3', 'Purple'),
            ('#f72585', 'Pink'),
            ('#06d6a0', 'Teal'),
            ('#1a1a2e', 'Dark Navy'),
        ],
        default='#4361ee'
    )

    def __str__(self):
        return f"{self.user.username}'s Settings"
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    icon = models.CharField(max_length=50, default='info-circle')  # fa-icon name
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    