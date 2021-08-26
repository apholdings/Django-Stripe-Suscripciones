from django.urls import path

from .views import PricingView, PaymentView,CreateSubscriptionView, ThankYouView, RetryInvoiceView, webhook, ChangeSubscriptionView

app_name="payment"

urlpatterns = [
    path('pricing/', PricingView.as_view(), name="pricing"),
    path('pricing/<slug>/', PaymentView.as_view(), name="payment"),
    path('create-subscription/', CreateSubscriptionView.as_view(), name='create-subscription'),
    path('thank-you/',ThankYouView.as_view(),name='thank-you'),
    path('retry-invoice/', RetryInvoiceView.as_view(), name='retry-invoice'),
    path('change-subscription/', ChangeSubscriptionView.as_view(), name='change-subscription'),
    path('webhook/', webhook, name='webhook'),
]
