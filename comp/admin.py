from django.contrib import admin
from .models import *

# Register your models here.


class RAMAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'recomend')
    list_display_links = ('name',)
    search_fields = ('id', 'name')


class ProcAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'recomend')
    list_display_links = ('name',)
    search_fields = ('id', 'name')


class GrCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'recomend')
    list_display_links = ('name',)
    search_fields = ('id', 'name')


class MemTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('id', 'name')


class SocketAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('id', 'name')


class MotherboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'recomend')
    list_display_links = ('name',)
    search_fields = ('id', 'name')


admin.site.register(RAM, RAMAdmin)
admin.site.register(Processor, ProcAdmin)
admin.site.register(GrapCard, GrCardAdmin)
admin.site.register(Motherboard, MotherboardAdmin)
admin.site.register(MemoryType, MemTypeAdmin)
admin.site.register(Socket, SocketAdmin)
