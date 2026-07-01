from django.contrib import admin
from .models import UserProfile, Attendance, Announcement, Material

# 1. Sajili UserProfile ili isomeke kama "Students" kule Admin Panel
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('reg_number', 'get_first_name', 'get_last_name')
    search_fields = ('reg_number', 'user__first_name', 'user__last_name')

    # Mbinu za kuvuta majina kutoka kwenye table ya User
    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'Jina la Kwanza'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Jina la Mwisho'

# 2. Sajili Meza ya Mahudhurio (Attendance)
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('student__username', 'student__first_name', 'student__last_name')

# 3. Sajili Meza ya Matangazo (Announcement)
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'content')

# 4. Sajili Meza ya Nyaraka za Masomo (Material)
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title', 'description')