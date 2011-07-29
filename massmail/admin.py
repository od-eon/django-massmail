from massmail.models import *
from django.contrib import admin

class QueueAdmin(admin.ModelAdmin):
    list_display = ['id', '__unicode__', 'status', 'sent', 'hostname'] 
    list_filter = ('status', 'sent', 'hostname')
    search_fields = ('subject', 'body')


class QueueEmailAdmin(admin.ModelAdmin):
    list_display = ['id', '__unicode__', 'queue', 'sent'] 
    list_filter = ('to_email',)
    search_fields = ('to_email',)

admin.site.register(Queue, QueueAdmin)
admin.site.register(QueueEmail, QueueEmailAdmin)
