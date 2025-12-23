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

    @property
    def tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []

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
    tools = models.CharField(max_length=500, blank=True, help_text="Comma-separated")
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    live_link = models.URLField(blank=True)
    code_link = models.URLField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def tools_list(self):
        if self.tools:
            return [tool.strip() for tool in self.tools.split(',') if tool.strip()]
        return []

    def __str__(self):
        return self.title
    
    # dashboard/models.py
class PortfolioSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Profile
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    portfolio_title = models.CharField(max_length=200, default="My Portfolio")
    bio = models.TextField(blank=True)

    # Skills (stored as comma-separated string)
    skills = models.CharField(max_length=500, blank=True, help_text="Comma-separated")
    location = models.CharField(max_length=100, blank=True)
    # Contact
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)

    # Social Links
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)

    # Theme
    theme_color = models.CharField(
        max_length=7,
        choices=[
            ('#4361ee', 'Blue'),
            ('#3a0ca3', 'Purple'),
            ('#f72585', 'Pink'),
            ('#06d6a0', 'Teal'),
            ('#1a1a2e', 'Navy'),
        ],
        default='#4361ee'
    )

    @property
    def skills_list(self):
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
        return []

    def __str__(self):
        return f"{self.user.username}'s Portfolio Settings"

# New Experience model
class Experience(models.Model):
    LEVEL_CHOICES = [
        ('intern', 'Intern'),
        ('junior', 'Junior'),
        ('mid', 'Mid-Level'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='junior')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False, help_text="Check if this is your current role")
    description = models.TextField()

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.position} at {self.company}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    icon = models.CharField(max_length=50, default='info-circle')  # fa-icon name
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    