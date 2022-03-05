from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

CATEGORY = [('other', 'Разное'), ('milk', 'Молочная продукция'), ('meat', 'МЯСО'), ('vegetables', 'Овощи'), ('drink', 'Напитки')]
class Product(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Название')
    category = models.CharField(max_length=15, default='other', null=False, blank=False, choices=CATEGORY, verbose_name='Категория')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Картинка')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        db_table = 'products'

    def __str__(self):
        return f'{self.name}'


    def get_absolute_url(self):
        return reverse('webapp:index')

    def average(self):
        sum = 0
        count = 0
        reviews = self.review.filter(check_moderated=True)
        if reviews:
            for i in reviews:
                sum += i.grade
                count += 1
            return sum/count



class Review(models.Model):
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, blank=True, verbose_name='Автор')
    product = models.ForeignKey('webapp.Product', blank=True, on_delete=models.CASCADE, related_name='review', verbose_name='Продукт')
    description = models.TextField(null=False, blank=False, verbose_name='Описание')
    grade = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
    check_moderated = models.BooleanField(default=False, verbose_name='Модерирование')
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now_add=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        db_table = 'reviews'
        permissions = [
            ('can_view_not_moderated_list', 'Can view not moderated list')
        ]

    def get_absolute_url(self):
        return reverse('webapp:index')

    def __str__(self):
        return f'{self.author.username}===Оценка: {self.grade}'