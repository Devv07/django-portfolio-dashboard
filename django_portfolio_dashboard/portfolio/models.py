from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100, help_text="e.g. fab fa-python")  # Font Awesome class

    def __str__(self):
        return self.name

class ProjectTag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.URLField()  # Use Unsplash URLs or upload later
    live_link = models.URLField(blank=True, null=True)
    code_link = models.URLField(blank=True, null=True)
    case_link = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(ProjectTag, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, default="Tutorial")
    date = models.DateField()
    read_time = models.CharField(max_length=20, default="8 min read")
    excerpt = models.TextField()
    image = models.URLField()
    likes = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title