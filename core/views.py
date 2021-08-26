from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from courses.models import Course


class HomeView(View):
    def get(self, request, *args, **kwargs):
        courses = Course.objects.filter(is_active=True)

        paginator = Paginator(courses, 9)
        page_number = request.GET.get('page')
        courses_data = paginator.get_page(page_number)

        context={
            'courses':courses_data
        }
        return render(request, 'pages/index.html', context)