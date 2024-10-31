from django.db import models
from django.utils import timezone
from tinymce import models as tinymce_models

class Project(models.Model):
	title = models.CharField(max_length = 200)
	published_date = models.DateTimeField(blank=True, null=True)
	link = models.URLField(max_length = 200,null=True, blank=True)
	img = models.ImageField(null=True, blank=True)
	text = tinymce_models.HTMLField()
	def __str__(self):
		return self.title

class Skill(models.Model):
	title = models.CharField(max_length=20)
	link = models.CharField(max_length = 200,null=True, blank=True)
	img = models.ImageField(null=True, blank=True)
	text = tinymce_models.HTMLField()

	def __str__(self):
		return self.title
