from django.shortcuts import render
from .models import Project, Skill
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect


def projects(request):
	entries = Project.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	skills = Skill.objects.all()
	return render(request, 'projects/home.html',{'entries': entries, 'skills': skills})

