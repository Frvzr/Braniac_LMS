from django.contrib import admin
from mainapp.models import News, Course, Lesson, CourseTeacher, CourseFeedback
from django.utils.html import format_html


# admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CourseTeacher)
# admin.site.register(CourseFeedback)


@admin.register(News)
class NewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'deleted', 'created_at')
    list_filter = ('deleted', 'created_at')
    #ordering = ('pk',)
    list_per_page = 10
    search_fields = ('title', 'intro', 'body',)
    actions = ('mark_as_delete',)

    def slug(self, obj):
        return format_html(
            '<a href= "{}" target="_blank">{}</a>',
            obj.title.lower().replace(' ', '-'),
            obj.title
        )

    slug.short_description = 'Слаг'

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'cost', 'description',
                    'deleted', 'created_at')
    list_filter = ('cost', 'created_at', 'deleted')
    list_per_page = 10
    search_fields = ('title', 'cost', 'description',)
    actions = ('mark_as_delete',)

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'


@admin.register(CourseFeedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('pk', 'course', 'user', 'rating', 'deleted', 'created')
    list_filter = ('course', 'user', 'deleted', 'created')
    #ordering = ('pk',)
    list_per_page = 10
    search_fields = ('user', 'course',)
    actions = ('mark_as_delete',)

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'
