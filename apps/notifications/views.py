from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from apps.notifications.models import Notification


@login_required
def notification_list_view(request):
    notifications = Notification.objects.filter(to_user=request.user.is_a_dealer, is_seen=False).order_by('-date')
    # Notification.objects.filter(to_user=request.user.is_a_dealer, is_seen=False).update(is_seen=True)

    context = {
        'notifications': notifications
    }
    return render(request, 'notifications/notification_list.html', context)


def notification_delete_view(request, pk):
    user = request.user.is_a_dealer
    notification = Notification.objects.filter(pk=pk, to_user=user)
    notification.update(is_seen=True)
    return redirect('notifications:list')


def user_notification_delete_view(request, pk):
    user = request.user
    notification = Notification.objects.filter(pk=pk, to_user=user)
    notification.update(is_seen=True)
    return redirect('notifications:list')


@login_required
def notification_counts(request):
    notification_count = Notification.objects.filter(to_user=request.user).exclude(is_seen=True).order_by('-date').count()
    return {
        'notification_count': notification_count,
    }


# def notification_counts(request):
#     comment_notifications = Notification.objects.filter(notification_type=2).filter(is_seen=False).count()
#     subscription_notifications = Notification.objects.filter(notification_type=3).filter(is_seen=False).count()
#     dealer_message_notifications = Notification.objects.filter(notification_type=1).filter(is_seen=False).count()
#     user_message_notifications = Notification.objects.filter(notification_type=4).filter(is_seen=False).count()

#     latest_comment_notifications = Notification.objects.filter(notification_type=2).filter(is_seen=False)[:3]
#     latest_subscription_notifications = Notification.objects.filter(notification_type=3).filter(is_seen=False)[:3]
#     latest_dealer_message_notifications = Notification.objects.filter(notification_type=1).filter(is_seen=False)[:3]
#     latest_user_message_notifications = Notification.objects.filter(notification_type=4).filter(is_seen=False)[:3]
#     return {
#         'comment_notifications': comment_notifications,
#         'subscription_notifications': subscription_notifications,
#         'dealer_message_notifications': dealer_message_notifications,
#         'user_message_notifications': user_message_notifications,
#         'latest_comment_notifications': latest_comment_notifications,
#         'latest_subscription_notifications': latest_subscription_notifications,
#         'latest_dealer_message_notifications': latest_dealer_message_notifications,
#         'latest_user_message_notifications': latest_user_message_notifications,
#     }
