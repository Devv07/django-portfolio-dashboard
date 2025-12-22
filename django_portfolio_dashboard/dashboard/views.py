from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def dashboard(request):
    context = {
        'total_blog_posts': 24,
        'total_projects': 16,
        'total_views': 5842,
        'engagement_rate': 4.8,
        'top_posts': [
            {'title': 'Building Interactive Dashboards', 'category': 'Tutorial', 'views': 1245},
            {'title': 'Impact of Inflation Analysis', 'category': 'Analysis', 'views': 982},
            {'title': 'Data Visualization Tools 2023', 'category': 'Tools', 'views': 756},
        ],
        'popular_tags': [
            {'name': 'Python', 'count': 12},
            {'name': 'Data Visualization', 'count': 9},
            {'name': 'Machine Learning', 'count': 7},
            {'name': 'Tutorial', 'count': 6},
        ],
        'unread_notifications': 3,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def upload_content(request):
    if request.method == 'POST':
        # Handle form submission
        messages.success(request, 'Content uploaded successfully!')
        return redirect('upload_content')
    
    context = {
        'unread_notifications': 3,
    }
    return render(request, 'dashboard/upload.html', context)

@login_required
def manage_projects(request):
    context = {
        'projects': [
            {
                'title': 'Sales Performance Dashboard',
                'description': 'Interactive sales tracking dashboard',
                'type': 'Dashboard',
                'tools': ['Power BI', 'SQL'],
                'views': 1245,
                'status': 'published',
                'date': 'May 15, 2023'
            },
            # Add more projects...
        ],
        'unread_notifications': 3,
    }
    return render(request, 'dashboard/project.html', context)

@login_required
def manage_blog(request):
    context = {
        'blog_posts': [
            {
                'title': 'Building Interactive Dashboards with Python',
                'description': 'Learn how to create interactive business dashboards',
                'category': 'Tutorial',
                'views': 1245,
                'likes': 124,
                'comments': 28,
                'status': 'published',
                'date': 'May 15, 2023'
            },
            # Add more posts...
        ],
        'unread_notifications': 3,
    }
    return render(request, 'dashboard/blogs.html', context)

@login_required
def analytics(request):
    context = {
        'unread_notifications': 3,
    }
    return render(request, 'dashboard/analytics.html', context)

@login_required
def settings(request):
    if request.method == 'POST':
        # Handle settings update
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
    
    context = {
        'unread_notifications': 3,
    }
    return render(request, 'dashboard/settings.html', context)