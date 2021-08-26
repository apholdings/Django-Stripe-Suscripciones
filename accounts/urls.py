from django.urls import path

from .views import UserSubscriptionView, CancelSubscriptionView

app_name="accounts"

urlpatterns = [
    path("<str:username>/subscription/", UserSubscriptionView.as_view(), name="subscription"),
    path("<str:username>/subscription/cancel/", CancelSubscriptionView.as_view(), name="cancel-subscription"),
]
