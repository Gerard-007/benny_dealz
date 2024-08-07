from django import template
from apps.notifications.models import Notification

register = template.Library()


@register.inclusion_tag('notifications/show_notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    notifications = Notification.objects.filter(to_user=request_user).exclude(is_seen=True).order_by('-date')
    return {
        'notifications': notifications
    }