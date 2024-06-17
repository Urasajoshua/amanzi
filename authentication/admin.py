from django.contrib import admin
from .models import User, Dissertation, Comment, Supervision ,Department,Course
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('firstname',  'surname', 'role','RegNo','course')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'firstname','surname', 'role','RegNo','course')}
        ),
    )
    list_display = ('email', 'firstname','middlename','surname','RegNo','role','course', 'is_staff')
    search_fields = ('email', 'firstname', 'surname')
    ordering = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(Comment)


class SupervisionAdminForm(forms.ModelForm):
    class Meta:
        model = Supervision
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(role='STUDENT')
        self.fields['student'].label_from_instance = lambda obj: f"{obj.firstname} {obj.surname} ({obj.RegNo})"
        self.fields['supervisor'].queryset = User.objects.filter(role='SUPERVISOR')
        self.fields['supervisor'].label_from_instance = lambda obj: f"{obj.firstname} {obj.surname} ({obj.email})"

class SupervisionAdmin(admin.ModelAdmin):
    form = SupervisionAdminForm
    list_display = ('student', 'supervisor', 'created_at')
    search_fields = ('student__firstname', 'student__surname', 'supervisor__firstname', 'supervisor__surname')
    list_filter = ('created_at',)

admin.site.register(Supervision, SupervisionAdmin)



class DissertationAdminForm(forms.ModelForm):
    class Meta:
        model = Dissertation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.all()
        self.fields['student'].label_from_instance = lambda obj: f"{obj.firstname} {obj.surname}"

@admin.register(Dissertation)
class DissertationAdmin(admin.ModelAdmin):
    form = DissertationAdminForm
    list_display = ('title','student','file','status')
   

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'year')
    search_fields = ('name', 'department__name')
    list_filter = ('department', 'year')
