from django.urls import path

from .views import CourseDetailView, ChapterDetailView, LessonDetailView

app_name= "courses"

urlpatterns = [
    path('<slug>/', CourseDetailView.as_view(), name="detail"),
    path('<course_slug>/<int:chapter_number>/', ChapterDetailView.as_view(), name="chapter-detail"),
    path('<course_slug>/<int:chapter_number>/<int:lesson_number>/', LessonDetailView.as_view(), name="lesson-detail"),
]
