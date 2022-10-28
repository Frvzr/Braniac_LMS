from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from datetime import datetime
from mainapp.models import News, Course, Lesson, CourseTeacher


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['contacts'] = [
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHcrhA',
                'city': 'Санкт‑Петербург',
                'phone': '+7-999-11-11111',
                'email': 'geeklab@spb.ru',
                'address': 'территория Петропавловская крепость, 3Ж'
            },
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHX3xB',
                'city': 'Казань',
                'phone': '+7-999-22-22222',
                'email': 'geeklab@kz.ru',
                'address': 'территория Кремль, 11, Казань, Республика Татарстан, Россия'
            },
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHh9kD',
                'city': 'Москва',
                'phone': '+7-999-33-33333',
                'email': 'geeklab@msk.ru',
                'address': 'Красная площадь, 7, Москва, Россия'
            }
        ]
        return context_data


class CoursesListView(TemplateView):
    template_name = 'mainapp/courses_list.html'

    def get_context_data(self, **kwargs):

        context_data = super(CoursesListView, self).get_context_data(**kwargs)
        context_data["objects"] = Course.objects.all()[:7]
        return context_data


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Приветствую, путник!'
        return context_data


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = News.objects.all()[:5]
        # context_data['object_list'] = [
        #     {
        #         'title': 'Первая новость',
        #         'preview': 'Превью к первой новости',
        #         'date': '2022-01-01'
        #     },
        #     {
        #         'title': 'Вторая новость',
        #         'preview': 'Превью к второй новости',
        #         'date': '19-10-2022'
        #     },
        #     {
        #         'title': 'Третья новость',
        #         'preview': 'Превью',
        #         'date': '18-10-2022'
        #     },
        #     {
        #         'title': 'Четвертая новость',
        #         'preview': 'Превью',
        #         'date': '17-10-2022'
        #     },
        #     {
        #         'title': 'Пятая новость',
        #         'preview': 'Превью',
        #         'date': datetime.now().strftime('%d.%m.%Y')
        #     },
        # ]
        return context_data


# class NewsWithPaginatorView(NewsView):
#     def get_context_data(self, page, **kwargs):
#         context = super().get_context_data(page=page, **kwargs)
#         context["page_num"] = page
#         return context


class NewsDetail(TemplateView):
    template_name = 'mainapp/news_detail.html'

    def get_context_data(self, pk=None, **kwargs):
        context_data = super().get_context_data(pk=pk, **kwargs)
        context_data['object'] = get_object_or_404(
            News, pk=self.kwargs.get('pk'))
        return context_data


class CoursesDetail(TemplateView):
    template_name = 'mainapp/courses_detail.html'

    def get_context_data(self, pk=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["course_object"] = get_object_or_404(Course, pk=pk)
        context_data["lessons"] = Lesson.objects.filter(
            course=context_data["course_object"])
        context_data["teachers"] = CourseTeacher.objects.filter(
            course=context_data["course_object"])
        return context_data
