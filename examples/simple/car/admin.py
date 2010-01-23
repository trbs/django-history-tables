from models import *
from django.contrib import admin
from django_history_tables.admin import HistoryAdmin


admin.site.register(Manufacturer)
admin.site.register(Color)
admin.site.register(Car)

admin.site.register(CarHistory, HistoryAdmin)
