"""Global context processors — data available in every template."""


def global_context(request):
    unread_notifications = 0
    if request.user.is_authenticated:
        try:
            from accounts.models import Notification
            unread_notifications = Notification.objects.filter(
                user=request.user, is_read=False
            ).count()
        except Exception:
            pass
    return {
        'unread_notifications': unread_notifications,
    }
