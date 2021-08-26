from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.utils import timezone
from django.shortcuts import reverse
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

from allauth.account.signals import email_confirmed

from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.
# Author|
# Course|
# -Chapter|
# --Leccion

def user_directory_path(instance,filename):
    return 'courses/{0}/{1}'.format(instance.title, filename)

def chapter_directory_path(instance, filename):
    return 'courses/{0}/{1}/{2}'.format(instance.course, instance.title, filename)

def lesson_directory_path(instance, filename):
    return 'courses/{0}/{1}/Lesson #{2}: {3}/{4}'.format(instance.course, instance.chapter, instance.lesson_number,instance.title, filename)


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Pricing(models.Model):
    name= models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    stripe_price_id = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    currency = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE, related_name='subscriptions')
    created = models.DateTimeField(auto_now_add=True)
    stripe_subscription_id = models.CharField(max_length=50)
    status = models.CharField(max_length=100)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.user.email

    @property
    def is_active(self):
        return self.status == "active" or self.status == "trialing"


class Course(models.Model):
    authors = ManyToManyField(Author)
    pricing_tiers = models.ManyToManyField(Pricing, blank=True)
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    video = models.FileField(upload_to=user_directory_path)
    vimeo_video = models.CharField(verbose_name="Vimeo Video ID (Optional)",max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='published', null=False, unique=True)
    published = models.DateTimeField(default=timezone.now)
    is_active=models.BooleanField(default=True)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={
            'slug': self.slug
        })


def post_email_confirmed(request, email_address, *args, **kwargs):
    user = User.objects.get(email=email_address.email)
    free_trial_pricing = Pricing.objects.get(name='Free Trial')

    subscription = Subscription.objects.create(
        user=user,
        pricing=free_trial_pricing
    )

    #Crear cliente en stripe
    stripe_customer = stripe.Customer.create(
        email=user.email
    )

    stripe_subscription = stripe.Subscription.create(
        customer=stripe_customer["id"],
        items=[{'price': 'price_1HAFmwA2yg3TLgLvda4AwmQb'}],
        trial_period_days=7
    )

    subscription.status=stripe_subscription["status"]
    subscription.stripe_subscription_id = stripe_subscription["id"]
    subscription.save()
    user.stripe_customer_id=stripe_customer["id"]
    user.save()


class Chapter(models.Model):
    course = ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    chapter_number = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to=chapter_directory_path)
    video = models.FileField(upload_to=chapter_directory_path)
    vimeo_video = models.CharField(verbose_name="Vimeo Video ID (Optional)",max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:chapter-detail", kwargs={
            'course_slug': self.course.slug,
            'chapter_number': self.chapter_number,
        })


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,blank=True, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,blank=True, null=True)
    lesson_number = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to=lesson_directory_path, default='courses/default.jpg')
    video = models.FileField(upload_to=lesson_directory_path)
    vimeo_video = models.CharField(verbose_name="Vimeo Video ID (Optional)",max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("courses:lesson-detail", kwargs={
            'course_slug': self.chapter.course.slug,
            'chapter_number': self.chapter.chapter_number,
            'lesson_number': self.lesson_number
        })


email_confirmed.connect(post_email_confirmed)