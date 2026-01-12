from django.contrib import admin
from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role')
    search_fields = ('name', 'role')
    list_editable = ()
    list_display_links = ('name',)

