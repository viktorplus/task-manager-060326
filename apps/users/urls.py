from django.urls import path

from apps.users.views import UserListGenericView

app_name = 'users'

urlpatterns = [
    path('', UserListGenericView.as_view()),
]