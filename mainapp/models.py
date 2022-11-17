from email.policy import default
from tabnanny import verbose
from unicodedata import decimal
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class News(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    preamble = models.CharField(max_length=1024, verbose_name='Интро')

    body = models.TextField(verbose_name='Содержимое', blank=True, null=True,)
    body_as_markdown = models.BooleanField(
        default=False, verbose_name='Разметка в формате Markdown')

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создан', editable=False)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Обновлен', editable=False)
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return f'{self.pk} {self.title}'

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class CoursesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Course(models.Model):

    objects = CoursesManager()

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(
        verbose_name='Описание',  blank=True, null=True)

    cost = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='Стоимость', default=0)

    cover = models.CharField(
        max_length=25, default="no_image.svg", verbose_name="Cover")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создан', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    description_as_markdown = models.BooleanField(
        verbose_name="As markdown", default=False)

    def __str__(self):
        return f'{self.pk} {self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='Курс')
    num = models.PositiveIntegerField(default=0, verbose_name='Номер урока')

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')

    description_as_markdown = models.BooleanField(
        verbose_name="as_markdown", default=False)

    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Created", editable=False)
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Edited", editable=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.course.title} | {self.num} | {self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class CourseTeacher(models.Model):
    course = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')
    day_birth = models.DateField(verbose_name="Birth date", default='')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'курс к учителю'
        verbose_name_plural = 'курсы к учителям'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()
