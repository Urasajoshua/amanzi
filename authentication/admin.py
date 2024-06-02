from django.contrib import admin
from .models import User, Dissertation, Comment, Supervision ,Department,Course
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('firstname', 'middlename', 'surname', 'role','RegNo','course')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'firstname', 'middlename', 'surname', 'role')}
        ),
    )
    list_display = ('email', 'firstname','middlename','surname','RegNo','role','course', 'is_staff')
    search_fields = ('email', 'firstname', 'surname')
    ordering = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(Dissertation)
admin.site.register(Comment)
admin.site.register(Supervision)



@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'year')
    search_fields = ('name', 'department__name')
    list_filter = ('department', 'year')
