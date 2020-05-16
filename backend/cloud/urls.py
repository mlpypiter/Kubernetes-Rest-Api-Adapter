from django.urls import path
from .views import SubscriptionCreateView, ControlServerView, ChangeServerView
app_name = 'cloud'

urlpatterns = [
    path('byp/setapprovedsubscriptions/', SubscriptionCreateView.as_view()),
    path('byp/control_server/', ControlServerView.as_view()),
    path('byp.karel.cloud/updateserverstate/', ChangeServerView.as_view()),
]
