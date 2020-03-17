from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


# Create your models here.
class Topic(models.Model):
    """Тема которую изучает пользователь"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.SET(0))
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Entry(models.Model):
    """Инфа, изученная пользователем по теме"""
    topic = models.ForeignKey(Topic,
                              on_delete=models.SET(0))
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, default='Тема')
    url = models.URLField(max_length=200, default='a')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.text[:50] + "..."


class EntryAdmin(admin.ModelAdmin):
    list_display = ('text', 'date_added', 'views')
