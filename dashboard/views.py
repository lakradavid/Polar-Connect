import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import CustomUser, Notification, Bookmark
from research.models import ResearchPublication
from repository.models import KnowledgeResource
from education.models import LearningProgress, QuizAttempt, LearningModule
from expeditions.models import Expedition
from media_gallery.models import MediaAsset
from news.models import NewsArticle, Event
from community.models import Discussion


@login_required
def dashboard_index(request):
    user = request.user

    # Learning progress
    completed_modules = LearningProgress.objects.filter(user=user, completed=True).count()
    total_modules = LearningModule.objects.filter(is_published=True).count()
    progress_pct = int((completed_modules / total_modules * 100)) if total_modules else 0

    # Quiz scores
    quiz_attempts = QuizAttempt.objects.filter(user=user).order_by('-attempted_at')[:5]
    best_score = max((a.percentage for a in QuizAttempt.objects.filter(user=user)), default=0)

    # Recent notifications  — compute unread BEFORE slicing
    notifications_qs = Notification.objects.filter(user=user).order_by('-created_at')
    unread_count = notifications_qs.filter(is_read=False).count()
    notifications = notifications_qs[:5]

    # Bookmarks
    bookmark_count = Bookmark.objects.filter(user=user).count()

    # Uploaded research (for researchers)
    my_research = ResearchPublication.objects.filter(uploaded_by=user).order_by('-created_at')[:3]

    # Recent discussions
    my_discussions = Discussion.objects.filter(author=user).order_by('-created_at')[:3]

    context = {
        'completed_modules': completed_modules,
        'total_modules': total_modules,
        'progress_pct': progress_pct,
        'quiz_attempts': quiz_attempts,
        'best_score': round(best_score, 1),
        'notifications': notifications,
        'unread_count': unread_count,
        'bookmark_count': bookmark_count,
        'my_research': my_research,
        'my_discussions': my_discussions,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def admin_dashboard(request):
    if not request.user.is_admin_role:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('dashboard:index')

    # Counts
    total_users        = CustomUser.objects.count()
    total_research     = ResearchPublication.objects.count()
    pending_research   = ResearchPublication.objects.filter(status='pending').count()
    total_resources    = KnowledgeResource.objects.count()
    total_media        = MediaAsset.objects.count()
    total_articles     = NewsArticle.objects.count()
    total_expeditions  = Expedition.objects.count()
    total_discussions  = Discussion.objects.count()

    # Chart data: users by category
    cat_labels, cat_counts = [], []
    for cat_val, cat_label in CustomUser.USER_CATEGORIES:
        count = CustomUser.objects.filter(user_category=cat_val).count()
        cat_labels.append(cat_label)
        cat_counts.append(count)

    # Chart data: research by category
    res_labels, res_counts = [], []
    for cat_val, cat_label in ResearchPublication._meta.get_field('category').choices:
        count = ResearchPublication.objects.filter(category=cat_val).count()
        if count:
            res_labels.append(cat_label)
            res_counts.append(count)

    # Recent items
    recent_users     = CustomUser.objects.order_by('-date_joined')[:8]
    recent_research  = ResearchPublication.objects.order_by('-created_at')[:8]
    pending_papers   = ResearchPublication.objects.filter(status='pending').order_by('-created_at')[:10]

    context = {
        'total_users': total_users,
        'total_research': total_research,
        'pending_research': pending_research,
        'total_resources': total_resources,
        'total_media': total_media,
        'total_articles': total_articles,
        'total_expeditions': total_expeditions,
        'total_discussions': total_discussions,
        'chart_user_labels': json.dumps(cat_labels),
        'chart_user_counts': json.dumps(cat_counts),
        'chart_res_labels':  json.dumps(res_labels),
        'chart_res_counts':  json.dumps(res_counts),
        'recent_users': recent_users,
        'recent_research': recent_research,
        'pending_papers': pending_papers,
    }
    return render(request, 'dashboard/admin.html', context)


@login_required
def notifications(request):
    if request.method == 'POST' and request.POST.get('mark_all_read'):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        messages.success(request, 'All notifications marked as read.')
        return redirect('dashboard:notifications')

    notif_list = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notif_list.filter(is_read=False).count()
    # Mark fetched ones as read
    notif_list.filter(is_read=False).update(is_read=True)

    return render(request, 'dashboard/notifications.html', {
        'notifications': notif_list,
        'unread_count': unread_count,
    })


@login_required
def bookmarks(request):
    bookmark_list = Bookmark.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/bookmarks.html', {'bookmarks': bookmark_list})
