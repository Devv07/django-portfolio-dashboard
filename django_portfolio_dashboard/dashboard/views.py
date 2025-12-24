import json
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .forms import BlogPostForm, ExperienceForm, ProjectForm, PortfolioSettingsForm
from .models import BlogPost, Experience, Project, PortfolioSettings
from collections import defaultdict, OrderedDict
from django.db.models.functions import TruncDate


@login_required
def dashboard(request):
    # At the top of each view function
    settings, created = PortfolioSettings.objects.get_or_create(user=request.user)
    # Real counts
    total_blog_posts = BlogPost.objects.count()
    total_projects = Project.objects.count()
    total_views = BlogPost.objects.aggregate(total=Sum('views'))['total'] or 0

    # ========== REAL CHANGE CALCULATIONS ==========
    # Last month vs current month
    one_month_ago = timezone.now() - timedelta(days=30)
    two_months_ago = timezone.now() - timedelta(days=60)

    # Blog posts change - REAL
    prev_month_posts = BlogPost.objects.filter(created_at__gte=two_months_ago, created_at__lt=one_month_ago).count()
    curr_month_posts = BlogPost.objects.filter(created_at__gte=one_month_ago).count()
    if prev_month_posts > 0:
        blog_posts_change = round(((curr_month_posts - prev_month_posts) / prev_month_posts) * 100, 1)
    else:
        blog_posts_change = 100.0 if curr_month_posts > 0 else 0.0

    # Projects change - REAL
    prev_month_projects = Project.objects.filter(created_at__gte=two_months_ago, created_at__lt=one_month_ago).count()
    curr_month_projects = Project.objects.filter(created_at__gte=one_month_ago).count()
    if prev_month_projects > 0:
        projects_change = round(((curr_month_projects - prev_month_projects) / prev_month_projects) * 100, 1)
    else:
        projects_change = 100.0 if curr_month_projects > 0 else 0.0

    # Views change - REAL
    prev_month_views = BlogPost.objects.filter(created_at__gte=two_months_ago, created_at__lt=one_month_ago).aggregate(total=Sum('views'))['total'] or 0
    curr_month_views = BlogPost.objects.filter(created_at__gte=one_month_ago).aggregate(total=Sum('views'))['total'] or 0
    if prev_month_views > 0:
        views_change = round(((curr_month_views - prev_month_views) / prev_month_views) * 100, 1)
    else:
        views_change = 100.0 if curr_month_views > 0 else 0.0

    # ========== REAL ENGAGEMENT RATE ==========
    if total_blog_posts > 0 and total_views > 0:
        # Real engagement: (total views / total posts) as percentage (normalized)
        engagement_rate = round((total_views / total_blog_posts) / 10, 1)  # Scale to realistic %
        
        # Real engagement change
        prev_month_engagement_posts = BlogPost.objects.filter(created_at__gte=two_months_ago, created_at__lt=one_month_ago).count()
        prev_month_engagement_views = BlogPost.objects.filter(created_at__gte=two_months_ago, created_at__lt=one_month_ago).aggregate(total=Sum('views'))['total'] or 0
        if prev_month_engagement_posts > 0 and prev_month_engagement_views > 0:
            prev_engagement = (prev_month_engagement_views / prev_month_engagement_posts) / 10
            curr_engagement = (curr_month_views / curr_month_posts) / 10 if curr_month_posts > 0 else 0
            engagement_change = round(((curr_engagement - prev_engagement) / prev_engagement * 100), 1) if prev_engagement > 0 else 0.0
        else:
            engagement_change = 0.0
    else:
        engagement_rate = 0.0
        engagement_change = 0.0

    # Rest of your code (top_posts, tags, charts - already real)...
    top_posts = BlogPost.objects.order_by('-views')[:3]

    # Popular tags - real
    tag_counts = {}
    for post in BlogPost.objects.all():
        if post.tags:
            for tag in [t.strip() for t in post.tags.split(',')]:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
    popular_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    popular_tags = [{'name': name, 'count': count} for name, count in popular_tags]

    # Content Distribution - real categories
    category_counts = BlogPost.objects.values('category').annotate(count=Count('id'))
    content_distribution_data = {
        'labels': [c['category'].capitalize() for c in category_counts],
        'values': [c['count'] for c in category_counts],
    }

    # Blog Performance - real views by day
    def get_performance_data(days):
        end = timezone.now()
        start = end - timedelta(days=days)

        dates = OrderedDict()
        current = start.date()
        while current <= end.date():
            key = current.strftime('%b %d' if days <= 31 else '%b %Y')
            dates[key] = 0
            current += timedelta(days=1)

        view_data = (
            BlogPost.objects
            .filter(created_at__gte=start)
            .annotate(day=TruncDate('created_at'))   # ✅ returns DATE object
            .values('day')
            .annotate(views=Sum('views'))
        )

        for item in view_data:
            day_obj = item['day']                    # ✅ this is DATE
            day_str = day_obj.strftime('%b %d' if days <= 31 else '%b %Y')
            dates[day_str] = item['views']

        return {
            'labels': list(dates.keys()),
            'data': list(dates.values())
        }

    blog_performance_data = {
        'week': get_performance_data(7),
        'month': get_performance_data(30),
        'year': get_performance_data(365),
    }

    context = {
        'total_blog_posts': total_blog_posts,
        'total_projects': total_projects,
        'total_views': total_views,
        'blog_posts_change': blog_posts_change,
        'projects_change': projects_change,
        'views_change': views_change,
        'engagement_rate': engagement_rate,
        'engagement_change': engagement_change,
        'top_posts': top_posts,
        'popular_tags': popular_tags,
        'blog_performance_data': json.dumps(blog_performance_data),
        'content_distribution_data': json.dumps(content_distribution_data),
    }
    return render(request, 'dashboard/dashboard.html', context)

# views.py
@login_required
def upload_content(request, tab='blog'):
    settings, created = PortfolioSettings.objects.get_or_create(user=request.user)

    blog_form = BlogPostForm()
    project_form = ProjectForm()

    if request.method == 'POST':
        action = request.POST.get('action')  # 'publish' or 'draft'

        # Check which form was submitted by looking for form-specific fields
        if 'title' in request.POST and 'content' in request.POST:  # Blog fields
            blog_form = BlogPostForm(request.POST, request.FILES)
            if blog_form.is_valid():
                post = blog_form.save(commit=False)
                post.author = request.user
                post.status = 'published' if action == 'publish' else 'draft'
                post.save()
                messages.success(request, f'Blog post "{post.title}" { "published" if action == "publish" else "saved as draft" }!')
                return redirect('dashboard:upload_content', tab='blog')
            else:
                messages.error(request, "Please correct the errors in the blog form.")

        elif 'title' in request.POST and 'description' in request.POST:  # Project fields
            project_form = ProjectForm(request.POST, request.FILES)
            if project_form.is_valid():
                project = project_form.save(commit=False)
                project.author = request.user
                project.status = 'published' if action == 'publish' else 'draft'
                project.save()
                messages.success(request, f'Project "{project.title}" { "published" if action == "publish" else "saved as draft" }!')
                return redirect('dashboard:upload_content', tab='project')
            else:
                messages.error(request, "Please correct the errors in the project form.")

        tab = 'project' if 'description' in request.POST else 'blog'  # Keep active tab

    context = {
        'settings': settings,
        'active_menu': 'upload',
        'blog_form': blog_form,
        'project_form': project_form,
        'active_tab': tab,
    }
    return render(request, 'dashboard/upload_content.html', context)

@login_required
def manage_projects(request):
    settings, created = PortfolioSettings.objects.get_or_create(user=request.user)
    
    # Show ALL projects
    project_list = Project.objects.all().order_by('-created_at')
    
    paginator = Paginator(project_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'settings': settings,
        'active_menu': 'projects',
        'projects': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'dashboard/projects_list.html', context)

@login_required
def manage_blog_posts(request):
    settings, created = PortfolioSettings.objects.get_or_create(user=request.user)
    
    # This line shows ALL posts (published + draft)
    blog_posts = BlogPost.objects.all().order_by('-created_at')
    
    paginator = Paginator(blog_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'settings': settings,
        'active_menu': 'blog',
        'blog_posts': page_obj,  # This sends posts to template
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'dashboard/blog_list.html', context)

@login_required
def create_blog_post(request):
    # At the top of each view function
    settings, created = PortfolioSettings.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Blog post published successfully!')
            return redirect('manage_blog_posts')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogPostForm()

    return render(request, 'dashboard/blog_form.html', {'form': form, 'title': 'Create New Blog Post'})

@login_required
def edit_blog_post(request, pk):

    # At the top of each view function
    settings, created = PortfolioSettings.objects.get_or_create(user=request.user)
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('manage_blog_posts')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'dashboard/blog_form.html', {
        'form': form,
        'title': 'Edit Blog Post',
        'post': post
    })

@login_required
def delete_blog_post(request, pk):
    # At the top of each view function
    settings, created = PortfolioSettings.objects.get_or_create(user=request.user)
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('manage_blog_posts')
    return render(request, 'dashboard/blog_confirm_delete.html', {'post': post})

def blog_detail(request, slug):
    # At the top of each view function
    settings, created = PortfolioSettings.objects.get_or_create(user=request.user)
    post = get_object_or_404(BlogPost, slug=slug)
    post.views = F('views') + 1
    post.save(update_fields=['views'])
    post.refresh_from_db()
    return render(request, 'dashboard/blog_detail.html', {'post': post})


@login_required
def blog_analytics(request):

    # At the top of each view function
    settings, created = PortfolioSettings.objects.get_or_create(user=request.user)
    # Real Category Distribution
    categories = BlogPost.objects.values('category').annotate(count=Count('id')).order_by('-count')
    categories_chart_data = {
        'labels': [cat['category'].capitalize() for cat in categories[:5]] or ['No posts yet'],
        'values': [cat['count'] for cat in categories[:5]] or [0],
    }

    # Real Total Stats
    total_posts = BlogPost.objects.count()
    total_views = BlogPost.objects.aggregate(total=Sum('views'))['total'] or 0
    published_posts = BlogPost.objects.filter(status='published').count()

    # Real Engagement Data by Period
    def get_period_data(days):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Group posts by day
        daily_stats = defaultdict(lambda: {'views': 0, 'posts': 0})
        
        posts = BlogPost.objects.filter(created_at__gte=start_date)
        for post in posts:
            day_str = post.created_at.strftime('%b %d')
            daily_stats[day_str]['posts'] += 1
            daily_stats[day_str]['views'] += post.views
        
        # Create ordered labels (last N days)
        labels = []
        views_list = []
        posts_list = []
        
        current_date = start_date.date()
        for i in range(days):
            day_str = (current_date + timedelta(days=i)).strftime('%b %d')
            stats = daily_stats[day_str]
            labels.append(day_str)
            views_list.append(stats['views'])
            posts_list.append(stats['posts'])
        
        return {
            'labels': labels,
            'views': views_list,
            'posts': posts_list
        }

    # Generate data for all periods
    engagement_chart_data = {
        'week': get_period_data(7),
        'month': get_period_data(30),
        'quarter': get_period_data(90),
    }

    # Real Insights
    if total_posts > 0:
        avg_views = round(total_views / total_posts, 1)
        top_post = BlogPost.objects.order_by('-views').first()
        top_category_obj = categories.first() if categories else None
    else:
        avg_views = 0
        top_post = None
        top_category_obj = None

    insights = {
        'total_posts': total_posts,
        'total_views': total_views,
        'published_posts': published_posts,
        'avg_views_per_post': avg_views,
        'top_category': top_category_obj['category'].capitalize() if top_category_obj else 'None',
        'top_post_title': top_post.title[:30] + '...' if top_post else 'None',
        'top_post_views': top_post.views if top_post else 0,
    }

    context = {
        'engagement_chart_data': json.dumps(engagement_chart_data),
        'categories_chart_data': json.dumps(categories_chart_data),
        'insights': insights,
    }
    return render(request, 'dashboard/analytics.html', context)

@login_required
def portfolio_settings(request):
    settings, created = PortfolioSettings.objects.get_or_create(user=request.user)
    experiences = Experience.objects.filter(user=request.user).order_by('-start_date')

    if request.method == 'POST':
        action = request.POST.get('action')

        # Save main settings
        if action == 'save':
            form = PortfolioSettingsForm(request.POST, request.FILES, instance=settings)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile settings saved successfully!")
                return redirect('dashboard:portfolio_settings')
            else:
                messages.error(request, "Please fix the errors in the form.")

        # Add new experience
        elif action == 'add_experience':
            exp_form = ExperienceForm(request.POST)
            if exp_form.is_valid():
                exp = exp_form.save(commit=False)
                exp.user = request.user
                exp.save()
                messages.success(request, "Experience added successfully!")
                return redirect('dashboard:portfolio_settings')
            else:
                messages.error(request, "Please fix errors in experience form.")

        # Delete experience
        elif action == 'delete_experience':
            exp_id = request.POST.get('exp_id')
            if exp_id:
                exp = get_object_or_404(Experience, id=exp_id, user=request.user)
                exp.delete()
                messages.success(request, "Experience deleted.")
            return redirect('dashboard:portfolio_settings')

        # Reset settings
        elif action == 'reset':
            settings.profile_picture = None
            settings.first_name = ""
            settings.last_name = ""
            settings.professional_title = "Data Analyst"
            settings.bio = ""
            settings.skills = ""
            settings.location = ""
            settings.contact_email = ""
            settings.contact_phone = ""
            settings.github_link = ""
            settings.linkedin_link = ""
            settings.twitter_link = ""
            settings.instagram_link = ""
            settings.theme_color = "#4361ee"
            settings.save()
            messages.success(request, "Settings reset to default!")
            return redirect('dashboard:portfolio_settings')

    else:
        form = PortfolioSettingsForm(instance=settings)
        exp_form = ExperienceForm()

    context = {
        'form': form,
        'exp_form': exp_form,
        'settings': settings,
        'experiences': experiences,
        'active_menu': 'settings',
    }
    return render(request, 'dashboard/settings.html', context)


@login_required
def profile_view(request):
    settings, created = PortfolioSettings.objects.get_or_create(user=request.user)
    experiences = Experience.objects.filter(user=request.user).order_by('-start_date')

    context = {
        'settings': settings,
        'experiences': experiences,
        'active_menu': 'profile',
    }
    return render(request, 'dashboard/profile_view.html', context)