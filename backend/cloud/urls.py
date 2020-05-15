from django.urls import path
from .views import SubscriptionCreateView
app_name = 'cloud'

urlpatterns = [
    path('byp/setapprovedsubscriptions/', SubscriptionCreateView.as_view()),
]
