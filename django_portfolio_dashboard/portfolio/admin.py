from django.contrib import admin
from .models import Skill, Project, ProjectTag, BlogPost

admin.site.site_header = "DataSphere Portfolio Dashboard"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Manage Your Portfolio Content"

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_class']
    search_fields = ['name']

@admin.register(ProjectTag)
class ProjectTagAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    list_editable = ['order']
    filter_horizontal = ['tags']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'category', 'likes']
    list_filter = ['category', 'date']
    search_fields = ['title']