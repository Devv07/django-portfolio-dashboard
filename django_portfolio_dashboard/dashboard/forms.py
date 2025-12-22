from django import forms
from .models import BlogPost, Project, PortfolioSettings

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'content', 'tags', 'featured_image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter blog title', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your blog content here...', 'rows': 8, 'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, Data Science', 'class': 'form-control'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Blog title is required.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or len(content.strip()) < 10:
            raise forms.ValidationError("Blog content must be at least 10 characters.")
        return content

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'project_type', 'description', 'tools', 'image', 'live_link', 'code_link']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter project title', 'class': 'form-control'}),
            'project_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your project...', 'rows': 6, 'class': 'form-control'}),
            'tools': forms.TextInput(attrs={'placeholder': 'e.g. Python, Tableau, SQL', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'live_link': forms.URLInput(attrs={'placeholder': 'https://your-project.com', 'class': 'form-control'}),
            'code_link': forms.URLInput(attrs={'placeholder': 'https://github.com/your-repo', 'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Project title is required.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description or len(description.strip()) < 10:
            raise forms.ValidationError("Description must be at least 10 characters.")
        return description

# dashboard/forms.py
class PortfolioSettingsForm(forms.ModelForm):
    class Meta:
        model = PortfolioSettings
        fields = [
            'portfolio_title', 'portfolio_description',
            'contact_email', 'contact_phone',
            'github_link', 'linkedin_link', 'twitter_link',
            'theme_color'
        ]
        widgets = {
            'portfolio_title': forms.TextInput(attrs={'class': 'form-control'}),
            'portfolio_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/username'}),
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'}),
            'twitter_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/username'}),
            'theme_color': forms.RadioSelect(),
        }