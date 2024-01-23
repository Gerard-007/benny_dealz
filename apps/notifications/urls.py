from django.urls import path

from apps.notifications.views import notification_list_view, notification_delete_view, user_notification_delete_view

urlpatterns = [
    path('', notification_list_view, name="list"),
    path('<int:pk>/delete', notification_delete_view, name="delete"),
    path('<int:pk>/remove', user_notification_delete_view, name="user_delete"),
]