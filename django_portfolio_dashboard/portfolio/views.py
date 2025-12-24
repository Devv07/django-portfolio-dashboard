from django.shortcuts import render
from .models import Project, BlogPost, Skill

def home(request):
    projects = Project.objects.all()
    blog_posts = BlogPost.objects.all()[:3]  # Latest 3 posts
    skills = Skill.objects.all()
    context = {
        'projects': projects,
        'blog_posts': blog_posts,
        'skills': skills,
    }
    return render(request, 'portfolio/index.html', context)