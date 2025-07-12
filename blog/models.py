from enum import unique

from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        PENDING= 'pending', 'Pending'
    title = models.CharField(max_length=200 , default="")
    slug = models.SlugField(unique=True, blank=True )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post' , default=1)
    body = models.TextField(default="hi")
    published = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    image=models.ImageField(upload_to='blog_images/', null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title
    def save(self,  *args, **kwargs):
        if not self.slug or self.slug.strip()  == "":
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while Post.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists() :
                unique_slug=f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args,**kwargs)
class Comment(models.Model):
    post = models.ForeignKey('Post',  related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'comment by {self.author.username} on {self.created_at}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100 , blank=True)
    phone = models.CharField(max_length=20 , blank=True)
    address= models.TextField(blank=True)
    profile_image= models.ImageField(upload_to='profile_images/',blank=True, null=True)

    def __str__(self):
        return f'profile{self.user.username}'
@receiver(post_save , sender=User)
def create_or_update_user_profile(sender, instance , created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)
