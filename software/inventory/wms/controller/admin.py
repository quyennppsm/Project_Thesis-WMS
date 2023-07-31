from django.contrib import admin
from controller.models import Layout, Slot, Product
from log.models import LogCarrier, LogOrder

class ControllerAdminSite(admin.AdminSite):
    site_header = "Controller Admin"
    site_title = "Controller Admin Portal"
    index_title = "Welcome to Controller Portal"

class LayoutOption(admin.ModelAdmin):
    list_display = ('id', 'identification', 'emc')
    list_filter = ['floor', 'section', 'location', 'shelf', 'column', 'row']

controller_admin_site = ControllerAdminSite(name='controller_admin')

controller_admin_site.register(Layout, LayoutOption)
controller_admin_site.register(Slot)
controller_admin_site.register(Product)
controller_admin_site.register(LogCarrier)
controller_admin_site.register(LogOrder)