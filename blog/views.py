import os
import uuid
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from PIL import Image

from .forms import PostForm
from .models import Post


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail_redirect(request, pk):
    """Redirect old pk-based URLs to new slug-based URLs."""
    post = get_object_or_404(Post, pk=pk)
    return redirect('post_detail', slug=post.slug, permanent=True)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if request.POST.get('action') == 'publish':
                post.published_date = timezone.now()
            post.save()
            if post.published_date:
                return redirect('post_detail', slug=post.slug)
            else:
                return redirect('post_draft_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if request.POST.get('action') == 'publish' and not post.published_date:
                post.published_date = timezone.now()
            post.save()
            if post.published_date:
                return redirect('post_detail', slug=post.slug)
            else:
                return redirect('post_draft_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', slug=post.slug)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


@login_required
@require_POST
def upload_image(request):

    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    uploaded_file = request.FILES['file']

    # Validate file size (10MB max per image)
    max_file_size = 10 * 1024 * 1024  # 10MB
    if uploaded_file.size > max_file_size:
        return JsonResponse({'error': 'File too large (max 10MB)'}, status=400)

    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if uploaded_file.content_type not in allowed_types:
        return JsonResponse({'error': 'Invalid file type'}, status=400)

    # Open and process image (validates it's a real image)
    try:
        img = Image.open(uploaded_file)
        img.verify()  # Verify it's a valid image
        uploaded_file.seek(0)  # Reset file pointer after verify
        img = Image.open(uploaded_file)  # Re-open after verify
    except Exception:
        return JsonResponse({'error': 'Invalid image file'}, status=400)

    # Skip compression for GIFs (animated)
    if uploaded_file.content_type == 'image/gif':
        if img.format != 'GIF':
            return JsonResponse({'error': 'Invalid GIF file'}, status=400)
        uploaded_file.seek(0)  # Reset for saving
        ext = '.gif'
        filename = f"blog_images/{uuid.uuid4().hex}{ext}"
        saved_path = default_storage.save(filename, uploaded_file)
    else:
        # Resize if larger than 1920px on longest side
        max_size = 1920
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size), Image.LANCZOS)

        # Convert to RGB if necessary (for JPEG)
        if img.mode in ('RGBA', 'P'):
            # Has transparency - save as PNG
            buffer = BytesIO()
            img.save(buffer, format='PNG', optimize=True)
            ext = '.png'
        else:
            # No transparency - save as JPEG
            if img.mode != 'RGB':
                img = img.convert('RGB')
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85, optimize=True)
            ext = '.jpg'

        buffer.seek(0)
        filename = f"blog_images/{uuid.uuid4().hex}{ext}"
        saved_path = default_storage.save(filename, ContentFile(buffer.read()))

    file_url = default_storage.url(saved_path)
    return JsonResponse({'location': file_url})
