from django.contrib import admin
from django_celery_results.models import TaskResult
from django_celery_results.admin import TaskResultAdmin

admin.site.unregister(TaskResult)

class CustomTaskResultAdmin(TaskResultAdmin):
    list_display = ('id', 'task_id', 'status', 'result', 'date_created', 'date_done', 'traceback')
    list_filter = ('status', 'result', 'date_created', 'date_done')

admin.site.register(TaskResult, CustomTaskResultAdmin)

admin.site.site_header = "Server ADMINistration"
admin.site.site_title = "Server Admin Portal"
admin.site.index_title = "Welcome to thesis project"


