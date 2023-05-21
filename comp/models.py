from django.db import models
from django.conf import settings

# Create your models here.


class Socket(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class MemoryType(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Processor(models.Model):
    name = models.CharField(max_length=250)
    cores = models.IntegerField()
    frequency = models.FloatField()
    socket = models.ForeignKey('Socket', on_delete=models.CASCADE)
    recomend = models.IntegerField(default=0, verbose_name='Popularity')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class RAM(models.Model):
    name = models.CharField(max_length=250)
    capacity = models.IntegerField()
    frequency = models.FloatField()
    memory_type = models.ForeignKey('MemoryType', on_delete=models.CASCADE)
    recomend = models.IntegerField(default=0, verbose_name='Popularity')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class GrapCard(models.Model):
    name = models.CharField(max_length=250)
    video_memory = models.IntegerField()
    proc_frequency = models.IntegerField()
    effective_mem_freq = models.IntegerField()
    recomend = models.IntegerField(default=0, verbose_name='Popularity')

    class Meta:
        verbose_name = 'Graphical Crad'
        verbose_name_plural = 'Graphical Cards'
        ordering = ['id']

    def __str__(self):
        return self.name


class Motherboard(models.Model):
    name = models.CharField(max_length=250)
    socket = models.ForeignKey('Socket', on_delete=models.CASCADE)
    chipset = models.CharField(max_length=10)
    memory_type = models.ForeignKey('MemoryType', on_delete=models.CASCADE)
    max_memory = models.IntegerField()
    recomend = models.IntegerField(default=0, verbose_name='Popularity')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class History(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    result = models.CharField(max_length=50)
    comp_type = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)
