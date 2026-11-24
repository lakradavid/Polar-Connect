from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DiscussionForum, Discussion, Comment


def forum_home(request):
    forums = DiscussionForum.objects.all()
    recent = Discussion.objects.select_related('author', 'forum').order_by('-created_at')[:10]
    return render(request, 'community/forum.html', {'forums': forums, 'recent': recent})


def forum_detail(request, slug):
    forum = get_object_or_404(DiscussionForum, slug=slug)
    discussions = Discussion.objects.filter(forum=forum).order_by('-created_at')
    return render(request, 'community/forum_detail.html', {'forum': forum, 'discussions': discussions})


def discussion_detail(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    discussion.view_count += 1
    discussion.save(update_fields=['view_count'])
    comments = discussion.comments.all()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to reply.')
            return redirect('accounts:login')
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(discussion=discussion, author=request.user, content=content)
            messages.success(request, 'Reply posted.')
            return redirect('community:discussion', pk=pk)
    return render(request, 'community/discussion.html', {
        'discussion': discussion,
        'comments': comments,
    })


@login_required
def new_discussion(request):
    forums = DiscussionForum.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        forum_id = request.POST.get('forum', '')
        if not title or not content or not forum_id:
            messages.error(request, 'All fields are required.')
            return render(request, 'community/new_discussion.html', {'forums': forums})
        forum = get_object_or_404(DiscussionForum, pk=forum_id)
        disc = Discussion.objects.create(
            forum=forum,
            author=request.user,
            title=title,
            content=content,
            is_question=bool(request.POST.get('is_question')),
        )
        messages.success(request, 'Discussion started.')
        return redirect('community:discussion', pk=disc.pk)
    return render(request, 'community/new_discussion.html', {'forums': forums})
