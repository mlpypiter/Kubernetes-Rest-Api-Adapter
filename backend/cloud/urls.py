from django.urls import path
from .views import SubscriptionCreateView, ControlServerView, ChangeServerView, GetbrokenSubscriptionsView, \
    UpdateServiceDetail
app_name = 'cloud'

urlpatterns = [
    path('byp/setapprovedsubscriptions/', SubscriptionCreateView.as_view()),
    path('byp/control_server/', ControlServerView.as_view()),

    path('byp.karel.cloud/byp/updateservicedetail/', UpdateServiceDetail.as_view()),
    path('byp.karel.cloud/byp/updateserverstate/', ChangeServerView.as_view()),
    path('byp.karel.cloud/byp/getbrokensubscriptions/', GetbrokenSubscriptionsView.as_view()),
]
