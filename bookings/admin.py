from django.contrib import admin
from .models import MenuItem, Table, Booking

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'category')
    search_fields = ('name', 'category')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('size',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'table', 'date', 'time')
    list_filter = ('date', 'time')