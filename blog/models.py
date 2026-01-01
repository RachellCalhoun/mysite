import html
import re

from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import slugify
from tinymce import models as tinymce_models


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    text = tinymce_models.HTMLField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    img = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_excerpt(self, length=160):
        """Return plain text excerpt for meta descriptions and previews."""
        text = strip_tags(self.text)
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > length:
            text = text[:length].rsplit(' ', 1)[0] + '...'
        return text

    def get_first_image(self):
        """Extract first image URL from post content for social sharing."""
        match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', self.text)
        return match.group(1) if match else None

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = tinymce_models.HTMLField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


# Create your models here.
