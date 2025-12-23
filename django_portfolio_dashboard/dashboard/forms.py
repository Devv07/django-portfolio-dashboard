from django import forms
from .models import BlogPost, Experience, Project, PortfolioSettings

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

class PortfolioSettingsForm(forms.ModelForm):
    class Meta:
        model = PortfolioSettings
        fields = [
            'profile_picture', 'first_name', 'last_name',
            'portfolio_title', 'bio', 'skills',
            'contact_email', 'contact_phone',
            'location',
            'github_link', 'linkedin_link', 'twitter_link', 'instagram_link',
            'theme_color'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kathmandu, Nepal'}),
            'portfolio_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'My Data Portfolio'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'I am a passionate data analyst...'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_skills', 'placeholder': 'Python, SQL, Tableau...'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/username'}),
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'}),
            'twitter_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/username'}),
            'instagram_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/username'}),
            'theme_color': forms.RadioSelect(),
            'profile_picture': forms.FileInput(attrs={'accept': 'image/*'}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['position', 'company', 'level', 'start_date', 'end_date', 'current', 'description']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }