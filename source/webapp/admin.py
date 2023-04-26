from django.contrib import admin

from webapp.models import Organization, WorkTime, Branch

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'start_time', 'end_time', 'email']

class WorkTimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'start_time', 'end_time', 'created_at', 'organization', 'branch']



class BranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'organization', 'qr_code']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(WorkTime, WorkTimeAdmin)
admin.site.register(Branch, BranchAdmin)
