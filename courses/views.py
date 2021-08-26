from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from .models import Course, Chapter, Lesson
from django.shortcuts import get_object_or_404, render

# Create your views here.
class CourseDetailView(View):
    def get(self, request, slug,*args, **kwargs):
        course = get_object_or_404(Course, slug=slug)
        context={
            'course':course
        }
        return render(request, 'courses/pages/course/detail.html', context)


class ChapterDetailView(LoginRequiredMixin ,View):
    def get(self, request, course_slug, chapter_number,*args, **kwargs):
        
        course = get_object_or_404(Course, slug=course_slug)
        subscription = request.user.subscription
        pricing_tier = subscription.pricing
        subscription_is_active = subscription.status == "active" or subscription.status == "trialing"

        chapter_qs = Chapter.objects.filter(course__slug=course_slug).filter(chapter_number=chapter_number)
        chapter = chapter_qs[0]

        context={
            'chapter':chapter,
        }

        context.update({
            "has_permission": pricing_tier in course.pricing_tiers.all() and subscription_is_active
        })

        return render(request, 'courses/pages/chapter/detail.html', context)


class LessonDetailView(LoginRequiredMixin ,View):
    def get(self, request, course_slug, chapter_number, lesson_number,*args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)

        subscription = request.user.subscription
        pricing_tier = subscription.pricing
        subscription_is_active = subscription.status == "active" or subscription.status == "trialing" 
        
        chapter_qs = Chapter.objects.filter(course__slug=course_slug).filter(chapter_number=chapter_number)
        chapter = chapter_qs[0]

        lesson_qs = Lesson.objects \
            .filter(chapter__course__slug=course_slug) \
            .filter(chapter__chapter_number=chapter_number) \
            .filter(lesson_number=lesson_number)
        lesson = lesson_qs[0]

        context={
            'chapter':chapter,
            'lesson':lesson
        }
        context.update({
            "has_permission": pricing_tier in course.pricing_tiers.all() and subscription_is_active
        })
        return render(request, 'courses/pages/lesson/detail.html', context)