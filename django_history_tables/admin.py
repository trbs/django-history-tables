from django.contrib import admin

class HistoryAdmin(admin.ModelAdmin):
    date_hierarchy = "history_datetime"
    list_display = ('__unicode__', 'history_revision', 'history_datetime', 'history_objectid', 'history_comment')