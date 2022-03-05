from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


CATEGORY = [('other', 'Разное'), ('milk', 'Молочная продукция'), ('meat', 'МЯСО'), ('vegetables', 'Овощи'), ('drink', 'Напитки')]
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Название')
    category = models.CharField(max_length=15, default='other', null=False, blank=False, choices=CATEGORY, verbose_name='Категория')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Картинка')

class Review(models.Model):
    author = models.ManyToManyField(User, related_name='reviews', blank=True, verbose_name='Автор')
    product = models.ForeignKey('webapp.Product', on_delete=models.CASCADE, related_name='review', verbose_name='Продукт')
    description = models.TextField(null=False, blank=False, verbose_name='Описание')
    grade = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
    check_moderated = models.BooleanField(default=False, verbose_name='Модерирование')
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now_add=True, verbose_name="Дата изменения")