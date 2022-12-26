from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class News(models.Model):
    title = models.CharField(max_length=256, verbose_name=_('Article title'))
    preamble = models.CharField(max_length=1024, verbose_name=_('Preamble'))

    body = models.TextField(verbose_name=_('Content'), blank=True, null=True,)
    body_as_markdown = models.BooleanField(
        default=False, verbose_name=_('Markdown markup'))

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created'), editable=False)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated'), editable=False)
    deleted = models.BooleanField(default=False, verbose_name=_('Deleted'))

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

    title = models.CharField(max_length=256, verbose_name=_('Title'))
    description = models.TextField(
        verbose_name=_('Description'),  blank=True, null=True)

    cost = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name=_('Cost'), default=0)

    cover = models.CharField(
        max_length=25, default="no_image.svg", verbose_name=_("Cover"))

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создан', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    deleted = models.BooleanField(default=False, verbose_name=_('Deleted'))

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
        Course, on_delete=models.CASCADE, verbose_name=_('Course'))
    num = models.PositiveIntegerField(
        default=0, verbose_name=_('Lesson number'))

    title = models.CharField(max_length=256, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))

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
    first_name = models.CharField(max_length=256, verbose_name=_('First name'))
    last_name = models.CharField(max_length=256, verbose_name=_('Last name'))
    day_birth = models.DateField(verbose_name=_("Birth date"), default='')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'курс к учителю'
        verbose_name_plural = 'курсы к учителям'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class CourseFeedback(models.Model):

    RATINGS = (
        (5, '⭐⭐⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (3, '⭐⭐⭐'),
        (2, '⭐⭐'),
        (1, '⭐'),
    )

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("Course"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name=_("User"))
    rating = models.SmallIntegerField(
        choices=RATINGS, default=5, verbose_name=_('Rating'))
    feedback = models.TextField(verbose_name=_(
        'Feedback'), default='Без отзыва',)

    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв на {self.course} от {self.user}'
