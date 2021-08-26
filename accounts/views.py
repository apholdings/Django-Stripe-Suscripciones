from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CancelSubscriptionForm
from django.views.generic import FormView, View
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

import stripe
from django.contrib import messages


class CancelSubscriptionView(LoginRequiredMixin, FormView):
    form_class=CancelSubscriptionForm

    def get_success_url(self):
        return reverse("user:subscription", kwargs={"username": self.request.user.username})

    def form_valid(self, form):
        stripe.Subscription.delete(self.request.user.subscription.stripe_subscription_id)
        messages.success(self.request, "You have successfully cancelled your subscription")
        return super().form_valid(form)


class UserSubscriptionView(View):
    def get(self, request, username,*args, **kwargs):
        user = get_object_or_404(User, username=username)
        context={
            'user':user
        }
        return render(request, 'users/user_subscription.html',context)