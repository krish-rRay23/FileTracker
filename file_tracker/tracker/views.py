from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.uploaded_by = request.user
            file.save()
            FileHolder.objects.create(file=file, current_holder=request.user)
            return redirect('file_list')
    else:
        form = FileForm()
    return render(request, 'tracker/upload_file.html', {'form': form})

@login_required
def pass_file(request, file_id):
    file = File.objects.get(id=file_id)
    if request.method == 'POST':
        form = PassFileForm(request.POST)
        if form.is_valid():
            passed_to = form.cleaned_data['passed_to']
            FileLog.objects.create(file=file, passed_from=request.user, passed_to=passed_to)
            file_holder = FileHolder.objects.get(file=file)
            file_holder.current_holder = passed_to
            file_holder.save()
            return redirect('file_list')
    else:
        form = PassFileForm()
    return render(request, 'tracker/pass_file.html', {'form': form, 'file': file})

@login_required
def file_list(request):
    files = File.objects.filter(uploaded_by=request.user)
    return render(request, 'tracker/file_list.html', {'files': files})

@login_required
def file_log(request, file_id):
    logs = FileLog.objects.filter(file_id=file_id)
    return render(request, 'tracker/file_log.html', {'logs': logs})


def file_detail(request, file_id):
    file = get_object_or_404(File, id=file_id)
    comments = file.comments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.file = file
            comment.user = request.user
            comment.save()
            return redirect('file_detail', file_id=file.id)
    else:
        form = CommentForm()
    
    return render(request, 'tracker/file_detail.html', {'file': file, 'comments': comments, 'form': form})

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('upload_file')  # Redirect to the upload file page after submitting the comment
    else:
        form = CommentForm()
    return render(request, 'upload_file.html', {'form': form})