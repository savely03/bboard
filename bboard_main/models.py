from django.db import models
from django.contrib.auth.models import AbstractUser


class AvdUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Слать оповещения о новых комментариях')

    class Meta(AbstractUser.Meta):
        pass

    def delete(self, *args, **kwargs):
        for bb in self.bbs:
            bb.delete()
        super().delete(*args, **kwargs)


class AbstractRubrics(models.Model):
    name = models.CharField(max_length=50, db_index=True, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('order', 'name')
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'


class SuperRubric(AbstractRubrics):
    class Meta:
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubric(AbstractRubrics):
    class Meta:
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'

    super_rubric = models.ForeignKey(SuperRubric, on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name='Надрубрика', related_name='sub_rubrics')

    def __str__(self):
        return f'{self.super_rubric} - {self.name}'


class Bb(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Подрубрика', related_name='bbs')
    title = models.CharField(max_length=50, verbose_name='Название товара')
    content = models.TextField(verbose_name='Описание товара')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена товара')
    contacts = models.CharField(max_length=50, verbose_name='Контакты')
    image = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Основная иллюстрация к объявлению')
    author = models.ForeignKey(AvdUser, on_delete=models.CASCADE, related_name='bbs', verbose_name='Автор объявления')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, null=True, verbose_name='Объявление')
    image = models.ImageField(upload_to='additional/%Y/%m/%d', verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'


class Comment(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, related_name='bbs', verbose_name='Объявление')
    author = models.CharField(max_length=30, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Показывать в списке')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')

    def __str__(self):
        return f'Комментарий к {self.bb.title}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)
