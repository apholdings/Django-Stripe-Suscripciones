from django.contrib import admin
from .models import Course, Chapter, Lesson, Author, Pricing, Subscription
# Register your models here.
admin.site.register(Author)
admin.site.register(Chapter)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Pricing)
admin.site.register(Subscription)